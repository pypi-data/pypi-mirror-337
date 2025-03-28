import typing as tp

import numpy as np
import pandas as pd
from sklift.metrics import uplift_by_percentile


class UpliftCalibration:
    """описание идеи работы класс
    1) храним модель и коэфффициенты по бакетам
    2) храним границы бакетов (при деградации переобучим все, с калибровками)
    3) для новых данных предсказания умножаем на коэфф бакета скора клиента
    4) для выборки можно требовать наличие всех фич модели и ни одной лишней
    """

    def __init__(
        self,
        model: tp.Any,
        features: tp.List[str],
        target_col: str,
        treatment_col: str,
        treatment_groups_mapper: tp.Dict[tp.Any, int] = {0: 0, 1: 1},
        bins: int = 10,
    ):
        self._model: tp.Any = model
        self._features: tp.List[str] = features
        self._target_col: str = target_col
        self._treatment_col: str = treatment_col
        self._treatment_groups_mapper: tp.Dict[tp.Any, int] = treatment_groups_mapper
        # self._treatment_groups_mapper_inv: tp.Dict[tp.Any, int] = {
        #     value: key for key, value in treatment_groups_mapper
        # }
        self._bins: int = bins
        self._bucket_coeffs: np.array = None
        self._uplift_borders_left: np.array = None  # desc
        self._uplift_borders_right: np.array = None  # desc

    def fit(self, data: pd.DataFrame):
        """Учим калибровочные коэффициенты на переданной выборке.

        Args:
            data (pd.DataFrame): выборка для подбора калибровочных коэффициентов
        """
        uplift = self._model.predict(data[self._features])
        target = data[self._target_col]
        treatment = data[self._treatment_col].map(self._treatment_groups_mapper)
        uplift_bucket_stats = [
            (np.min(bucket), np.max(bucket), np.mean(bucket))
            for bucket in np.array_split(np.sort(uplift)[::-1], self._bins)
        ]
        self._uplift_borders_left, self._uplift_borders_right, mean_uplift_preds = map(
            list, zip(*uplift_bucket_stats)
        )
        self._uplift_borders_left[-1] = -np.inf
        self._uplift_borders_right[0] = np.inf
        mean_uplift = uplift_by_percentile(target, uplift, treatment, bins=self._bins)[
            "uplift"
        ].values
        self._bucket_coeffs = mean_uplift / mean_uplift_preds

    def _get_coeffs(self, uplift: np.array):
        func1d = lambda num: [
            idx
            for idx in range(self._bins)
            if self._uplift_borders_left[idx] <= num
            and num <= self._uplift_borders_right[idx]
        ][0]
        func1d = np.vectorize(func1d)
        idxs = np.apply_along_axis(func1d, axis=-1, arr=uplift)
        return self._bucket_coeffs[idxs]

    def predict(self, data: pd.DataFrame):
        """Получение скоров для выборки с учетом калибровки.

        Args:
            data (pd.DataFrame): выборка для получения калиброванных скоров
        """
        uplift = self._model.predict(data[self._features])
        calibrated_uplift = self._get_coeffs(uplift) * uplift
        return calibrated_uplift
