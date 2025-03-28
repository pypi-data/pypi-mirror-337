import typing as tp

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from causalml.feature_selection import FilterSelect
from causalml.inference.tree import UpliftRandomForestClassifier
from sklift.models import SoloModel


class FilterRanker:
    """Sorts features using filter-based methods for measuring the feature ability to predict uplift

    Filter means that each feature is processed separately using some procedure
    This procedure depends only on number of feature bins and divergence measure for response rates used for all bins
    This ranker sorts features at one time being able to use only train data

    Args:
        name (string): ranker name
        method (string, ['F', 'LR', 'KL', 'ED', 'Chi']): the feature selection method to be used to rank the features
            'F' for F-test
            'LR' for likelihood ratio test
            'KL', 'ED', 'Chi' for bin-based uplift filter methods, KL divergence, Euclidian distance, Chi-Square repsectively
        bins (int): number of bins to be used for bin-based uplift filter methods
        data (pd.DataFrame): DataFrame containing target, features, and treatment group
        features (1d array-like): list of feature names, that are columns in the data DataFrame
        target_col (string): target column name
        treatment_col (string): treatment column name

    Examples:
        >>> from AUF.feature_selection import FilterRanker
        >>> ranker = FilterRanker(method = "KL", bins = 10)
        >>> ranked_features, ranked_importances = ranker.run(df, features, target_col, treatment_col)

    Returns: None
    """

    def __init__(self, method: str, bins: int, name: str = "__empty_name__"):
        self.name: str = name
        self.method: str = method
        self.bins: int = bins
        self.ranked_features: tp.List[str] = []
        self.ranked_features_scores: tp.List[float] = []

    def run(
        self,
        data: pd.DataFrame,
        features: tp.List[str],
        target_col: str,
        treatment_col: str,
    ) -> tp.List[str]:

        assert "treatment_group_key" not in data.columns
        assert ((data[treatment_col] == 0) | (data[treatment_col] == 1)).all()

        try:
            data["treatment_group_key"] = data[treatment_col].apply(
                lambda x: "control" if x == 0 else "treatment"
            )

            selector = FilterSelect()

            result = selector.filter_D(
                data=data,
                features=features,
                y_name=target_col,
                n_bins=self.bins,
                method=self.method,
                null_impute="mean",  # {'mean', 'median', 'most_frequent', None}
                experiment_group_column="treatment_group_key",
                control_group="control",
            )

        except Exception as e:
            print("Exception was raised:", str(e))
            raise e

        finally:
            data.drop("treatment_group_key", axis=1, inplace=True)

        self.ranked_features = list(result.feature.values)
        self.ranked_features_scores = list(result.score.values)
        return self.ranked_features, self.ranked_features_scores

    def get_ranked_features(self):
        return self.ranked_features

    def get_ranked_features_scores(self):
        return self.ranked_features_scores

    def get_ranker_name(self) -> str:
        return self.name
