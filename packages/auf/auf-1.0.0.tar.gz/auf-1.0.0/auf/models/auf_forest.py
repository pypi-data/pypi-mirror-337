import warnings

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from causalml.inference.tree import UpliftRandomForestClassifier

warnings.filterwarnings("ignore")


class AufRandomForestClassifier(UpliftRandomForestClassifier):
    def __init__(
        self,
        control_name,
        n_estimators=10,
        max_features=10,
        random_state=None,
        max_depth=5,
        min_samples_leaf=100,
        min_samples_treatment=10,
        n_reg=10,
        early_stopping_eval_diff_scale=1,
        evaluationFunction="KL",
        normalization=True,
        honesty=False,
        estimation_sample_size=0.5,
        n_jobs=-1,
        joblib_prefer: str = "threads",
    ):
        self.params = {
            "control_name": control_name,
            "n_estimators": n_estimators,
            "max_features": max_features,
            "random_state": random_state,
            "max_depth": max_depth,
            "min_samples_leaf": min_samples_leaf,
            "min_samples_treatment": min_samples_treatment,
            "n_reg": n_reg,
            "early_stopping_eval_diff_scale": early_stopping_eval_diff_scale,
            "evaluationFunction": evaluationFunction,
            "normalization": normalization,
            "honesty": honesty,
            "estimation_sample_size": estimation_sample_size,
            "n_jobs": n_jobs,
            "joblib_prefer": joblib_prefer,
        }
        super().__init__(**self.params)
        self.base_model = CatBoostClassifier(
            n_estimators=200, learning_rate=0.05, max_depth=4, silent=True
        )
        self.ctrl_preds_ = None
        self.trmnt_preds_ = None

    def get_params(self):
        # Вызываем метод get_params из родительского класса и добавляем новый параметр
        return self.params

    def fit(self, X: pd.DataFrame, y: pd.Series, treatment: pd.Series):
        self.feature_names_ = X.columns.tolist()
        fltr = treatment.astype("str") == self.params["control_name"]
        self.base_model.fit(X=X[fltr], y=y[fltr])
        with np.errstate(divide="ignore", invalid="ignore"):
            super().fit(
                X=X.values, y=y.values, treatment=treatment.astype("str").values
            )
        return super()

    def predict(self, X: pd.DataFrame):
        self.ctrl_preds_ = self.base_model.predict_proba(X)[:, 1]
        with np.errstate(divide="ignore", invalid="ignore"):
            uplift = super().predict(X.values).reshape(-1)
        self.trmnt_preds_ = self.ctrl_preds_ + uplift
        return uplift
