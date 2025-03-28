import typing as tp

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from causalml.feature_selection import FilterSelect
from causalml.inference.tree import UpliftRandomForestClassifier
from sklift.models import SoloModel


class PermutationRanker:
    """Sorts features using bootstrapped estimation of uplift from using this feature with normal values instead of shuffled

    предпосылки:
        - 2 фичи в среднем теряют в метрике X при перемешивании значений
            - вопрос: какая фича "важнее" или "полезнее"? та, в которой больше уверены (меньше разбор, дисперсия)
            - больше дисперсия -- меньше интереса к фиче, поэтому ее можно учесть в знаменателе
            - проблема в малых float -- предел точности достижим легко, привим 0.001 к ним -- будет лучше
        - 2 фичи теряют X и Y: X > Y (считаем оба числа положительными, меньше нуля значит что перемешивание улучшило модель ... странно)
    - вопрос: точно ли вторая лучше? а если у нее дисперсия в 4 раза больше? а если X в 4 раза больше при этом тоже?
            - что важнее -- низкая диперсия или низкое смещение (bias-variance tradeoff)
            - нужен компромисс -- получаем необходимость в регуляризации (ограничении на среднее падение и дисперсию падения при формировании скора)
    - перемешивание ведет к потере в качестве X -- а X как получить? среднее падение или медиана падения?

    score = abs ( median (uplift_decrease) ) / ( 0.001 + variance**0.5 )
    ? clip ( 1% , 99% ) ?

    Args:
        train_data (pd.DataFrame): train DataFrame containing target, features, and treatment group
        val_data (pd.DataFrame): validation DataFrame containing target, features, and treatment group
        all_featuress (1d array-like): list of feature names, that are columns in the data DataFrame
        target_col (string): target column name
        treatment_col (string): treatment column name
        metric: function taking three arrays target, predictions and treatment and return float

    Attributes:
        _model: uplift model
        _ranked_features (1d array-like): list of ranked feature names, that are columns in the data DataFrame
        _ranked_features_scores (1d array-like): list of ranked feature importance scores
        _name (string): ranker name

    Idea:
        - train & evaluate model with all features
        - choose any feature from the feature set & shuffle its values
        - train & evaluate model with this feature being shuffled
        - estimate feature importance via bootstrap as median uplift metric divided by its std
        - repeat this procedure for every feature

    Quality:
        - it is meant to be an uplift metric (qini, uplift@k)
        - it is NOT optimized, it just shows feature importance via bootstrap statistic

    Note:
        - if there are highly correlated features, the method may work poorly for some features
          because information from shuffled feature will leak from other features into ranking model
        - it only sorts features, does not drop them

    Examples:
        >>> from AUF.feature_selection import PermutationRanker
        >>> from functools import partial
        >>> ranker = PermutationRanker(uplift_model = SoloModel(model_params))
        >>> ranked_candidates = ranker.run(
                df_train, df_val, features, target_col, treatment_col,
                partial(uplift_at_k, strategy="overall", k=0.2)
            )

    """

    def __init__(
        self,
        model_class: tp.Any,
        model_params: tp.Dict[str, tp.Any],
        rng: np.random.RandomState,
        bootstrap_repeats: int,
        name: str = "__empty_name__",
    ):

        try:
            try_to_create_model = model_class(**model_params)
            assert "fit" in list(dir(try_to_create_model))
            assert (
                set(["predict", "predict_proba"]) & set(dir(try_to_create_model))
                != set()
            )
            del try_to_create_model
        except Exception as exc:
            raise ValueError(
                "Check params for creating model: model creation failed"
            ) from exc

        self._model_class = model_class
        self._model_params = model_params
        self._rng = rng
        self._bootstrap_repeats = bootstrap_repeats
        self._model: tp.Any = None
        self._name: str = name
        self._ranked_features: tp.List[str] = []
        self._ranked_features_scores: tp.List[float] = []

    def _model_fit(self, x_train, y_train, t_train):
        self._model = self._model_class(**self._model_params)
        if self._model_class is SoloModel:
            self._model.fit(x_train, y_train, t_train)
        elif self._model_class is UpliftRandomForestClassifier:
            self._model.fit(
                X=x_train.values,
                treatment=t_train.apply(
                    lambda t: "treatment" if t == 1 else "control"
                ).values,
                y=y_train.values,
            )
        else:
            self._model.fit(x_train, y_train)

    def _model_predict(self, x_val):
        if (
            self._model_class is SoloModel
            or self._model_class is UpliftRandomForestClassifier
        ):
            return self._model.predict(x_val).reshape(-1)
        else:
            return self._model.predict_proba(x_val)[:, 1].reshape(-1)

    def _get_feature_gain(
        self,
        metric,
        x_train,
        y_train,
        t_train,
        x_val,
        y_val,
        t_val,
        feature_to_check,
        n_test_repeats,
        permutation_idxs=None,
    ):

        self._model_fit(x_train, y_train, t_train)
        preds_usual = self._model_predict(x_val)

        values_copy = x_train.loc[:, feature_to_check].values.copy()

        # it is very slow if we do it every time
        # one permutation for whole sample = permutation for every feature
        # idxs = self._rng.choice(range(x_train.shape[0]), size=x_train.shape[0], replace=False)
        idxs = permutation_idxs

        x_train.loc[:, feature_to_check] = x_train.loc[:, feature_to_check].values[idxs]
        self._model_fit(x_train, y_train, t_train)
        x_train.loc[:, feature_to_check] = values_copy
        preds_shuffled = self._model_predict(x_val)

        delta_uplifts = [0 for _ in range(n_test_repeats)]

        for i in range(n_test_repeats):
            idxs = self._rng.choice(
                range(x_val.shape[0]), size=x_val.shape[0], replace=True
            )
            quality_usual = metric(
                y_val.values[idxs], preds_usual[idxs], t_val.values[idxs]
            )
            quality_shuffled = metric(
                y_val.values[idxs], preds_shuffled[idxs], t_val.values[idxs]
            )
            delta_uplifts[i] = (
                quality_usual - quality_shuffled
            )  # assume that quality with shuffled feature values is worse

        std = np.std(delta_uplifts)
        median = np.median(delta_uplifts)

        epsilon = 1e-5
        feature_score = median / (std + epsilon)

        # mean = np.mean(delta_uplifts)
        # q_05 = np.quantile(delta_uplifts, q=0.05)
        # q_95 = np.quantile(delta_uplifts, q=0.95)
        # return mean, std, q_05, median, q_95, feature_score

        return median, std, feature_score

    def run(
        self,
        train_data: pd.DataFrame,
        val_data: pd.DataFrame,
        all_features: tp.List[str],
        target_col: str,
        treatment_col: str,
        metric,  #: tp.Callable[]
    ) -> tp.List[str]:
        """Implements permutation feature importance estimation scheme"""
        assert np.all(train_data.columns == val_data.columns)
        assert target_col in train_data.columns
        assert treatment_col in train_data.columns
        assert set(all_features) & set(train_data.columns) == set(all_features)

        features_scores = []  # list of pairs (feature, score when added)

        permutation_idxs = self._rng.choice(
            range(train_data.shape[0]), size=train_data.shape[0], replace=False
        )
        x_train, y_train, t_train = (
            train_data.loc[:, all_features],
            train_data.loc[:, target_col],
            train_data.loc[:, treatment_col],
        )
        x_val, y_val, t_val = (
            val_data.loc[:, all_features],
            val_data.loc[:, target_col],
            val_data.loc[:, treatment_col],
        )

        # from tqdm import tqdm
        # for f in tqdm(all_features):
        for f in all_features:
            _, _, feature_score = self._get_feature_gain(
                metric,
                x_train,
                y_train,
                t_train,
                x_val,
                y_val,
                t_val,
                feature_to_check=f,
                n_test_repeats=self._bootstrap_repeats,
                permutation_idxs=permutation_idxs,
            )

            features_scores.append((f, feature_score))

        features_scores = sorted(features_scores, key=lambda f_score: -f_score[1])
        self._ranked_features = [f for (f, score) in features_scores]
        self._ranked_features_scores = [score for (f, score) in features_scores]
        return self._ranked_features, self._ranked_features_scores

    def get_ranker_name(self) -> str:
        return self._name

    def get_ranked_features(self) -> tp.List[str]:
        return self._ranked_features
