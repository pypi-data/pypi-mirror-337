import pickle
import typing as tp
from copy import deepcopy

import pandas as pd

from ..training.gridsearch import ModelResult


class UpliftPipelineInference:
    def __init__(
        self, result: ModelResult, fillna_value: tp.Union[float, tp.Dict[str, float]]
    ):
        self.result = deepcopy(result)
        self.fillna_value = fillna_value

    def save(self, filename: str):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename: str):
        with open(filename, "rb") as f:
            return pickle.load(f)

    def _preprocess(self, data: pd.DataFrame):
        if self.fillna_value is None:
            return
        if isinstance(self.fillna_value, dict):
            for col, value in self.fillna_value:
                data[col] = data[col].fillna(value=value)
        else:
            for col in self.result.features:
                # TODO : process categorical features
                if data[col].dtype != "object":
                    data[col] = data[col].fillna(value=self.fillna_value)

    def _postprocess(self, data: pd.DataFrame):
        if self.fillna_value is None:
            return
        if isinstance(self.fillna_value, dict):
            for col, value in self.fillna_value:
                data.loc[data[col] == value, col] = None
        else:
            for col in self.result.features:
                # TODO : process categorical features
                if data[col].dtype != "object":
                    data.loc[data[col] == self.fillna_value, col] = None

    def infer(self, data: pd.DataFrame):
        self._preprocess(data)
        uplift = self.result.estimator.predict(data[self.result.features])
        if self.result.uplift_prediction_type != "abs":
            trmnt_preds = self.result.estimator.trmnt_preds_
            ctrl_preds = self.result.estimator.ctrl_preds_
            uplift = trmnt_preds / ctrl_preds - 1
        self._postprocess(data)
        return uplift
