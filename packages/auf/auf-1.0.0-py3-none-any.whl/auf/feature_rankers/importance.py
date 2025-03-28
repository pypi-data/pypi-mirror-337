import typing as tp

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from causalml.feature_selection import FilterSelect
from causalml.inference.tree import UpliftRandomForestClassifier
from sklift.models import SoloModel


class ImportanceRanker:
    """Sorts features by their importance scores from some model.

    Uses one of available uplift or propensity modelling methods which provides feature_importances_
    Sorts features either at one time or recursively elliminating features by one or some fixed percent
    This ranker can work only with train dataset to calculate feature importances

    Note: 'dropping' below means "don't consider it in further ranking process", not "remove feature from the feature list"

    Args:
        model_class ([propensity, s-learner, uplift tree]): uplift model object
        model_params (dict): dictionary of model parameters
        sorting_mode (string, ['at_once', 'iterative', 'rfe']): features sorting method to be used
            'at_once' for just sorting features with single model
            'iterative' for 'dropping' 10 % worst feature (by importance scores) each time till 1 feature remains
            'rfe' for 'dropping' one worst feature (by importance scores) each time till 1 feature remains
        name (string): ranker name
        data (pd.DataFrame): DataFrame containing target, features, and treatment group
        features (1d array-like): list of feature names, that are columns in the data DataFrame
        target_col (string): target column name
        treatment_col (string): treatment column name

    Examples:
        >>> from AUF.feature_selection import ImportanceRanker
        >>> ranker = ImportanceRanker(SoloModel, model_params, "at_once")
        >>> ranked_features, ranked_importances = ranker.run(df, features, target_col, treatment_col)

    Returns: None
    """

    def __init__(
        self,
        model_class: tp.Any,
        model_params: tp.Dict[str, tp.Any],
        sorting_mode: str,
        name: str = "__empty_name__",
    ):

        assert sorting_mode in ("at_once", "iterative", "rfe")

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
        self._sorting_mode = sorting_mode
        self._name: str = name
        self._ranked_features: tp.List[str] = []
        self._ranked_features_scores: tp.List[float] = []

    def _run_propensity(
        self, data: pd.DataFrame, features: tp.List[str], target_col: str
    ) -> tp.List[str]:
        model = self._model_class(**self._model_params)
        model.fit(data[features], data[target_col])
        importances = model.feature_importances_
        features_info = list(zip(importances, features))
        features_info = sorted(features_info, key=lambda x: -x[0])
        importances, ranked_features = map(list, zip(*features_info))
        return ranked_features, importances

    def _run_s_learner(
        self,
        data: pd.DataFrame,
        features: tp.List[str],
        target_col: str,
        treatment_col: str,
    ) -> tp.List[str]:
        model = self._model_class(**self._model_params)
        model.fit(data[features], data[target_col], data[treatment_col])
        importances = model.estimator.feature_importances_
        feature_names = model.estimator.feature_names_
        features_info = list(zip(importances, feature_names))
        features_info = [
            p for p in features_info if p[1] not in [treatment_col, "treatment"]
        ]
        features_info = sorted(features_info, key=lambda x: -x[0])
        importances, ranked_features = map(list, zip(*features_info))
        return ranked_features, importances

    def _run_uplift_forest(
        self,
        data: pd.DataFrame,
        features: tp.List[str],
        target_col: str,
        treatment_col: str,
    ) -> tp.List[str]:
        model = self._model_class(**self._model_params)
        model.fit(
            X=data[features].values,
            treatment=data[treatment_col]
            .apply(lambda t: "treatment" if t == 1 else "control")
            .values,
            y=data[target_col].values,
        )
        importances = model.feature_importances_
        features_info = list(zip(importances, features))
        features_info = sorted(features_info, key=lambda x: -x[0])
        importances, ranked_features = map(list, zip(*features_info))
        return ranked_features, importances

    def _run(
        self,
        data: pd.DataFrame,
        features: tp.List[str],
        target_col: str,
        treatment_col: str,
    ) -> tp.List[str]:
        """Just calls needed model runner"""

        # self.model_info = (class, rfe-mode, params dict)
        ranked_features: tp.List[str] = []
        importances: tp.List[float] = []

        if self._model_class is SoloModel:
            ranked_features, importances = self._run_s_learner(
                data, features, target_col, treatment_col
            )
        elif self._model_class is UpliftRandomForestClassifier:
            ranked_features, importances = self._run_uplift_forest(
                data, features, target_col, treatment_col
            )
        else:
            # rank features with propensity model
            ranked_features, importances = self._run_propensity(
                data, features, target_col
            )

        return ranked_features, importances

    def run(
        self,
        data: pd.DataFrame,
        features: tp.List[str],
        target_col: str,
        treatment_col: str,
    ) -> tp.Tuple[tp.List[str], tp.List[float]]:
        """Defines the strategy of ranking features (at once, iterative, rfe)"""

        # self.model_info = (class, rfe-mode, params dict)
        ranked_features: tp.List[str] = features.copy()
        importances: tp.List[float] = [0.0 for f in ranked_features]

        if self._sorting_mode == "at_once":
            ranked_features, importances = self._run(
                data, ranked_features, target_col, treatment_col
            )
        elif self._sorting_mode == "iterative":
            # 10%
            n_top = len(features)
            while n_top:
                feats, imps = self._run(
                    data, ranked_features[:n_top], target_col, treatment_col
                )
                ranked_features[:n_top] = feats
                importances[:n_top] = imps
                n_top = int(n_top * 0.9)
        else:
            # rfe
            for n_top in range(len(features), 0, -1):
                feats, imps = self._run(
                    data, ranked_features[:n_top], target_col, treatment_col
                )
                ranked_features[:n_top] = feats
                importances[:n_top] = imps

        self._ranked_features = ranked_features.copy()
        self._ranked_features_scores = importances.copy()
        return self._ranked_features, self._ranked_features_scores

    def get_ranker_name(self) -> str:
        return self._name

    def get_ranked_features(self) -> tp.List[str]:
        return self._ranked_features

    def get_ranked_features_scores(self) -> tp.List[float]:
        return self._ranked_features_scores
