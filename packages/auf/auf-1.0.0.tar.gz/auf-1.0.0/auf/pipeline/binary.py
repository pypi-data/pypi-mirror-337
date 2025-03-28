import copy
import itertools
import os
import typing as tp
from collections.abc import Callable
from datetime import datetime
from functools import partial

import matplotlib as mpl
import matplotlib.pyplot as plt
import mlflow
import numpy as np
import pandas as pd
import seaborn as sns
from catboost import CatBoostClassifier
from causalml.inference.tree import UpliftRandomForestClassifier
from IPython.display import display, display_html
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklift.metrics import qini_auc_score, uplift_at_k, uplift_by_percentile
from sklift.models import SoloModel, TwoModels
from sklift.viz import plot_qini_curve, plot_uplift_curve

from ..constants import BOOTSTRAP_REPEATS, METRICS, RANDOM_STATE
from ..data.checks import (
    check_bernoulli_dependence,
    check_bernoulli_equal_means,
    check_correlations,
    check_leaks,
    check_leaks_v2,
    check_nans,
    check_too_less_unique_value,
    check_train_val_test_split,
    process_too_much_categories,
)
from ..data.preprocessing import Preprocessor
from ..data.split import train_val_test_split
from ..feature_rankers import (
    FilterRanker,
    ImportanceRanker,
    PermutationRanker,
    StepwiseRanker,
)
from ..metrics import overfit_abs, overfit_metric_minus_metric_delta
from ..ml_flow.ml_flow import (
    AUFModel,
    generate_run,
    get_or_create_experiment,
    save_dataframe_html,
    save_figure,
    save_json,
    save_metrics,
    save_model,
    save_params_dict,
    save_pdf_figures,
)
from ..models import AufRandomForestClassifier, AufTreeClassifier, AufXLearner
from ..plots import (
    plot_portrait_tree,
    plot_uplift_by_feature_bins,
    plot_uplift_by_percentile,
)
from ..training.fitting import fit_model, generate_model_from_classes, models_fast_fit
from ..training.gridsearch import ModelResult, OptuneUpliftDefault
# from .preprocess import Preprocessor


class UpliftPipeline:
    """Automatic uplift modeling pipeline

    Attributes:
        _df (pd.DataFrame): loaded sample
        _feature_cols (1d array-like): list of loaded sample features
        _base_cols_mapper (dict): mapping of unified column names to custom names
            Default is {"id": "id", "treatment": "treatment", "target": "target", "segm": "segm"}
        _treatment_groups_mapper (dict): mapping of unified treatment group names to custom names.
            Default is {0: 0, 1: 1}

        _removed_features (dict): dictionary of deleted features, where the keys are the reasons for removing
        _feature_cols_treatment_leaks_roc_aucs (1d array-like): feature names and ROC-AUCs of leaking on treatment features
        _feature_cols_treatment_roc_aucs (1d array-like): feature name and ROC-AUC with treatment for each feature

        _ranked_candidates (dict): features ranked by importance using different methods

        _train_results (dict): dictionary of models where keys are model classes and values are traindes models

    Methods:
        load_sample
             this method has automatic checks for column names, target & treatment values,
             also it checks that take rates in control & treatment groups differ and that
             train/val/test split is made such that sample sizes are not less than allowed
        preselect_features_candidates
            save a long-list of features which have potential benefit
        check_feature_values
            simple check for ratio of missed values and number in unique values for each feature
        check_treatment_leaks
            check leak on target or treatment for each feature using small catboost model feature importances
            and get top leaking features stats
        check_correlated_features
            filter out features with pairwise absolute correlation not exceeding the specified level
        show_selected_features_stat
            get number of all features and also separately categorical and numerical ones
        show_removed_features_with_reasons
            get stats on removed features and reasond for removing

    Examples:
        >>> from AUF.pipeline import UpliftPipeline
        >>> pipeline = UpliftPipeline()
        >>> base_cols_mapper = {
                'id': 'client_pin',
                'treatment': 'treatment',
                'target': 'deal',
                'segm': 'segm',
                'date': None
            }
        >>> df = pd.read_csv(filename)
        >>> feature_cols = df.columns[5:]
        >>> pipeline.load_sample(df, base_cols_mapper, feature_cols)
        >>> feature_checks_thresholds = {}
        >>> pipeline.check_features(feature_checks_thresholds)

    """

    _base_cols = ["id", "treatment", "target", "segm"]

    def __init__(
        self,
        print_doc: bool = True,
        task_name_mlflow: str = None,
        run_id: str = None,
        run_name: str = None,
        run_description: str = None,
    ):
        self._df: pd.DataFrame = None
        self._feature_cols: tp.List[str] = None
        self._base_cols_mapper: tp.Dict[str, str] = None
        self._treatment_groups_mapper: tp.Dict[tp.Any, int] = None

        self._experiment_name = task_name_mlflow
        self._experiment_id = get_or_create_experiment(self._experiment_name)
        self._run_id = run_id
        self._run_name = (
            run_name
            if run_name is not None
            else datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        self._run_description = run_description

        self._removed_features: tp.Dict[str, str] = {}
        self._feature_cols_treatment_leaks_roc_aucs: tp.List[str] = None
        self._feature_cols_treatment_roc_aucs: tp.List[tp.Tuple[str, float]] = None

        self._ranked_candidates: tp.Dict[str, tp.List[str]] = None

        self._train_metric: tp.Callable[[np.array, np.array, np.array], float] = None
        self._train_results: tp.Dict[tp.Any, tp.Dict[str, tp.List[ModelResult]]] = (
            dict()
        )

        self._use_default_run: bool = False

        if print_doc:
            print(self.__doc__)

    def _check_base_column_names(self, df, base_cols_mapper):
        for col in self._base_cols:

            if col not in base_cols_mapper:
                raise AssertionError(
                    f"Specify None or value for base_cols_mapper['{col}']"
                )

            if base_cols_mapper[col] is None:
                if col in ["id", "treatment", "target"]:
                    raise AssertionError(
                        f"Value of base_cols_mapper['{col}'] must not be None"
                    )
                continue

            if base_cols_mapper[col] not in df.columns:
                raise AssertionError(
                    f"Value of base_cols_mapper['{col}'] must be a dataframe column"
                )

        self._base_cols_mapper = base_cols_mapper

    def _check_base_column_values(self, df, treatment_groups_mapper):
        id_col = self._base_cols_mapper["id"]  # usually int or str
        target_col = self._base_cols_mapper["target"]
        treatment_col = self._base_cols_mapper["treatment"]
        segm_col = self._base_cols_mapper["segm"]

        for base_col, col in self._base_cols_mapper.items():
            if col is not None:
                if df[col].isna().any():
                    raise AssertionError(
                        f"'{col}' column must not contain missed values"
                    )

        if set(treatment_groups_mapper.keys()) != set(np.unique(df[treatment_col])):
            raise AssertionError(
                f"'treatment_groups_mapper' must contain all treatment groups as keys and only"
            )

        if set(treatment_groups_mapper.values()) != set([0, 1]):
            raise AssertionError(
                f"'treatment_groups_mapper' must contain both 0 and 1 and only"
            )

        self._treatment_groups_mapper = treatment_groups_mapper

        if set(np.unique(df[target_col])) != set([0, 1]):
            raise AssertionError(
                f"'{target_col}' column must contain both 0 and 1 and only"
            )

        if segm_col is not None and set(np.unique(df[segm_col])) != {
            "train",
            "val",
            "test",
        }:
            raise AssertionError(
                f"'{segm_col}' column must contain all of ['train', 'val', 'test']"
            )

        # TODO : checks for id_col and date_col if really need it

    def _check_take_rate_differ(self, df):
        """Here we assume that there are only 2 types of treatment (0 = control group, 1 = treatment group)"""
        target_col = self._base_cols_mapper["target"]
        treatment_col = self._base_cols_mapper["treatment"]

        treatment_flag = df[treatment_col].map(self._treatment_groups_mapper)
        target_treatment = df.loc[treatment_flag == 1, target_col]
        target_control = df.loc[treatment_flag == 0, target_col]
        result = check_bernoulli_equal_means(
            target_treatment, target_control, alpha=0.05
        )
        print(
            "Difference in target rates for treatment and control groups:\n"
            f"{'':<4}pvalue = {result['pvalue']:.3f}\n"
            f"{'':<4}treatment target rate : {target_treatment.mean():.3f}\n"
            f"{'':<4}control target rate   : {target_control.mean():.3f}",
            flush=True,
        )

        save_dataframe_html(
            pd.DataFrame(
                {
                    "equals": [result["equals"]],
                    "pvalue": round(result["pvalue"], 3),
                    "treatment target rate": round(target_treatment.mean(), 3),
                    "control target rate": round(target_control.mean(), 3),
                }
            ),
            "3_take_rate_diff",
            "1_data",
            self._run_id,
        )

        if result["equals"]:
            error_msg = "Target rates in control and treatment groups must have statistically significant difference for uplift modeling"
            print("\033[91m" + error_msg + "\033[0m")
            # raise AssertionError(error_msg)

    def show_take_rate_info(self):
        """Show tables with take rate statistics

        1) mean take rate in both treatment and control groups
        2) number of observations in each treatment group and target group (pandas.crosstab)
        3) ratio in % of whole sample size in each treatment group and target group (pandas.crosstab)
        """
        target_col = self._base_cols_mapper["target"]
        treatment_col = self._base_cols_mapper["treatment"]
        segm_col = self._base_cols_mapper["segm"]

        info = self._df.groupby([segm_col, treatment_col])[target_col].agg(
            ["mean", "sum", "count"]
        )
        info.columns = ["target_mean", "target_sum", "target_count"]
        save_dataframe_html(info, "3_take_rate_info", "1_data", self._run_id)
        display(info)

    def _check_train_val_test_split(self, df):
        segm_col = self._base_cols_mapper["segm"]
        target_col = self._base_cols_mapper["target"]
        treatment_col = self._base_cols_mapper["treatment"]
        treatment_flag = df[treatment_col].map(self._treatment_groups_mapper)
        check_train_val_test_split(
            df, segm_col, target_col, treatment_col, self._treatment_groups_mapper
        )

    def _default_train_val_test_split(self, df):
        df_train_idx, df_val_idx, df_test_idx = train_val_test_split(
            df,
            size_ratios=[0.6, 0.2, 0, 2],
            stratify_cols=[
                self._base_cols_mapper["target"],
                self._base_cols_mapper["treatment"],
            ],
        )

        df["segm"] = "train"
        self._base_cols_mapper["segm"] = "segm"
        df.loc[df.index.isin(df_val_idx), "segm"] = "val"
        df.loc[df.index.isin(df_test_idx), "segm"] = "test"

    def _get_available_features(self):
        removed_features = list(itertools.chain(*self._removed_features.values()))
        removed_features += list(
            itertools.chain(
                self._base_cols_mapper.keys(), self._base_cols_mapper.values()
            )
        )
        return [f for f in self._feature_cols if f not in removed_features]

    def load_sample(
        self,
        df: pd.DataFrame,
        base_cols_mapper: tp.Dict[str, str] = {
            "id": "id",
            "treatment": "treatment",
            "target": "target",
            "segm": "segm",
        },
        treatment_groups_mapper: tp.Dict[str, str] = {0: 0, 1: 1},
    ):
        """Save sample dataframe, check target/treatment per full sample and train/val/test segments

        Args:
            df (pd.DataFrame): sample
            base_cols_mapper (tp.Dict[str, str], optional): mapping of unified column names to custom names
                Default is {"id": "id", "treatment": "treatment", "target": "target", "segm": "segm"}
            treatment_groups_mapper (tp.Dict[str, str], optional): mapping of unified treatment group names to custom names.
                Default is {0: 0, 1: 1}

        Returns: None

        Examples:
            from AUF.pipeline import UpliftPipeline
            pipeline = UpliftPipeline()
            base_cols_mapper = {
                "id": "id",
                "treatment": "treatment",
                "target": "target",
                "segm": "segm"
            }

            treatment_groups_mapper = {0: 0, 1: 1}

            df = pd.read_csv(filename)

            pipeline.load_sample(
                df, base_cols_mapper, treatment_groups_mapper
                )
        """
        assert isinstance(df, pd.DataFrame), "Parameter 'df' must be a pandas dataframe"
        self._run_id = (
            self._run_id
            if self._run_id is not None
            else generate_run(
                self._experiment_name,
                self._experiment_id,
                self._run_name,
                self._run_description,
            )
        )

        # TODO : это нужно, если есть дефолтный аргумент?
        if base_cols_mapper is None:
            base_cols_mapper = {
                "id": "id",
                "treatment": "treatment",
                "target": "target",
                "segm": "segm",
            }

        # TODO : это нужно, если есть дефолтный аргумент?
        if treatment_groups_mapper is None:
            treatment_groups_mapper = {0: 0, 1: 1}

        mappers = {
            "base_cols_mapper": base_cols_mapper,
            "treatment_groups_mapper": treatment_groups_mapper,
        }
        save_json(mappers, "1_mappings", "1_data", self._run_id)

        self._check_base_column_names(df, base_cols_mapper)
        self._check_base_column_values(df, treatment_groups_mapper)
        self._check_take_rate_differ(df)

        if base_cols_mapper["segm"] is not None:
            self._check_train_val_test_split(df)
        else:
            self._default_train_val_test_split(df)

        self._df = df
        self._feature_cols = df.columns.tolist()

        self._feature_cols = self._get_available_features()
        self._removed_features["all values missed"] = [
            f for f in self._feature_cols if self._df[f].isna().all()
        ]
        self._feature_cols = self._get_available_features()
        self._removed_features["only 1 unique value"] = [
            f for f in self._feature_cols if self._df[f].nunique() == 1
        ]
        self._feature_cols = self._get_available_features()

        for f in self._feature_cols:
            if self._df[f].dtype == "object":
                self._df[f] = self._df[f].astype(str)

        # remove categorical features for MVP
        # self._removed_features["categorical (for MVP)"] = [
        #     f for f in self._feature_cols if self._df[f].dtype == "object"
        # ]

        print("\nSample was succesfully loaded!")
        self.show_take_rate_info()

    def show_selected_features_stat(self):
        """Shows number of numerical and categorical features selected for modeling at the moment"""
        selected_features = self._get_available_features()
        cat_feats = [f for f in selected_features if self._df[f].dtype == "object"]
        num_feats = [f for f in selected_features if f not in cat_feats]
        print(f"Currently selected for modeling: {len(selected_features)}")
        print(f"{'':<4}{len(num_feats):5} numerical features")
        print(f"{'':<4}{len(cat_feats):5} categorical features")

    def preselect_features_candidates(
        self, n_features: int = 300, method: str = "filter", early_stopping: int = 5
    ):
        """Saves a long-list of features which have potential benefit

        Note:
            - feature preselction needs to be very fast and simple
            - features that have potential for the task may be rarely filled or be categorical
            - save them in any case and work with only well filled numerical features here

        Args:
            method (str, optional): method for feature selection (by importance of SoloModel with
                CatBoostClassifier as base model of bin-based filter method). Default is "filter"
            n_features (int, optional): number of feature to use in further pipeline steps. Default is 200

        Raises:
            ValueError: if method is not in ["importance", "filter"]

        Returns: None
        """

        target_col = self._base_cols_mapper["target"]
        treatment_col = self._base_cols_mapper["treatment"]

        treatment_map = self._treatment_groups_mapper
        treatment_map_inv = {v: k for k, v in self._treatment_groups_mapper.items()}

        self._df[treatment_col] = self._df[treatment_col].map(treatment_map)

        try:

            # repeated run of preselection needs to be independent
            if "preselection" in self._removed_features:
                del self._removed_features["preselection"]

            ctb_params = {
                "iterations": 200,
                "max_depth": 4,
                "learning_rate": 0.05,
                "cat_features": [
                    f
                    for f in self._get_available_features()
                    if self._df[f].dtype == "object"
                ],
            }

            model_params = {
                "estimator": CatBoostClassifier(
                    **ctb_params, silent=True, random_state=8
                ),
                "method": "dummy",
            }

            if method == "importance":

                ranker = ImportanceRanker(SoloModel, model_params, "at_once")
                ranked_features, ranked_importances = ranker.run(
                    self._df, self._get_available_features(), target_col, treatment_col
                )

                # give the last chance to show their importance to the features with zero importance
                # zero_importance_features = [
                #     f for f, imp in zip(ranked_features, ranked_importances) if not imp > 0
                # ]

                # Importance ranker with S-learner as a base model returns 'tratment' feature importance too
                # => we need manually remove it
                # assert "treatment" not in zero_importance_features
                # assert treatment_col not in zero_importance_features

                zero_importance_features = [
                    f
                    for f, imp in zip(ranked_features, ranked_importances)
                    if not imp > 0 and f not in ["treatment", treatment_col]
                ]

                ctb_params = {
                    "iterations": 200,
                    "max_depth": 4,
                    "learning_rate": 0.05,
                    "cat_features": [
                        f
                        for f in zero_importance_features
                        if self._df[f].dtype == "object"
                    ],
                }

                model_params = {
                    "estimator": CatBoostClassifier(
                        **ctb_params, silent=True, random_state=8
                    ),
                    "method": "dummy",
                }

                ranker = ImportanceRanker(SoloModel, model_params, "at_once")
                zero_ranked_features, zero_ranked_importances = ranker.run(
                    self._df, zero_importance_features, target_col, treatment_col
                )

                # change the scores & sort for features with zero importance
                ranked_features, ranked_importances = map(
                    list,
                    zip(
                        *[
                            (f, imp)
                            for f, imp in zip(ranked_features, ranked_importances)
                            if imp > 0
                        ]
                    ),
                )
                ranked_features += zero_ranked_features
                ranked_importances += zero_ranked_importances

            elif method == "filter":
                # there are 2 properties of the feature:
                #   1) being numerical / categorical and
                #   2) being filled enough (e.g. 10+% values aren't missed)
                #
                # we have 4 groups which we need to process very fast to get rid of the features with the least potential
                #   1) filled enough numerical features can be ranked with bin-based filter method
                #   2) filled enough categorical features can be ranked with boosting model
                #   3) poorly filled both numerical and categorical features may have potential that is not easy to check especially for an uplift task
                #       - the easiest way is to use them all, but there may be 30+% of features with 90+% missing values
                #       - statistical test for dependence between missing value and uplift (conversion difference)
                #       - fit a boosing model of medium size and select features with the greatest importance
                #
                # idea :
                #   - filter filled enough numerical features
                #   - use boosting model feature importance score to tank others
                #   - select n_features / 2 top features from both ratings

                # consider only numerical features with less than 95% of missed values
                filled_num_features = [
                    f
                    for f in self._get_available_features()
                    if self._df[f].dtype != "object" and self._df[f].isna().mean() < 0.9
                ]

                ranker = FilterRanker(method="KL", bins=10)
                ranked_features, ranked_importances = ranker.run(
                    self._df, filled_num_features, target_col, treatment_col
                )

                other_features = [
                    f
                    for f in self._get_available_features()
                    if f not in filled_num_features
                ]
                ranker = ImportanceRanker(SoloModel, model_params, "at_once")
                other_ranked_features, other_ranked_importances = ranker.run(
                    self._df, other_features, target_col, treatment_col
                )

                ranked_features = (
                    ranked_features[: n_features // 2]
                    + other_ranked_features[: n_features - n_features // 2]
                    + ranked_features[n_features // 2 :]
                    + other_ranked_features[n_features - n_features // 2 :]
                )

            else:
                raise ValueError(
                    f"'method' parameter must be either 'importance' or 'filter', but is {method}"
                )
        finally:
            self._df[treatment_col] = self._df[treatment_col].map(treatment_map_inv)

        self._removed_features["preselection"] = ranked_features[n_features:].copy()

        save_json(
            ranked_features[n_features:],
            "2_preselect_feature_candidates",
            "2_feature_selection",
            self._run_id,
        )

    def check_feature_values(
        self,
        max_nan_ratio: float = 0.95,
        max_categories_count: int = 20,
    ):
        """Simple check the percentage of missing values and the number in unique values for each feature

        Args:
            max_nan_ratio (float, optional): maximum allowed percentage of missed values. Default is 0.95
            max_categories_count (int, optional): maximum allowed number of unique values for
                categorical features. Default is 20

        Returns: None
        """
        if not self._use_default_run:
            print("Simple feature values checks.")

        all_feature_cols = self._get_available_features()

        if not self._use_default_run:
            print(f"{len(all_feature_cols):7} features in total")

        filled_feature = check_nans(
            self._df, all_feature_cols, max_nan_ratio=max_nan_ratio
        )
        remove_features = [col for col in all_feature_cols if col not in filled_feature]
        self._removed_features["too much nans"] = remove_features

        if not self._use_default_run:
            print(
                f"{len(filled_feature):7} features with less than {int(100 * max_nan_ratio)}% nans"
            )

        process_too_much_categories(
            self._df, all_feature_cols, max_categories_count=max_categories_count
        )

        if not self._use_default_run:
            print("\nProcess categorical features with too much unique values.")
            print(
                f"{'':<4}all they have now no more than {max_categories_count} categories."
            )

    def check_treatment_leaks(
        self,
        max_val_roc_auc_treatment: float = 0.65,  # check features together with small model
        early_stopping: int = None,  # stop if remaining features don't give leak together
        check_only_available_features: bool = True,
    ):
        """Check leak on treatment for each feature using small catboost model feature importances

        Args:
            max_val_roc_auc_treatment (float, optional): maximum allowable ROC-AUC score for predicting
                treatment by feature on validation set. Default is 0.65
            check_only_available_features (bool): whether to use only filtered features. Default is True

        Returns: None
        """
        if not self._use_default_run:
            print("Check feature leaks for treatment column.")

        if check_only_available_features:
            all_feature_cols = self._get_available_features()
        else:
            all_feature_cols = self._feature_cols

        if not self._use_default_run:
            print(f"{len(all_feature_cols):7} features in total")

        if not self._use_default_run:
            print("\nAnalyze potential leaks of treatment")

        treatment_leaks_roc_aucs, treatment_not_leaks, treatment_roc_aucs = (
            check_leaks_v2(
                self._df,
                self._base_cols_mapper,
                all_feature_cols,
                col_to_check="treatment",
                alpha=0.05,
                max_val_roc_auc=max_val_roc_auc_treatment,
                early_stopping=early_stopping,
            )
        )

        treatment_leaks = pd.DataFrame(
            treatment_leaks_roc_aucs, columns=["feature", "roc_auc"]
        )
        save_dataframe_html(
            treatment_leaks, "1_treatment_leaks", "2_feature_selection", self._run_id
        )

        self._removed_features["treatment leaks"] = [
            f for f, roc_auc in treatment_leaks_roc_aucs
        ]

        if not self._use_default_run:
            if len(treatment_leaks_roc_aucs) > 0:
                print(
                    f"TOP leaking features ({len(treatment_leaks_roc_aucs)} found, but at most 5 are printed):"
                )
                for f, roc_auc in treatment_leaks_roc_aucs[:5]:
                    print(f"   {f:20} --> ROC-AUC = {roc_auc:.3f}")
            else:
                print("No leaking features were detected.")

        self._feature_cols_treatment_leaks_roc_aucs = treatment_leaks_roc_aucs.copy()
        self._feature_cols_treatment_roc_aucs = treatment_roc_aucs.copy()

    def check_correlated_features(
        self, max_abs_corr: float = 0.9, check_only_available_features: bool = True
    ):
        """Filter out features with pairwise absolute correlation not exceeding the specified threshold

        Args:
            max_abs_corr (float): maximum allowed level of features correlation. Default is 0.9
            check_only_available_features (bool): whether to use only filtered features. Default is True

        Returns: None
        """
        if check_only_available_features:
            too_correlated, clean_feature_cols = check_correlations(
                self._df, self._get_available_features(), max_abs_corr=max_abs_corr
            )
        else:
            too_correlated, clean_feature_cols = check_correlations(
                self._df, self._feature_cols, max_abs_corr=max_abs_corr
            )

        remove_features = [g for f, g in too_correlated]
        save_json(
            remove_features,
            "3_check_correlated_features",
            "2_feature_selection",
            self._run_id,
        )
        self._removed_features["too correlated"] = remove_features.copy()

    def show_removed_features_with_reasons(self):
        """Print number of features which should be removed by some reason"""
        print("Number of features removed for each reason:")
        for reason, removed_features in self._removed_features.items():
            print(f"{'':<4}{len(removed_features):5} : {reason}")

        save_json(
            self._removed_features,
            "4_deleted_features_with_reason",
            "2_feature_selection",
            self._run_id,
        )

    def get_removed_features_by_reason(self, reason: str):
        """Return features which should be removed by some reason"""
        return self._removed_features[reason]

    def plot_treatment_leaks(self, top_k: int = None, features: tp.List[str] = None):
        """Plot probability density function by treatment group for each feature to analyze treament leak.

        Plot distributions for features with top_k highest ROC-AUC in predicting treatment
        Distributions are displayed for all treatment groups for every of selected features
        """

        assert not (
            top_k is None and features is None
        ), "Specify only one set of features for analyzing"
        assert not (
            top_k is not None and features is not None
        ), "Specify only one set of features for analyzing"

        if features is not None:
            for f in features:
                assert (
                    f in self._feature_cols
                ), f"features to remove must be in feature list, but '{f}' isn't"

        features_roc_aucs = self._feature_cols_treatment_roc_aucs

        if features is not None:

            features_roc_aucs_copy = features_roc_aucs.copy()
            features_roc_aucs = []
            for col in features:
                for f, roc_auc in features_roc_aucs_copy:
                    if f == col:
                        features_roc_aucs.append((col, roc_auc))

                if not features_roc_aucs or features_roc_aucs[-1][0] != col:
                    features_roc_aucs.append((col, None))

        else:
            features_roc_aucs = features_roc_aucs[:top_k]

        n_rows, n_cols = (len(features_roc_aucs) + 2) // 3, min(
            len(features_roc_aucs), 3
        )
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 4, n_rows * 4))

        # plt.set_cmap("Reds")

        for idx, (feature, roc_auc) in enumerate(features_roc_aucs):
            plt.subplot(n_rows, n_cols, 1 + idx)

            values = self._df.loc[~self._df[feature].isna(), feature]
            q01, q99 = np.quantile(values, q=[0.01, 0.99])

            mask = (q01 < self._df[feature]) & (self._df[feature] < q99)
            sns.kdeplot(
                data=self._df.loc[
                    mask, [feature, self._base_cols_mapper["treatment"]]
                ],  # col_to_check]],
                x=feature,
                hue=self._base_cols_mapper["treatment"],  # col_to_check,
                ax=plt.gca(),
                # palette=sns.light_palette('#ef0000', as_cmap=True),
                # palette=sns.color_palette("Reds", 4, as_cmap=True),
                # color="red",
                palette=list(plt.cm.Reds(np.linspace(0, 1, 20))[[6, 14]]),
                common_norm=False,
            )

            if roc_auc is not None:
                plt.title(
                    f"Validation ROC-AUC\nquantile(95%) = {roc_auc:.3f}", fontsize=14
                )
            else:
                plt.title(
                    f"Feature wasn't considered\nas leak of treatment",
                    fontsize=14,
                )

            plt.xlabel(feature, fontsize=14)
            plt.ylabel("Density", fontsize=14)

        plt.tight_layout()
        save_figure(fig, "1_treatment_leaks", "2_feature_selection", self._run_id)
        plt.show()

    def remove_features(self, features: tp.List[str]):
        """Remove features from the list of used features for a custom reason

        Args:
            features (tp.List[str]): list of features to remove

        Returns: None
        """
        for f in features:
            assert (
                f in self._feature_cols
            ), f"features to remove must be in feature list, but '{f}' isn't"

        if "custom blacklist" not in self._removed_features:
            self._removed_features["custom blacklist"] = []

        self._removed_features["custom blacklist"].extend(features)

    def rank_features_candidates(
        self,
        ranker_types: tp.List[str] = None,
        opt_metric: tp.Callable[
            [np.array, np.array, np.array], np.array
        ] = qini_auc_score,
    ):
        """Run all feature selection methods to rank features from the long list by their importance"""

        if ranker_types is None:
            ranker_types = ["filter", "importance"]

        available_rankers = ["filter", "importance", "permutation", "stepwise"]
        assert all(x in available_rankers for x in ranker_types)

        segm_col = self._base_cols_mapper["segm"]
        target_col = self._base_cols_mapper["target"]
        treatment_col = self._base_cols_mapper["treatment"]

        treatment_map = self._treatment_groups_mapper
        treatment_map_inv = {v: k for k, v in self._treatment_groups_mapper.items()}

        self._df[treatment_col] = self._df[treatment_col].map(treatment_map)

        catboost_params = {
            "iterations": 200,
            "max_depth": 4,
            "learning_rate": 0.05,
            "cat_features": [
                f
                for f in self._get_available_features()
                if self._df[f].dtype == "object"
            ],
            "random_seed": 8,
            "silent": True,
        }

        s_learner_params = {
            "estimator": CatBoostClassifier(**catboost_params),
            "method": "dummy",
        }

        self._ranked_candidates = dict()

        try:

            if "filter" in ranker_types:
                # TODO : add categorical features for filter ranker
                ranker = FilterRanker(method="KL", bins=10)

                ranked_features, ranked_importances = ranker.run(
                    self._df, self._get_available_features(), target_col, treatment_col
                )

                self._ranked_candidates["filter"] = ranked_features.copy()

            if "importance" in ranker_types:
                ranker = ImportanceRanker(
                    model_class=SoloModel,
                    model_params=s_learner_params,
                    sorting_mode="iterative",
                )

                ranked_features, ranked_importances = ranker.run(
                    self._df.loc[self._df[segm_col] != "test"],
                    self._get_available_features(),
                    target_col,
                    treatment_col,
                )

                self._ranked_candidates["importance"] = ranked_features.copy()

            if "permutation" in ranker_types:
                rng = np.random.RandomState(seed=RANDOM_STATE)
                ranker = PermutationRanker(
                    SoloModel, s_learner_params, rng, BOOTSTRAP_REPEATS
                )

                ranked_features, ranked_importances = ranker.run(
                    self._df.loc[self._df[segm_col] == "train"],
                    self._df.loc[self._df[segm_col] == "val"],
                    self._get_available_features(),
                    target_col,
                    treatment_col,
                    metric=opt_metric,
                )

                self._ranked_candidates["permutation"] = ranked_features.copy()

            if "stepwise" in ranker_types:
                rng = np.random.RandomState(seed=RANDOM_STATE)
                ranker = StepwiseRanker(
                    SoloModel, s_learner_params, rng, BOOTSTRAP_REPEATS
                )

                ranked_features, ranked_importances = ranker.run(
                    self._df.loc[self._df[segm_col] == "train"],
                    self._df.loc[self._df[segm_col] == "val"],
                    self._get_available_features(),
                    target_col,
                    treatment_col,
                    metric=opt_metric,
                )

                self._ranked_candidates["stepwise"] = ranked_features.copy()

            # TODO : self._ranked_candidates["straightforward"]

            save_json(
                self._ranked_candidates,
                "1_ranked_features_candidates",
                "3_feature_ranking",
                self._run_id,
            )

            all_candidates = list()
            for cands in self._ranked_candidates.values():
                all_candidates.extend(cands)

            # Можно вынести куда-нибудь ---------------------------------------------------------------------------------------------

            TOP_TO_COMPARE = 20
            top_ranked_candidates = pd.DataFrame(self._ranked_candidates).head(
                TOP_TO_COMPARE
            )

            def bold_common_values(val, common_values):
                if val in common_values:
                    return f"<b>{val}</b>"
                return str(val)

            ranked_candidates_names = top_ranked_candidates.columns
            common_candidates = set(top_ranked_candidates[ranked_candidates_names[0]])
            for candidate in ranked_candidates_names[1:]:
                common_candidates.intersection_update(top_ranked_candidates[candidate])

            html_styled_top = top_ranked_candidates.applymap(
                lambda x: bold_common_values(x, common_candidates)
            )

            save_dataframe_html(
                html_styled_top,
                "3_rankers_top_feats_comparison",
                "3_feature_ranking",
                self._run_id,
            )

            # Можно вынести куда-нибудь ---------------------------------------------------------------------------------------------

        except Exception as e:
            print("Exception was raised:", str(e))
            self._ranked_candidates = dict()
            raise e

        finally:
            self._df[treatment_col] = self._df[treatment_col].map(treatment_map_inv)

    def train_models(
        self,
        classes: tp.List[str] = None,
        features: tp.List[str] = None,
        models: tp.List[tp.Tuple[tp.Any, str]] = None,
        feature_nums: tp.List[int] = [20, 35, 50, 100],
        use_default_params: bool = True,
        metric: object = None,
        timeout_estimator: int = 60 * 3,
        search_class=OptuneUpliftDefault,
        overfit_metric: object = overfit_metric_minus_metric_delta,
    ):
        """Train the specified models on the given classes and features
           Save results in attribute self._train_results

        Args:
            classes (1d array-like): a list of classes for which the models will be trained. If provided,
                the models parameter is ignored
            features (1d array-like): a list of features to be used for training the models, which should be
                sorted by importance if feature_nums is used. If not provided, features from
                self._ranked_candidates will be used
            models (1d array-like): a list of models to be trained with their names. If not None, the
                parameters param_grids and use_default_params are ignored
            feature_nums (1d array-like): the number of features to be used in the models
            use_default_params (bool): if True, default parameters are used for all models
                If False, Optuna is used. Default is True
            metric: optimization function for optuna class
            timeout_estimator (int): time for fitting one estimator
            search_class: class for estimators best params search
            overfit_metric: if not none, optuna class optimization overfit_metric(metric_valid, metric_train)
            (deprecated) uplift_type: type of uplift, if abs use TR_1-TR2 , if rel use TR_1/TR_2 -1

        Notes:
            The method may raise errors if the lengths of the lists models, feature_nums,
                and param_grids do not match when provided

        Returns: None

        Examples:

            # no need to import classes
            pipeline.train_models(
                classes=["CatBoostClassifier", "SoloModel", "TwoModels"],
                feature_nums=[5, 10, 15, 20, 25, 30, 50,]
            )
        """
        assert not (
            classes is None and models is None
        ), "Только один из аргументов models и classes должен быть None"
        assert not (
            classes is not None and models is not None
        ), "Только один из аргументов models и classes должен быть None"
        assert (
            use_default_params is False or metric is not None
        ), "Для подбора лучших гиперпараметров нужно указать оптимизируемую метрику"

        assert not (
            features is None and self._ranked_candidates is None
        ), "parameter features is None, specify it or call rank_features_candidates() method"

        cls_map = {
            "CatBoostClassifier": CatBoostClassifier,
            "SoloModel": SoloModel,
            "TwoModels": TwoModels,
            "AufRandomForestClassifier": AufRandomForestClassifier,
            "AufTreeClassifier": AufTreeClassifier,
            # TODO : add our uplift models
            "AufXLearner": AufXLearner,
        }

        if classes is not None:
            for cls_name in classes:
                if cls_name not in cls_map:
                    raise ValueError(
                        "Check correctness of passed class names: "
                        + f"{cls_name} not found"
                    )
            classes = [cls_map[cls_name] for cls_name in classes]

        self._train_metric = metric

        model_info = dict()  # make method calls independent

        segm_col = self._base_cols_mapper["segm"]
        target_col = self._base_cols_mapper["target"]
        treatment_col = self._base_cols_mapper["treatment"]

        treatment_map = self._treatment_groups_mapper
        treatment_map_inv = {v: k for k, v in self._treatment_groups_mapper.items()}
        self._df[treatment_col] = self._df[treatment_col].map(treatment_map)

        try:
            df_train_mask = self._df[segm_col] == "train"
            df_val_mask = self._df[segm_col] == "val"
            df_test_mask = self._df[segm_col] == "test"

            if features is None:
                features = self._ranked_candidates
            else:
                features = {"custom_features": features}

            feature_nums = sorted(feature_nums)
            feature_nums = [
                x for x in feature_nums if x <= len(self._get_available_features())
            ]
            if feature_nums[-1] != len(self._get_available_features()):
                feature_nums.append(len(self._get_available_features()))

            if models is not None:
                for mc in models:
                    model_result = models_fast_fit(
                        mc[0],
                        self._df.loc[df_train_mask],
                        self._df.loc[df_val_mask],
                        self._df.loc[df_test_mask],
                        features,
                        target_col,
                        treatment_col,
                        feature_nums,
                    )
                    model_info[mc[1]] = model_result
            else:
                for cls_model in classes:
                    print(f"{cls_model.__name__} training started")
                    model_result = generate_model_from_classes(
                        cls_model,
                        self._df.loc[df_train_mask],
                        self._df.loc[df_val_mask],
                        self._df.loc[df_test_mask],
                        features,
                        target_col,
                        treatment_col,
                        feature_nums,
                        timeout_estimator,
                        metric,
                        use_default_params,
                        search_class=search_class,
                        overfit_metric=overfit_metric,
                    )
                    model_info[cls_model.__name__] = model_result
                    print(f"{cls_model.__name__} successfully trained\n")

        except Exception as e:
            print("Exception was raised:", str(e))
            self._train_results = dict()
            raise e

        finally:
            self._df[treatment_col] = self._df[treatment_col].map(treatment_map_inv)

        self._train_results = model_info

    def _get_median_test_metrics(
        self, metric: tp.Callable[[np.array, np.array, np.array], float]
    ):
        """Works only with uplift models that have method predict, but not predict_proba"""

        segm_col = self._base_cols_mapper["segm"]
        target_col = self._base_cols_mapper["target"]
        treatment_col = self._base_cols_mapper["treatment"]

        # assume : treatment mapper is already used before calling this private method

        treatment_map = self._treatment_groups_mapper
        treatment_map_inv = {v: k for k, v in self._treatment_groups_mapper.items()}
        self._df[treatment_col] = self._df[treatment_col].map(treatment_map)

        mask_test = self._df[segm_col] == "test"
        x_test = self._df.loc[mask_test, self._get_available_features()]
        y_test = self._df.loc[mask_test, target_col].values
        t_test = self._df.loc[mask_test, treatment_col].values

        for model_name, rankers in self._train_results.items():
            for ranker_method, current_results in rankers.items():
                for result in current_results:

                    estimator = result.estimator
                    features = result.features
                    uplift_prediction_type = result.uplift_prediction_type

                    # assume : model has method predict -- it is not propensity, it is uplift model
                    if uplift_prediction_type == "abs":
                        uplift_test = estimator.predict(x_test[features])
                    else:
                        estimator.predict(x_test[features])
                        uplift_test = estimator.trmnt_preds_ / estimator.ctrl_preds_ - 1

                    metric_values = np.zeros(shape=BOOTSTRAP_REPEATS)
                    rng = np.random.RandomState(seed=RANDOM_STATE)

                    for it in range(BOOTSTRAP_REPEATS):
                        idxs = rng.choice(
                            range(
                                mask_test.sum(),
                            ),
                            size=mask_test.sum(),
                            replace=True,
                        )
                        metric_values[it] = metric(
                            y_test[idxs], uplift_test[idxs], t_test[idxs]
                        )

                    result.median_test_metric_value = np.median(metric_values)

        self._df[treatment_col] = self._df[treatment_col].map(treatment_map_inv)

    def get_result(
        self,
        metric: tp.Callable[[np.array, np.array, np.array], float],
        n_max_features: int = None,
        rating: int = None,
    ):
        """
        Select model, features and uplift prediction type with specified rating w.r.t. sorting results by metric values on test data.
        It is possible to choose model from those which have no more than n_max_features features.
        Also it is possible to get model with at rating among filtered models.
        If no rating specified, then model is chosen by criterions:
            it has metric as great as 95% of best metric or greater
            it has the smallest number of features
            it has the simplest structure ("<" means "simpler")
                propensity baseline < S-learner < T-learner < X-learner < R-learner < UpliftRandomForest
        Models are sorted descending by median test metric estimated via bootstrap and form TOP.

        Returns : model_class_name, ranker_method, result
        """

        assert (
            n_max_features is not None
        ), "n_max_features is None, but should be either set by user or by default value in caller"

        self._get_median_test_metrics(metric)

        results = []

        for model_name, rankers in self._train_results.items():

            if model_name == "baseline":
                continue

            for ranker_method, current_results in rankers.items():

                for result in current_results:

                    if n_max_features < len(result.features):
                        continue

                    results.append((model_name, ranker_method, result))

        results = sorted(results, key=lambda p: -1 * p[2].median_test_metric_value)

        if rating is None:
            results = [
                p
                for p in results
                if p[2].median_test_metric_value
                >= 0.95 * results[0][2].median_test_metric_value
            ]
            min_n_features = min(len(p[2].features) for p in results)
            results = [p for p in results if len(p[2].features) == min_n_features]
            results = sorted(
                results, key=lambda p: p[0]
            )  # "SoloModel" < "TwoModels" < "UpliftRandomForest"
            model_class_name, ranker_method, result = results[0]
        else:
            model_class_name, ranker_method, result = results[rating]

        return model_class_name, ranker_method, result

    def _get_trn_vld_tst_predictions(self, model_result: ModelResult):
        segm_col = self._base_cols_mapper["segm"]

        mask_trn = self._df[segm_col] == "train"
        mask_val = self._df[segm_col] == "val"
        mask_tst = self._df[segm_col] == "test"

        estimator = model_result.estimator
        features = model_result.features
        uplift_type = model_result.uplift_prediction_type

        if type(estimator).__name__ == "CatBoostClassifier":
            uplift_trn = estimator.predict_proba(self._df.loc[mask_trn, features])[
                :, 1
            ].reshape(-1)
            uplift_val = estimator.predict_proba(self._df.loc[mask_val, features])[
                :, 1
            ].reshape(-1)
            uplift_tst = estimator.predict_proba(self._df.loc[mask_tst, features])[
                :, 1
            ].reshape(-1)

        else:
            uplift_trn = estimator.predict(self._df.loc[mask_trn, features]).reshape(-1)
            if (
                uplift_type == "rel"
                and type(estimator).__name__ != "AufRandomForestClassifier"
            ):
                uplift_trn = estimator.trmnt_preds_ / estimator.ctrl_preds_

            uplift_val = estimator.predict(self._df.loc[mask_val, features]).reshape(-1)
            if (
                uplift_type == "rel"
                and type(estimator).__name__ != "AufRandomForestClassifier"
            ):
                uplift_val = estimator.trmnt_preds_ / estimator.ctrl_preds_

            uplift_tst = estimator.predict(self._df.loc[mask_tst, features]).reshape(-1)
            if (
                uplift_type == "rel"
                and type(estimator).__name__ != "AufRandomForestClassifier"
            ):
                uplift_tst = estimator.trmnt_preds_ / estimator.ctrl_preds_

        return uplift_trn, uplift_val, uplift_tst

    def show_metrics_table(
        self,
        metrics_names: tp.List[str] = None,
        round_digits: int = 3,
        show_segments: tp.List[str] = ["train", "val", "test"],
    ):
        """Returns table with all available metrics for all trained models including baseline

        Args:
            metrics_names (tp.List[str], optional): _description_. Defaults to None.
            round_digits (int, optional): _description_. Defaults to 3.
            show_segments (tp.List[str], optional): _description_. Defaults to ["train", "val", "test"].

        Returns:
            pd.DataFrame: dataframe with all metrics for all trained models including baseline
        """

        assert metrics_names is None or all(
            [
                any([name == metric_name for name in METRICS])
                for metric_name in metrics_names
            ]
        ), (
            "Specify correct metric names or metric functions itself, already available metrics are:\n\t"
            + "\n\t".join(list(METRICS.keys()))
        )

        if metrics_names is None:
            use_at_k = list(range(5, 41, 5))
            use_bins = [5, 10, 20]
            metrics_names = []
            for name in METRICS.keys():
                if "@" in name and int(name.split("@")[-1]) not in use_at_k:
                    continue
                if (
                    "_bins" in name
                    and int(name.split("_bins")[0].split("_")[-1]) not in use_at_k
                ):
                    continue
                metrics_names.append(name)

        assert (
            show_segments
            and set(show_segments) - set({"train", "val", "test"}) == set()
        ), "show_segments parameter must be not empty and contain only labels from {'train', 'val', 'test'}"

        segm_col = self._base_cols_mapper["segm"]
        target_col = self._base_cols_mapper["target"]
        treatment_col = self._base_cols_mapper["treatment"]

        target = self._df[target_col]
        treatment = self._df[treatment_col].copy()

        treatment_map = self._treatment_groups_mapper
        treatment = treatment.map(treatment_map)

        mask_trn = self._df[segm_col] == "train"
        mask_val = self._df[segm_col] == "val"
        mask_tst = self._df[segm_col] == "test"

        y_trn, y_val, y_tst = target[mask_trn], target[mask_val], target[mask_tst]
        t_trn, t_val, t_tst = (
            treatment[mask_trn],
            treatment[mask_val],
            treatment[mask_tst],
        )

        metrics_df = None

        for model_name, rankers in self._train_results.items():
            for ranker_method, current_results in rankers.items():
                for result in current_results:

                    n_features = len(result.features)
                    uplift_type = result.uplift_prediction_type
                    uplift_trn, uplift_val, uplift_tst = (
                        self._get_trn_vld_tst_predictions(result)
                    )

                    for segm_name, segm_target, segm_treatment, segm_uplift in zip(
                        ["train", "val", "test"],
                        [y_trn, y_val, y_tst],
                        [t_trn, t_val, t_tst],
                        [uplift_trn, uplift_val, uplift_tst],
                    ):
                        if segm_name not in show_segments:
                            continue

                        metrics_info_row = {}
                        metrics_info_row.update(
                            {
                                "model_name": model_name,
                                "ranker_method": ranker_method,
                                "n_features": n_features,
                                "uplift_type": uplift_type,
                                "segm": segm_name,
                            }
                        )

                        metrics_info_row.update(
                            {
                                name: np.round(
                                    function(
                                        y_true=segm_target,
                                        treatment=segm_treatment,
                                        uplift=segm_uplift,
                                    ),
                                    round_digits,
                                )
                                for name, function in METRICS.items()
                                if name in metrics_names
                            }
                        )

                        if metrics_df is None:
                            metrics_df = pd.DataFrame(
                                columns=list(metrics_info_row.keys())
                            )

                        metrics_info_row_df = pd.DataFrame([metrics_info_row])
                        metrics_df = pd.concat(
                            [metrics_df, metrics_info_row_df], ignore_index=True
                        )

        metrics_df.set_index(
            ["model_name", "ranker_method", "n_features", "uplift_type"], inplace=True
        )

        return metrics_df

    def plot_results(
        self,
        metrics_df: pd.DataFrame,
        model_class_name: str,
        ranker_method: str,
        model_result: ModelResult,
        n_uplift_bins: int,
    ):

        segm_col = self._base_cols_mapper["segm"]
        target_col = self._base_cols_mapper["target"]
        treatment_col = self._base_cols_mapper["treatment"]

        target = self._df[target_col].copy()
        treatment = self._df[treatment_col].copy()

        treatment_map = self._treatment_groups_mapper
        treatment = treatment.map(treatment_map)

        mask_trn = self._df[segm_col] == "train"
        mask_val = self._df[segm_col] == "val"
        mask_tst = self._df[segm_col] == "test"

        y_trn, y_val, y_tst = target[mask_trn], target[mask_val], target[mask_tst]
        t_trn, t_val, t_tst = (
            treatment[mask_trn],
            treatment[mask_val],
            treatment[mask_tst],
        )

        uplift_trn, uplift_val, uplift_tst = self._get_trn_vld_tst_predictions(
            model_result
        )

        model_metrics_df = metrics_df.loc[
            metrics_df.index
            == (
                model_class_name,
                ranker_method,
                len(model_result.features),
                model_result.uplift_prediction_type,
            ),
            [
                "segm",
                "uplift@10",
                "uplift_rel@10",
                "uplift@15",
                "uplift_rel@15",
                "uplift@20",
                "uplift_rel@20",
                "qini_auc",
            ],
        ]

        model_metrics_df = model_metrics_df.sort_values(by=["segm"])
        model_metrics_df = model_metrics_df.iloc[[1, 2, 0]]
        display(model_metrics_df)
        save_dataframe_html(
            model_metrics_df,
            "2_best_model_main_metrics",
            "4_modeling_results",
            self._run_id,
        )

        metrics_dict = {}
        for metric_name in [
            "uplift@10",
            "uplift_rel@10",
            "uplift@15",
            "uplift_rel@15",
            "uplift@20",
            "uplift_rel@20",
            "qini_auc",
        ]:
            for segm in ["train", "val", "test"]:
                metrics_dict[f'{metric_name.replace("@", "_at_")}_{segm}'] = (
                    model_metrics_df.loc[
                        model_metrics_df["segm"] == segm, metric_name
                    ].values[0]
                )

        save_metrics(metrics_dict, self._run_id)

        uplift_buckets_info = self.show_uplift_by_bucket(
            model_result=model_result, show_segment="test", n_uplift_bins=n_uplift_bins
        )
        display(uplift_buckets_info)
        save_dataframe_html(
            uplift_buckets_info,
            "3_best_model_test_k_bins",
            "4_modeling_results",
            self._run_id,
        )

        uplift_type = {
            "abs": "absolute",
            "absolute": "absolute",
            "rel": "relative",
            "relative": "relative",
        }[model_result.uplift_prediction_type]

        figure_name = os.path.join("mlflow_artifacts", "2_metrics_by_segment_type.pdf")
        os.makedirs(os.path.dirname(figure_name), exist_ok=True)
        with PdfPages(figure_name) as pdf:
            for row, y, t, u, segm in zip(
                [0, 1, 2],
                [y_trn, y_val, y_tst],
                [t_trn, t_val, t_tst],
                [uplift_trn, uplift_val, uplift_tst],
                ["Train", "Val", "Test"],
            ):

                fig, axes = plt.subplots(1, 2, figsize=(10, 5))
                if row == 0:
                    fig.suptitle(f"Uplift type : {uplift_type}\n\n{segm}", fontsize=14)
                else:
                    fig.suptitle(f"{segm}", fontsize=14)

                plot_uplift_by_percentile(
                    y_true=y,
                    uplift=u,
                    treatment=t,
                    strategy="overall",
                    kind="bar",
                    bins=n_uplift_bins,
                    string_percentiles=True,
                    axes=axes[0],
                    draw_bars="rates",
                )

                plot_qini_curve(
                    y_true=y,
                    uplift=u,
                    treatment=t,
                    random=True,
                    perfect=False,
                    ax=axes[1],
                )

                axes[0].set_title(f"Uplift by decile", fontsize=12)
                axes[1].set_title(f"Qini curve", fontsize=12)

                plt.tight_layout()
                pdf.savefig()
                plt.show()
        save_pdf_figures(figure_name, "4_modeling_results", self._run_id)

    def plot_feature_importances(self, model_result: ModelResult):
        """Plots feature importances for specified model.

        Args:
            model_result (ModelResult): returned by get_resut()
        """

        estimator = model_result.estimator

        if isinstance(estimator, TwoModels):
            feats_c = np.array(estimator.estimator_ctrl.feature_names_)
            imps_c = np.array(estimator.estimator_ctrl.feature_importances_)
            mask = np.vectorize(lambda x: "treatment" not in x)(feats_c)
            feats_c, imps_c = feats_c[mask], imps_c[mask]

            feats_t = np.array(estimator.estimator_trmnt.feature_names_)
            imps_t = np.array(estimator.estimator_trmnt.feature_importances_)
            mask = np.vectorize(lambda x: "treatment" not in x)(feats_t)
            feats_t, imps_t = feats_t[mask], imps_t[mask]

            feats_imps_t = pd.DataFrame({"f": feats_t, "i": imps_t}).sort_values(
                by=["i"], ascending=False
            )
            feats_imps_c = pd.DataFrame({"f": feats_c, "i": imps_c}).sort_values(
                by=["i"], ascending=False
            )
            # feats_imps = pd.merge(feats_imps_t, feats_imps_c, on='f').rename(columns={'i_x': 'i_trmnt', 'i_y': 'i_cntrl'})

            feats_imps_t = feats_imps_t.iloc[:10]
            feats_imps_c = feats_imps_c.iloc[:10]
            feats_imps = pd.concat(
                [
                    feats_imps_t.reset_index(drop=True),
                    feats_imps_c.reset_index(drop=True),
                ],
                axis=1,
            ).round(4)
            feats_imps.columns = [
                "feature_treatment",
                "i_trmnt",
                "feature_control",
                "i_cntrl",
            ]

            def bold_common_values(val, common_values):
                if val in common_values:
                    return f"<b>{val}</b>"
                return str(val)

            common_feats = set(feats_imps["feature_treatment"]) & set(
                feats_imps["feature_control"]
            )
            feats_imps = feats_imps.applymap(
                lambda x: bold_common_values(x, common_feats)
            )

            fig, axes = plt.subplots(1, 2, figsize=(12, 6))

            plt.subplot(121)
            plt.title("Treatment TOP-10 features")
            sns.barplot(x=feats_imps_t["i"], y=feats_imps_t["f"], color="forestgreen")
            plt.xlabel("feature importance")
            plt.ylabel("feature name")

            plt.subplot(122)
            plt.title("Control TOP-10 features")
            sns.barplot(x=feats_imps_c["i"], y=feats_imps_c["f"], color="orange")
            plt.xlabel("feature importance")
            plt.ylabel("feature name")

            plt.tight_layout()

        else:
            if hasattr(estimator, "estimator"):
                feats = np.array(estimator.estimator.feature_names_)
                imps = np.array(estimator.estimator.feature_importances_)
            else:
                feats = np.array(estimator.feature_names_)
                imps = np.array(estimator.feature_importances_)

            mask = np.vectorize(lambda x: "treatment" not in x)(feats)
            feats, imps = feats[mask], imps[mask]

            feats_imps = pd.DataFrame({"f": feats, "i": imps}).sort_values(
                by=["i"], ascending=False
            )
            feats_imps = feats_imps.iloc[:10].reset_index(drop=True)

            fig, axes = plt.subplots(1, 1, figsize=(6, 6))

            plt.subplot(111)
            plt.title("TOP-10 feature importances")
            sns.barplot(x=feats_imps["i"], y=feats_imps["f"])
            plt.xlabel("feature importance")
            plt.ylabel("feature name")
            feats_imps = feats_imps.rename(columns={"f": "features"}).round(4)

        save_figure(
            fig, "4_feature_importance_top_10", "4_modeling_results", self._run_id
        )
        save_dataframe_html(
            feats_imps,
            "4_feature_importance_top_10",
            "4_modeling_results",
            self._run_id,
        )

        return feats_imps

    def show_uplift_by_bucket(
        self,
        model_result: ModelResult,
        show_segment: str = "test",
        n_uplift_bins: int = 10,
    ):
        """Return table with info by sample bucket sorted by uplift descending."""
        assert show_segment in ["train", "val", "test"]

        mask = self._df[self._base_cols_mapper["segm"]] == show_segment

        target = self._df.loc[mask, self._base_cols_mapper["target"]]
        treatment = self._df.loc[mask, self._base_cols_mapper["treatment"]]
        treatment = treatment.map(self._treatment_groups_mapper)

        uplift_trn, uplift_val, uplift_tst = self._get_trn_vld_tst_predictions(
            model_result
        )
        idx = [i for i in range(3) if ["train", "val", "test"][i] == show_segment][0]
        uplift = [uplift_trn, uplift_val, uplift_tst][idx]

        buckets_info = uplift_by_percentile(
            target, uplift, treatment, bins=n_uplift_bins
        )
        buckets_info["rel_uplift, %"] = (
            buckets_info["response_rate_treatment"]
            / buckets_info["response_rate_control"]
            - 1
        ) * 100
        # buckets_info['extra_potential_targets\n(bucket_size * bucket_uplift)'] = (
        #     (buckets_info["n_treatment"] + buckets_info["n_control"]) * buckets_info["uplift"]
        # )
        return buckets_info

    def train_propensity_baseline(
        self,
        features: tp.List[str],
        metric: object = roc_auc_score,
        timeout_estimator: int = 60,
        search_class=OptuneUpliftDefault,
    ):
        """Train Catboost response model without treatment
           Save results in attribute self._train_results

        Args:
            features (1d array-like): a list of features to be used for training the models
            metric: optimization function for optune class
            timeout_estimator (int): time for fitting one estimator
            search_class: class for class estimators best params search

        Returns: None

        Examples:
            >>> pipeline.train_propensity_baseline(features=pipeline._get_available_features())
            or
            >>> pipeline.train_propensity_baseline(features=['age', 'gender', 'tail'], metric=accuracy_score, timeout_estimator=20)
        """
        assert len(features) == len(
            set(features) & set(self._feature_cols)
        ), f"{[f for f in features if f not in self._feature_cols]} не входят в self._feature_cols "
        segm_col = self._base_cols_mapper["segm"]
        target_col = self._base_cols_mapper["target"]
        treatment_col = self._base_cols_mapper["treatment"]

        treatment_map = self._treatment_groups_mapper
        treatment_map_inv = {v: k for k, v in self._treatment_groups_mapper.items()}
        self._df[treatment_col] = self._df[treatment_col].map(treatment_map)

        try:
            df_train_mask = self._df[segm_col] == "train"
            df_val_mask = self._df[segm_col] == "val"
            df_test_mask = self._df[segm_col] == "test"

            finder_class = OptuneUpliftDefault(
                self._df.loc[df_train_mask],
                self._df.loc[df_val_mask],
                metric,
                treatment_col,
                target_col,
            )

            model = finder_class.best_params_find(
                CatBoostClassifier, features, timeout_estimator
            )

            baseline_result = fit_model(
                model,
                self._df.loc[df_train_mask],
                self._df.loc[df_val_mask],
                self._df.loc[df_test_mask],
                features,
                target_col,
                treatment_col,
            )

            self._train_results["baseline"] = {"custom": [baseline_result]}

        finally:
            self._df[treatment_col] = self._df[treatment_col].map(treatment_map_inv)

    def _modify_catboost_params_dict(self, params: tp.Dict[str, float]):
        assert "depth" in params or "max_depth" in params
        assert "iterations" in params or "n_estimators" in params

        if "depth" in params:
            params["max_depth"] = params["depth"]
        else:
            params["depth"] = params["max_depth"]

        if "n_estimators" in params:
            params["iterations"] = params["n_estimators"]
        else:
            params["n_estimators"] = params["iterations"]

    def preprocess(
        self,
        numerical_method: str = "min",
        max_categories: int = 4,
        encoder_type: str = "target",
    ):
        """Preprocessing numerical and categorical data"""
        segm_col = self._base_cols_mapper["segm"]
        target_col = self._base_cols_mapper["target"]
        df_train_mask = self._df[segm_col] == "train"
        self._feature_cols = self._get_available_features()

        categorical_cols = [
            f for f in self._feature_cols if self._df[f].dtype == "object"
        ]
        numeric_cols = [f for f in self._feature_cols if self._df[f].dtype != "object"]

        self._preprocessor = Preprocessor(
            numerical_method, max_categories, encoder_type
        )
        self._preprocessor.fit(
            df=self._df[df_train_mask],
            numeric_cols=numeric_cols,
            categorical_cols=categorical_cols,
            target_col=target_col,
        )
        self._raw_df = self._df.copy()
        self._df = self._preprocessor.transform(self._df)

    def run(
        self,
        max_val_roc_auc_treatment: float = 0.65,
        early_stopping: int = 10,
        n_features_candidates: int = 200,
        max_abs_feature_correlation: float = 0.95,
        classes_for_train: tp.List[str] = [
            "SoloModel",
            "TwoModels",
            "AufRandomForestClassifier",
        ],
        feature_nums: tp.List[int] = [20, 35, 50, 100],
        train_with_optuna: bool = True,
        timeout_estimator: int = 60 * 3,
        opt_metric: str = "qini_auc",
        n_min_features: int = 5,
        n_max_features: int = None,
        n_uplift_bins: int = 10,
    ):
        """Runs all necessary steps of uplift pipeline except loading sample with default parameters."""

        run_parameters = {
            "max_val_roc_auc_treatment": max_val_roc_auc_treatment,
            "early_stopping": early_stopping,
            "n_features_candidates": n_features_candidates,
            "max_abs_feature_correlation": max_abs_feature_correlation,
            "classes_for_train": classes_for_train,
            "feature_nums": feature_nums,
            "train_with_optuna": train_with_optuna,
            "timeout_estimator": timeout_estimator,
            "opt_metric": opt_metric,
            "n_min_features": n_min_features,
            "n_max_features": n_max_features,
            "n_uplift_bins": n_uplift_bins,
        }
        save_json(run_parameters, "parameters", "0_pipeline_setting", self._run_id)

        self._use_default_run = True
        print("Preprocess features\n")
        self.preprocess()
        print(
            "Start with cleaning feature list: remove leaks, unimportant features and so on.\n"
        )

        self.check_treatment_leaks(
            max_val_roc_auc_treatment=max_val_roc_auc_treatment,
            early_stopping=early_stopping,
        )
        print(
            f"Number of features after cleaning: {len(self._get_available_features())}"
        )
        self.preselect_features_candidates(n_features_candidates, "importance")

        self.check_correlated_features(
            max_abs_feature_correlation, check_only_available_features=True
        )

        self.show_removed_features_with_reasons()

        print("\nRank filtered feature list by different kinds of importance.\n")

        self.rank_features_candidates()

        print(
            "Train models using different number of top features from every sort method.\n"
        )

        opt_metric = METRICS[opt_metric]

        if n_max_features is None:
            n_max_features = len(self._get_available_features())

        feature_nums = sorted(feature_nums)
        feature_nums = [
            x for x in feature_nums if x <= len(self._get_available_features())
        ]
        if feature_nums[-1] != len(self._get_available_features()):
            feature_nums.append(len(self._get_available_features()))
        feature_nums = [
            x for x in feature_nums if n_min_features <= x <= n_max_features
        ]

        self.train_models(
            classes=classes_for_train,
            features=None,
            feature_nums=feature_nums,
            use_default_params=not train_with_optuna,
            metric=opt_metric,
            timeout_estimator=timeout_estimator,
        )

        # print("Train propensity baseline.")
        # self.train_propensity_baseline(
        #     features = self._get_available_features(),
        #     metric = roc_auc_score,
        #     timeout_estimator = 120,
        #     search_class = OptuneUpliftDefault,
        # )
        # print("\n\n")

        if train_with_optuna:
            print("\nFind the best model.")
        else:
            print("\nAssess models quality")

        model_class_name, ranker_method, best_result = self.get_result(
            metric=opt_metric, n_max_features=n_max_features, rating=0
        )
        (
            best_model,
            best_model_name,
            best_ranker_name,
            best_n_features,
            best_uplift_type,
        ) = (
            best_result.estimator,
            model_class_name,
            ranker_method,
            len(best_result.features),
            best_result.uplift_prediction_type,
        )

        # TODO : add such method for getting specific model if you want
        # best_model, model_class_name, ranker_name, n_features = self._get_model(class_name, ranker_name, n_features)

        print("\n\nBest model description:")
        print(f"{'':<4}{'feature ranker':<21}: {best_ranker_name}")
        print(f"{'':<4}{'features count':<21}: {best_n_features}")
        print(f"{'':<4}{'model class':<21}: {best_model_name}")
        print(f"{'':<4}{'uplift type':<21}: {best_uplift_type}\n")

        best_model_wrapped = AUFModel(
            best_model,
            type(best_model).__name__,
            best_result.features,
            best_uplift_type,
        )
        save_model(
            best_model_wrapped,
            "5_best_model_artifacts",
            self._run_id,
            self._experiment_name,
        )

        if best_model_name == "TwoModels":
            ctrl_params = best_model.estimator_ctrl.get_params()
            trmnt_params = best_model.estimator_trmnt.get_params()
            self._modify_catboost_params_dict(ctrl_params)
            self._modify_catboost_params_dict(trmnt_params)
            print(f"\n{'':<4}control model parameters:")
            print(f"{'':<8}{'iterations':<17}: {ctrl_params['iterations']}")
            print(f"{'':<8}{'max_depth':<17}: {ctrl_params['max_depth']}")
            print(f"{'':<8}{'learning_rate':<17}: {ctrl_params['learning_rate']}")
            print(f"\n{'':<4}treatment model parameters:")
            print(f"{'':<8}{'iterations':<17}: {trmnt_params['iterations']}")
            print(f"{'':<8}{'max_depth':<17}: {trmnt_params['max_depth']}")
            print(f"{'':<8}{'learning_rate':<17}: {trmnt_params['learning_rate']}")
        elif best_model_name == "SoloModel":
            params = best_model.estimator.get_params()
            self._modify_catboost_params_dict(params)
            print(f"\n{'':<4}model parameters:")
            print(f"{'':<8}{'iterations':<17}: {params['iterations']}")
            print(f"{'':<8}{'max_depth':<17}: {params['max_depth']}")
            try:
                print(f"{'':<8}{'learning_rate':<17}: {params['learning_rate']}")
            except:
                print(
                    f"{'':<8}{'evaluationFunction':<17}{params['evaluationFunction']}"
                )
        elif best_model_name == "AufXLearner":
            params = best_model.get_params()
            model_params = params["model"].get_params()
            uplift_model_params = params["uplift_model"].get_params()
            self._modify_catboost_params_dict(model_params)
            self._modify_catboost_params_dict(uplift_model_params)
            print(f"\n{'':<4}(1 step) model parameters:")
            print(f"{'':<8}{'iterations':<17}: {model_params['iterations']}")
            print(f"{'':<8}{'max_depth':<17}: {model_params['max_depth']}")
            print(f"{'':<8}{'learning_rate':<17}: {model_params['learning_rate']}")
            print(f"\n{'':<4}(2 step) uplift model parameters:")
            print(f"{'':<8}{'iterations':<17}: {uplift_model_params['iterations']}")
            print(f"{'':<8}{'max_depth':<17}: {uplift_model_params['max_depth']}")
            print(
                f"{'':<8}{'learning_rate':<17}: {uplift_model_params['learning_rate']}"
            )
        else:
            # TODO : create separate method for printing best model parameters
            #        consider x-learner, uplift tree & uplift forest cases
            params = best_model.get_params()
            print(f"\n{'':<4}model parameters:")
            for name, value in params.items():
                print(f"{'':<8}{name}{'':<4}{value}")

        params = best_model.get_params()
        params["best_model_name"] = best_model_name
        params["best_ranker_name"] = best_ranker_name
        params["best_n_features"] = best_n_features
        params["best_uplift_type"] = best_uplift_type
        save_params_dict(params, self._run_id)

        print("\n\nBest model quality table:")
        full_metrics_df = self.show_metrics_table(
            metrics_names=[
                "uplift@10",
                "uplift_rel@10",
                "uplift@15",
                "uplift_rel@15",
                "uplift@20",
                "uplift_rel@20",
                "qini_auc",
                "qini_auc_20",
            ]
        )
        self._full_metrics_df = full_metrics_df
        save_dataframe_html(
            full_metrics_df,
            "1_all_models_all_metrics",
            "4_modeling_results",
            self._run_id,
        )

        if best_model_name != "AufXLearner":
            self.plot_feature_importances(model_result=best_result)
        else:
            print("AufXLearner has no feature importance analysis for now")

        self.plot_results(
            full_metrics_df, model_class_name, ranker_method, best_result, n_uplift_bins
        )

        features = self._ranked_candidates[best_ranker_name][:best_n_features]
        save_json(features, "model_features", "5_best_model_artifacts", self._run_id)
        save_json(
            self._preprocessor.get_dict_class(),
            "features_preprocessor",
            "5_best_model_artifacts",
            self._run_id,
        )
        figure_name = os.path.join(
            "mlflow_artifacts", "5_uplift_by_feature_bins_top_10_features.pdf"
        )
        os.makedirs(os.path.dirname(figure_name), exist_ok=True)
        with PdfPages(figure_name) as pdf:
            for i, f in enumerate(features[:10]):
                plot_uplift_by_feature_bins(
                    self._raw_df[f],
                    self._raw_df[self._base_cols_mapper["treatment"]].map(
                        self._treatment_groups_mapper
                    ),
                    self._raw_df[self._base_cols_mapper["target"]],
                    f"{f}",
                    amount_of_bins=6,
                )

                plt.tight_layout()
                pdf.savefig()
                plt.show()
        save_pdf_figures(figure_name, "4_modeling_results", self._run_id)

        fig, axes = plt.subplots(1, 1, figsize=(12, 8))
        test_mask = self._df[self._base_cols_mapper["segm"]] == "test"
        plot_portrait_tree(
            x=self._df.loc[test_mask, best_result.features],
            uplift=best_model.predict(self._df.loc[test_mask, best_result.features]),
            max_depth=2,
            axes=axes,
        )
        plt.tight_layout()
        save_figure(fig, "6_client_portrait_tree", "4_modeling_results", self._run_id)
        plt.show()

        self._use_default_run = False

        # return Inference(best_estimator, features)
        return best_model, features, best_result
