import typing as tp

import numpy as np
import pandas as pd
import scipy.stats as ss
from catboost import CatBoostClassifier
from sklearn.metrics import roc_auc_score

from ..constants import BOOTSTRAP_REPEATS, RANDOM_STATE


def check_bernoulli_dependence(x: np.array, y: np.array, alpha: float = 0.05):
    """Check if 2 binary flags are dependent

    Args:
        x, y (1d array-like): paired observations of flags
        alpha (float): max level for error of the 1-st type. Default 0.05

    Returns:
        dict: Result of dependency check
        {'stat': stat_value,
         'critical_stat': critical_stat_value,
         'dependent': bool_decision (1 == dependent == stat > critical),
         'pvalue': pvalue
        }
    """
    assert len(x) == len(y), f"{len(x)} != {len(y)}"
    assert set(np.unique(x)) == set([0, 1]), f"set(np.unique(x)) = {set(np.unique(x))}"
    assert set(np.unique(y)) == set([0, 1]), f"set(np.unique(y)) = {set(np.unique(y))}"
    assert 0.0 < alpha < 1.0

    n = len(x)
    co_matr = np.array([[0, 0], [0, 0]])
    for i in [0, 1]:
        for j in [0, 1]:
            co_matr[i, j] = np.sum((x == i) * (y == j))

    stat_sum = 0.0
    for i in [0, 1]:
        for j in [0, 1]:
            x_i = np.sum(co_matr[i, :])
            y_j = np.sum(co_matr[:, j])
            stat_sum += co_matr[i, j] ** 2 / (x_i * y_j)

    stat = n * (stat_sum - 1)

    critical_stat = ss.chi2(df=1).ppf(1 - alpha)
    pvalue = 1 - ss.chi2(df=1).cdf(stat)

    return {
        "stat": stat,
        "critical_stat": critical_stat,
        "dependent": stat > critical_stat,
        "pvalue": pvalue,
    }


def check_bernoulli_equal_means(x: np.array, y: np.array, alpha: float = 0.05):
    """Check if 2 binary flags have the same mean

    Args:
        x, y (1d array-like): (generally not paired) observations of flags
        alpha (float): max level for error of the 1-st type

    Returns:
        dict: Result of equal means check
        {'stat': stat_value,
         # 'critical_stat': critical_stat_value,
         'equals': bool_decision (1 == dependent == stat > critical),
         'pvalue': pvalue
         }
    """
    stat, pvalue = ss.ttest_ind(
        x,
        y,
        equal_var=False,
        nan_policy="propagate",
        alternative="two-sided",
    )

    return {
        "stat": stat,
        # 'critical_stat': critical_stat_value,
        "equals": pvalue >= alpha,
        "pvalue": pvalue,
    }


def check_nans(
    df: pd.DataFrame, feature_cols: tp.List[str], max_nan_ratio: float = 0.95
):
    """Check if the percentage of nans in a feature exceeds a certain specified threshold
       and then filter out the features where it does

    Args:
        df (pd.DataFrame): dataframe with features
        feature_cols (1d array-like): features to check
        max_nan_ratio (float): maximum allowable nans ratio for each feature
            in all (train / val / test) sets together

    Returns:
        list: Column names in which the percentage of nans does not exceed the specified threshold
    """
    return [f for f in feature_cols if df[f].isna().mean() <= max_nan_ratio]


# TO-DO: переименовать функцию в check_not_enough_unique_values или check_few_unique_values или вообще check_unique_values
def check_too_less_unique_value(df: pd.DataFrame, feature_cols: tp.List[str]):
    """Check that features have at least 2 unique values, filter out others

    Args:
        df (pd.DataFrame): dataframe with features
        feature_cols (1d array-like): features to check

    Returns:
        list: Column names in which the number of unique values is greater than one
    """
    return [f for f in feature_cols if df[f].nunique() >= 2]


# TO-DO: переименовать функцию в check_not_enough_unique_values или check_few_unique_values или вообще check_unique_category_values
def process_too_much_categories(
    df: pd.DataFrame, feature_cols: tp.List[str], max_categories_count: int = 20
):
    """Check that categorical features do not have more than specified number of unique values,
        if they do, leave the top of categories, all rest are replaced by "_others_"

    Args:
        df (pd.DataFrame): dataframe with features
        feature_cols (1d array-like): features to check
        max_categories_count (float): maximum allowable number of unique values for categorical
            feature in all (train / val / test) sets together

    Returns: None
    """
    for col in feature_cols:
        if df[col].dtype == "object" and df[col].nunique() >= max_categories_count:
            sorted_values_desc = df[col].value_counts().sort_values()[::-1]
            others = sorted_values_desc[max_categories_count - 1 :].index.tolist()
            df.loc[df[col].isin(others), col] = "_others_"


# TO-DO: Нужно ли вместе с early_stopping добавить допустимое уменьшение roc auc?
def check_leaks_v2(
    df: pd.DataFrame,
    base_cols_mapper: tp.Dict[str, str],
    feature_cols: tp.List[str],
    col_to_check: str,
    alpha: float = 0.05,
    max_val_roc_auc: float = 0.6,
    early_stopping: int = None,
):
    """Find features with leak on target or treatment using simple ML model

    Args:
        df (pd.DataFrame): dataframe with features
        base_cols_mapper (dict): dictionary of correspondences between the columns names used
            in library functions and names in input data
        feature_cols (1d array-like): features to check
        col_to_check (string): 'target' or 'treatment' -- names of columns to check for leaks
        alpha (float): significance level
        max_val_roc_auc (float): maximum allowable ROC-AUC score for predicting col_to_check
            by any single feature on validation set
        early_stopping (int): number of consecutive stages dirung which the model's preformance
            on the validation set plateaus or worsens

    One of preselection steps which helps to search appropriate feature candidates for modelling

    Idea:
        - build a small model for check_to_col prediction
        - assess degree of the total leak from all features with procedure which is described below
        - if leak is statistically significant, then drop top-1 feature (with the greatest feature_importance_) and repeat
        - else stop algorithm and return all other "clean" features

    Leak assession procedure description:
        - small model (CatBoostClassifier) is fitted on training set using all available features
        - probability predictions are made for validation set
        - these probabilities are bootstrapped 500 times together with corresponding targets
        - ROC-AUC is calculated for each bootstrapped probabilities and targets sample
        - all ROC-AUC scores less than 0.5 are transformed with function f(x) = 1 - x (x := max(x, 1-x))
        - (1 - alpha) quantile is computed for these 500 scores
        - if estimated quantile is less than max_val_roc_auc then leak is thought to be not such significant
        - if estimated quantile is more than max_val_roc_auc then leak is thought to exist

     Advantage over simple filter used in original function:
        - this method consideres features interactions in treatment prediction
        - for example, 3 features each with ROC-AUC 0.6 may give ROC-AUC 0.8 used together in one model

    Returns:
        leaks_roc_aucs (list): Feature names and ROC-AUCs of leaking features
        not_leaks (list): Feature names of non leaking features
        all_features_roc_aucs (list): Feature name and ROC-AUC for each feature
    """
    assert col_to_check in [
        "target",
        "treatment",
    ], f"Error : col_to_check must be in ['target', 'treatment'] but col_to_check='{col_to_check}'"
    assert (
        0.0 < alpha and alpha < 1.0
    ), f"alpha must be in [0.0, 1.0] but is {alpha:.2f}"
    assert (
        max_val_roc_auc > 0.5
    ), f"max_val_roc_auc must be greater than 0.5, but is {max_val_roc_auc:.2f}"

    features = feature_cols.copy()
    all_features_roc_aucs = []

    segm_col = base_cols_mapper["segm"]
    col_to_check = base_cols_mapper[col_to_check]

    while len(features) > 0:
        feature_df_train = df.loc[
            df[segm_col] == "train", features + [col_to_check]
        ].copy()
        feature_df_val = df.loc[df[segm_col] == "val", features + [col_to_check]].copy()

        bootstrap_data_size = max(
            15_000, min(feature_df_val.shape[0], int(df.shape[0] * 0.1))
        )
        feature_df_val = feature_df_val.sample(bootstrap_data_size, random_state=8)

        for f in features:
            if df[f].dtype == "object":
                feature_df_train[f] = feature_df_train[f].astype(str)
                feature_df_val[f] = feature_df_val[f].astype(str)

        checker = CatBoostClassifier(
            n_estimators=10,
            depth=2,
            learning_rate=0.1,
            silent=True,
            random_seed=8,
            cat_features=[f for f in features if df[f].dtype == "object"],
        )

        checker.fit(feature_df_train[features], feature_df_train[col_to_check])
        val_preds = checker.predict_proba(feature_df_val[features])[:, 1]
        val_true = feature_df_val[col_to_check].values

        bootstrap_roc_aucs = np.zeros(shape=BOOTSTRAP_REPEATS)
        rng = np.random.RandomState(seed=RANDOM_STATE)

        for boot in range(BOOTSTRAP_REPEATS):
            idxs = rng.choice(range(len(val_true)), size=len(val_true), replace=True)
            true, preds = val_true[idxs], val_preds[idxs]
            roc_auc = roc_auc_score(true, preds)
            bootstrap_roc_aucs[boot] = roc_auc

        # other (simpler?) but equivalent way to determine leak ?
        # pvalue = np.mean(bootstrap_roc_aucs >= max_val_roc_auc)
        # if pvalue >= alpha:
        #     not_leaks.append(f)

        q = np.quantile(bootstrap_roc_aucs, q=1 - alpha)
        q = max(q, 1 - q)  # revert labels if needed

        # if q < max_val_roc_auc:
        #     # this max allowed value is quite rare
        #     # all leaks found
        #     break

        top_leaking_feature = features[np.argmax(checker.feature_importances_)]
        features.remove(top_leaking_feature)
        all_features_roc_aucs.append((top_leaking_feature, q))

        if early_stopping is not None:
            if early_stopping == 0:
                break
            if q < max_val_roc_auc:
                early_stopping -= 1

    leaks_roc_aucs = [(f, q) for f, q in all_features_roc_aucs if q >= max_val_roc_auc]
    not_leaks = [
        f for f, q in all_features_roc_aucs if q < max_val_roc_auc
    ] + features  # not saved as leaks --> not leaks

    leaks_roc_aucs = sorted(leaks_roc_aucs, key=lambda p: -p[1])
    all_features_roc_aucs = sorted(all_features_roc_aucs, key=lambda p: -p[1])

    return leaks_roc_aucs, not_leaks, all_features_roc_aucs


def check_leaks(
    df: pd.DataFrame,
    base_cols_mapper: tp.Dict[str, str],
    feature_cols: tp.List[str],
    col_to_check: str,
    alpha: float = 0.05,
    max_val_roc_auc: float = 0.6,
):
    """Find features with leak on target or treatment using simple ML model

    Args:
        df (pd.DataFrame): dataframe with features
        base_cols_mapper (dict): dictionary of correspondences between the columns names used
            in library functions and names in input data
        feature_cols (1d array-like): features to check
        col_to_check (string): 'target' or 'treatment' -- names of columns to check for leaks
        alpha (float): significance level
        max_val_roc_auc (float): maximum allowable ROC-AUC score for predicting col_to_check
            by any single feature on validation set

    One of preselection steps which helps to search appropriate feature candidates for modelling

    Idea: (1 - alpha) quantile of validation ROC-AUC score in col_to_check prediction is estimated
        for each single feature independently with following procedure:
        - small model (CatBoostClassifier) is fitted on training set using only this one feature
        - probability predictions are made for validation set
        - these probabilities are bootstrapped 500 times together with corresponding targets
        - ROC-AUC is calculated for each bootstrapped probabilities and targets sample
        - all ROC-AUC scores less than 0.5 are transformed with function f(x) = 1 - x
        - compute (1 - alpha) quantile of these 500 scores

    The rule of leak detection for each feature is:
        - if estimated quantile is less than max_val_roc_auc then leak is thought to be not such significant
        - if estimated quantile is more than max_val_roc_auc then leak is thought to exist

    Returns:
        leaks_roc_aucs (list): Feature names and ROC-AUCs of leaking features
        not_leaks (list): Feature names of non leaking features
        all_features_roc_aucs (list): Feature name and ROC-AUC for each feature
    """

    assert col_to_check in [
        "target",
        "treatment",
    ], f"Error : col_to_check must be in ['target', 'treatment'] but col_to_check='{col_to_check}'"
    assert (
        0.0 < alpha and alpha < 1.0
    ), f"alpha must be in [0.0, 1.0] but is {alpha:.2f}"
    assert (
        max_val_roc_auc > 0.5
    ), f"max_val_roc_auc must be greater than 0.5, but is {max_val_roc_auc:.2f}"

    leaks_roc_aucs = []
    not_leaks = []
    all_features_roc_aucs = []

    segm_col = base_cols_mapper["segm"]
    col_to_check = base_cols_mapper[col_to_check]

    for f in feature_cols:
        feature_df_train = df.loc[df[segm_col] == "train", [f, col_to_check]].copy()
        feature_df_val = df.loc[df[segm_col] == "val", [f, col_to_check]].copy()

        if df[f].dtype == "object":
            feature_df_train[f] = feature_df_train[f].astype(str)
            feature_df_val[f] = feature_df_val[f].astype(str)

        checker = CatBoostClassifier(
            n_estimators=30,
            depth=1,
            learning_rate=0.1,
            silent=True,
            random_seed=8,
            cat_features=[f] if df[f].dtype == "object" else [],
        )

        checker.fit(feature_df_train[[f]], feature_df_train[col_to_check])
        val_preds = checker.predict_proba(feature_df_val[[f]])[:, 1]
        val_true = feature_df_val[col_to_check].values

        bootstrap_roc_aucs = np.zeros(shape=BOOTSTRAP_REPEATS)
        rng = np.random.RandomState(seed=RANDOM_STATE)

        for boot in range(BOOTSTRAP_REPEATS):
            idxs = rng.choice(range(len(val_true)), size=len(val_true), replace=True)
            true, preds = val_true[idxs], val_preds[idxs]
            roc_auc = roc_auc_score(true, preds)
            bootstrap_roc_aucs[boot] = roc_auc

        # other (simpler?) but equivalent way to determine leak ?
        # pvalue = np.mean(bootstrap_roc_aucs >= max_val_roc_auc)
        # if pvalue >= alpha:
        #     not_leaks.append(f)

        q = np.quantile(bootstrap_roc_aucs, q=1 - alpha)
        q = max(q, 1 - q)  # revert labels if needed

        all_features_roc_aucs.append((f, q))

        if q < max_val_roc_auc:
            # this max allowed value is quite rare
            not_leaks.append(f)
        else:
            # this value is not so rare
            leaks_roc_aucs.append((f, q))

    leaks_roc_aucs = sorted(leaks_roc_aucs, key=lambda p: -p[1])
    all_features_roc_aucs = sorted(all_features_roc_aucs, key=lambda p: -p[1])

    return leaks_roc_aucs, not_leaks, all_features_roc_aucs


def check_correlations(
    df: pd.DataFrame, feature_cols: tp.List[str], max_abs_corr: float = 0.95
):
    """Check that pairwise correlation of all features does not exeed a certain
        specified threshold, filter out others

    Args:
        df (pd.DataFrame): dataframe with features
        feature_cols (1d array-like): features to check
        max_abs_corr (float): maximum allowable absolute value for correlation between features

    Both train and validation sets are used here to get more precise results

    Algorithm checks for each feature independently:
        - correlations with other features which weren't checked with it yet
        - all features which have correlation greater than max_abs_corr are filtered
        - next feature checks are made with modified feature set

    Returns:
        too_correlated (list): Feature pairs with correlation higher than a given threshold
        features (list): Filtered feature names
    """

    assert (
        0.0 < max_abs_corr and max_abs_corr < 1.0
    ), f"max_abs_corr must be from 0 to 1, but is {max_abs_corr:.2f}"

    # df_trn_val = df.loc[(df["segm"] == "train") | (df["segm"] == "val")]
    # corr_matr = df_trn_val[feature_cols].corr()
    corr_matr = df[feature_cols].corr()

    too_correlated: list[tuple[str, str]] = []
    features = feature_cols.copy()
    something_deleted = True

    while something_deleted:
        features_to_remove = []
        something_deleted = False

        for f in features:
            if f in features_to_remove or df[f].dtype == "object":
                continue

            i = corr_matr.columns.get_loc(f)
            abs_corrs = corr_matr.iloc[i, i + 1 :].abs()
            bad_corrs_cols = list(abs_corrs[abs_corrs > max_abs_corr].index)
            bad_corrs_cols = [
                g
                for g in bad_corrs_cols
                if g not in features_to_remove and g in features
            ]
            too_correlated.extend([(f, g) for g in bad_corrs_cols])
            features_to_remove.extend(bad_corrs_cols)

        if features_to_remove:
            something_deleted = True
            features = [f for f in features if f not in features_to_remove]

    return too_correlated, features


def check_train_val_test_split(
    df: pd.DataFrame,
    segm_col: str,
    target_col: str,
    treatment_col: str,
    treatment_groups_mapper: tp.Dict[tp.Any, int],
):
    # segm_col = self._base_cols_mapper["segm"]
    # target_col = self._base_cols_mapper["target"]
    # treatment_col = self._base_cols_mapper["treatment"]
    # treatment_flag = df[treatment_col].map(self._treatment_groups_mapper)

    for col in [segm_col, target_col, treatment_col]:
        assert col in df.columns

    segm = df[segm_col]
    target = df[target_col]
    treatment = df[treatment_col].map(treatment_groups_mapper)

    segm_counts = segm.value_counts()
    segm_ratios = segm.value_counts() / df.shape[0]

    # TODO: нужно ли это? если да, убрать ли одно из двух / ослабить ограничения?
    # check segment sizes
    # if segm_ratios.loc["val"] < 0.15 and segm_counts.loc["val"] < 15_000:
    #     message = f"'{segm_col}' column must contain at least 15% or 15000 of 'val' samples"
    #     raise AssertionError(message)
    # if segm_ratios.loc["test"] < 0.15 and segm_counts.loc["test"] < 15_000:
    #     message = f"'{segm_col}' column must contain at least 15% or 15000 of 'test' samples"
    #     raise AssertionError(message)

    mask_train = (segm == "train").values
    mask_val = (segm == "val").values
    mask_test = (segm == "test").values

    # check treatment = 1 ratio in segments to be equal
    treatment_train = treatment[mask_train]
    treatment_val = treatment[mask_val]
    treatment_test = treatment[mask_test]

    result_train_val = check_bernoulli_equal_means(
        treatment_train, treatment_val, alpha=0.05
    )
    result_val_test = check_bernoulli_equal_means(
        treatment_val, treatment_test, alpha=0.05
    )

    if not result_train_val["equals"] or not result_val_test["equals"]:
        raise AssertionError(
            "Treatment ratio should be the same in train, val, test splits"
        )

    # check target = 1 ratio in segments to be equal w.r.t. treatment group
    target_train_treatment = target[mask_train & (treatment == 1)]
    target_val_treatment = target[mask_val & (treatment == 1)]
    target_test_treatment = target[mask_test & (treatment == 1)]

    result_train_val = check_bernoulli_equal_means(
        target_train_treatment, target_val_treatment, alpha=0.05
    )
    result_val_test = check_bernoulli_equal_means(
        target_val_treatment, target_test_treatment, alpha=0.05
    )

    if not result_train_val["equals"] or not result_val_test["equals"]:
        raise AssertionError(
            "Target rate ratio should be the same in train, val, test splits in treatment group"
        )

    # check target = 1 ratio in segments to be equal w.r.t. control group
    target_train_control = target[mask_train & (treatment == 0)]
    target_val_control = target[mask_val & (treatment == 0)]
    target_test_control = target[mask_test & (treatment == 0)]

    result_train_val = check_bernoulli_equal_means(
        target_train_control, target_val_control, alpha=0.05
    )
    result_val_test = check_bernoulli_equal_means(
        target_val_control, target_test_control, alpha=0.05
    )

    if not result_train_val["equals"] or not result_val_test["equals"]:
        raise AssertionError(
            "Target rate ratio should be the same in train, val, test splits in control group"
        )
