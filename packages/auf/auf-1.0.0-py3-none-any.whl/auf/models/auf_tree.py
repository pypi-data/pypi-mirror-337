import warnings

import numpy as np
import pandas as pd
from causalml.inference.tree import UpliftTreeClassifier

warnings.filterwarnings("ignore")


class AufTreeClassifier(UpliftTreeClassifier):
    def __init__(
        self,
        control_name,
        max_features=None,
        max_depth=3,
        min_samples_leaf=100,
        min_samples_treatment=10,
        n_reg=100,
        early_stopping_eval_diff_scale=1,
        evaluationFunction="KL",
        normalization=True,
        honesty=False,
        estimation_sample_size=0.5,
        random_state=None,
    ):

        # Сохраняем все параметры в self.params
        self.params = {
            "control_name": control_name,
            "max_features": max_features,
            "max_depth": max_depth,
            "min_samples_leaf": min_samples_leaf,
            "min_samples_treatment": min_samples_treatment,
            "n_reg": n_reg,
            "early_stopping_eval_diff_scale": early_stopping_eval_diff_scale,
            "evaluationFunction": evaluationFunction,
            "normalization": normalization,
            "honesty": honesty,
            "estimation_sample_size": estimation_sample_size,
            "random_state": random_state,
        }

        # Вызываем конструктор родительского класса
        super().__init__(**self.params)
        self.params["n_estimators"] = 1
        self.ctrl_preds_ = None
        self.trmnt_preds_ = None

    def get_params(self):
        # Возвращаем параметры
        return self.params

    def fit(self, X: pd.DataFrame, y: pd.Series, treatment: pd.Series):
        self.feature_names_ = X.columns.tolist()

        # Вызываем метод fit родительского класса
        with np.errstate(divide="ignore", invalid="ignore"):
            super().fit(
                X=X.values, y=y.values, treatment=treatment.astype("str").values
            )
        return super()

    def predict(self, X: pd.DataFrame):
        # Предсказываем uplift
        with np.errstate(divide="ignore", invalid="ignore"):
            uplift = super().predict(X.values)
        # print(uplift.shape, uplift)
        self.ctrl_preds_ = uplift[:, 0]
        # Вычисляем предсказания для обработанной группы
        self.trmnt_preds_ = uplift[:, 1]

        return uplift[:, 1] - uplift[:, 0]
