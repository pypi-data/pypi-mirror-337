import typing as tp

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from causalml.feature_selection import FilterSelect
from causalml.inference.tree import UpliftRandomForestClassifier
from sklift.models import SoloModel


class StepwiseRanker:
    """Sorts features using forward pass from stepwise algorithm.

    Idea:
        - at first we have empty final features set and full candidate features set
        - we choose every time one feature to make model quality to grow the most
        - if we can't do that, we choose the feature that causes the least quality decrease

    Quality:
        - it is meant to be an uplift metric (qini, uplift@k)
        - it is optimized directly with the procedure described below

    Note:
        - we can use any uplift model because we don't need to know feature_importances_
        - this ranker works both with train and validation datasets to measure quality on new data
        - it only sorts features, doesn't drop them

    Stepwise forward pass algorithm steps & components
        - selected features list
        - potentially useful features list
        - feature usefulness = median uplift metric growth (use validation data)
        - median estimation with boostrap
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
        train_data,
        val_data,
        target_col: str,
        treatment_col: str,
        current_features,
        feature_to_add,
        n_test_repeats,
    ):

        x_train, y_train, t_train = (
            train_data[current_features + [feature_to_add]],
            train_data[target_col],
            train_data[treatment_col],
        )
        x_val, y_val, t_val = (
            val_data[current_features + [feature_to_add]],
            val_data[target_col],
            val_data[treatment_col],
        )

        self._model_fit(x_train[current_features + [feature_to_add]], y_train, t_train)
        preds_full = self._model_predict(x_val[current_features + [feature_to_add]])

        if current_features:
            self._model_fit(x_train[current_features], y_train, t_train)
            preds_without = self._model_predict(x_val[current_features])
        else:
            preds_without = np.zeros_like(preds_full)

        delta_uplifts = [0 for _ in range(n_test_repeats)]

        for i in range(n_test_repeats):
            idxs = self._rng.choice(
                range(x_val.shape[0]), size=x_val.shape[0], replace=True
            )
            quality_full = metric(
                y_val.values[idxs], preds_full[idxs], t_val.values[idxs]
            )
            quality_without = metric(
                y_val.values[idxs], preds_without[idxs], t_val.values[idxs]
            )
            delta_uplifts[i] = quality_full - quality_without

        # mean = np.mean(delta_uplifts)
        std = np.std(delta_uplifts)

        # q_05 = np.quantile(delta_uplifts, q=0.05)
        median = np.median(delta_uplifts)
        # q_95 = np.quantile(delta_uplifts, q=0.95)

        epsilon = 1e-5
        feature_score = median / (std + epsilon)
        # return mean, std, q_05, median, q_95, feature_score
        return median, std, feature_score

    def run(
        self,
        train_data: pd.DataFrame,
        val_data: pd.DataFrame,
        all_features: tp.List[str],
        target_col: str,
        treatment_col: str,
        metric,  # : tp.Callable[]
    ) -> tp.List[str]:
        """Implements stepwise forward algorithm logic"""
        assert np.all(train_data.columns == val_data.columns)

        from datetime import datetime

        x_train, y_train, t_train = (
            train_data[all_features],
            train_data[target_col],
            train_data[treatment_col],
        )
        x_val, y_val, t_val = (
            val_data[all_features],
            val_data[target_col],
            val_data[treatment_col],
        )

        # список -- мутабельный, перепривяжем ссылку
        candidate_features = all_features.copy()
        features = []
        features_scores = []  # list of pairs (feature, score when added)

        steps = 0
        while steps < len(all_features):
            # from IPython.display import clear_output
            # clear_output(wait=True)
            # print(f"Алгоритм совершил {steps} шагов из {len(all_features)}", flush=True)
            steps += 1

            # добавляем лучшую фичу, если возможно
            best_feature = ""
            best_score = None

            # from tqdm import tqdm
            # for f in tqdm(candidate_features):
            for f in candidate_features:
                median, std, features_score = self._get_feature_gain(
                    metric,
                    train_data,
                    val_data,
                    target_col,
                    treatment_col,
                    current_features=features,
                    feature_to_add=f,
                    n_test_repeats=self._bootstrap_repeats,
                )

                if best_score is None or features_score > best_score:
                    best_feature = f
                    best_score = features_score

            features.append(best_feature)
            candidate_features.remove(best_feature)
            self._ranked_features_scores.append(best_score)

        self._ranked_features = features
        return self._ranked_features, self._ranked_features_scores

    def get_ranker_name(self) -> str:
        return self._name

    def get_ranked_features(self) -> tp.List[str]:
        return self._ranked_features
