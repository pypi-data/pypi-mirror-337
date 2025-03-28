import typing as tp

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from causalml.feature_selection import FilterSelect
from causalml.inference.tree import UpliftRandomForestClassifier
from sklift.models import SoloModel


# TODO : check correctness & test on example samples
class StraightforwardRanker:
    """Sorts features using bootstrapped estimation of uplift from using this feature with all others.

    Idea:
        - train & evaluate model with all features
        - drop any feature from the feature set
        - train & evaluate model without this feature
        - estimate feature importance as median uplift of uplift metric divided by std of it (get it via bootstrap)
        - do it for every feature

    Quality:
        - it is meant to be an uplift metric (qini, uplift@k)
        - it is NOT optimized, it just shows feature importance via bootstrap statistic

    Note:
        - if there are highly correlated features, the method may work poorly for some features
            because information from removed feature will leak from other features into ranking model
        - it only sorts features, doesn't drop them

    """

    def __init__(self, uplift_model: tp.Any):
        self.model = uplift_model
        self.ranked_features: tp.List[str] = []
        self.ranked_features_scores: tp.List[float] = []
        self.name: str = "__empty_name__"

    def _get_feature_gain(
        metric,
        train_data,
        val_data,
        target_col: str,
        treatment_col: str,
        features,
        feature_to_check,
        n_test_repeats=500,
    ):
        import scipy.stats

        x_train, y_train, t_train = (
            train_data[features],
            train_data[target_col],
            train_data[treatment_col],
        )
        x_val, y_val, t_val = (
            val_data[features],
            val_data[target_col],
            val_data[treatment_col],
        )

        self.model.fit(x_train[features], y_train, t_train)
        preds_full = self.model.predict(x_val[current_features + [feature_to_add]])

        self.model.fit(
            x_train[[f for f in features if f != feature_to_check]], y_train, t_train
        )
        preds_without = self.model.predict(
            x_val[[f for f in features if f != feature_to_check]]
        )

        delta_uplifts = [0 for _ in range(n_test_repeats)]

        for i in range(n_test_repeats):
            idxs = np.random.choice(
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
        metric: tp.Callable(),
    ) -> tp.List[str]:
        """Implements stepwise forward algorithm logic"""
        assert train_data.columns == val_data.columns

        features_scores = []  # list of pairs (feature, score when added)

        for f in tqdm(all_features):
            mean, std, feature_score = _get_feature_gain(
                metric,
                train_data,
                val_data,
                target_col,
                treatment_col,
                all_features,
                feature_to_check=f,
                n_test_repeats=1000,
            )

            features_scores.append((f, feature_score))

        features_scores = sorted(features_scores, key=lambda f_score: -f_score[1])
        self.ranked_features = [f for (f, score) in features_scores]
        self.ranked_features_scores = [score for (f, score) in features_scores]
        return self.ranked_features, self.ranked_features_scores

    def get_ranker_name(self) -> str:
        # if self.model_info[0] is SoloModel:
        #     self.name = "SoloModel"
        # elif self.model_info[0] is UpliftRandomForestClassifier:
        #     self.name = "UpliftRandomForestClassifier"
        # else:
        #     self.name = "propensity_model"
        return self.name
