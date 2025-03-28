import typing as tp

import numpy as np
import pandas as pd
from sklearn.utils.validation import check_consistent_length
from sklift.metrics import qini_auc_score, response_rate_by_percentile
from sklift.utils import check_is_binary


def bin_weighted_average_uplift(
    y_true: tp.Sequence[float],
    uplift: tp.Sequence[float],
    treatment: tp.Sequence[float],
    uplift_type: tp.Union["absolute", "relative"] = "absolute",
    strategy: tp.Union["overall", "by_group"] = "overall",
    bins: int = 10,
    control_stability: bool = False,
):
    """Modification of scikit-uplift weighted average uplift

        It is an average of uplift by percentile
        Weights are numbers of bins (from 1 to bins)
        Treatment response rate ia a target mean in the treatment group
        Control response rate is a target mean in the control group
        Uplift score is a difference between treatment response rate and control response rate

    Args:
        y_true (1d array-like): Correct (true) binary target values
        uplift (1d array-like): Predicted uplift, as returned by a model
        treatment (1d array-like): Treatment labels
        uplift_type (string, ['absolute', 'relative']): Determines the uplift
            calculating strategy. Default is 'absolute'
            * `'absolute'`:
                Just the difference between treatment and control response rate
            * `'relative'`:
                Proportion of treatment to control response rate

        strategy (string, ['overall', 'by_group']): Determines the calculating
            strategy. Default is 'overall'

            * `'overall'`:
                The first step is taking the first k observations of all test
                data ordered by uplift prediction (overall both groups - control
                and treatment) and conversions in treatment and control groups
                calculated only on them. Then the difference between these
                conversions is calculated

            * `'by_group'`:
                Separately calculates conversions in top k observations in each
                group (control and treatment) sorted by uplift predictions. Then
                the difference between these conversions is calculated

        bins (int): Determines а number of bins (and the relative percentile)
            in the test data. Default is 10
        control_stability (bool): Whether to include control response rate distribution
            by bins score. If true, a variation coefficient equal to the standard
            deviation of the control response rate divided by the average control
            response rate over all data is used to estimate the uniformity of the
            control response rate distribution. Then it is weighted harmonically
            (similar to F-score) with bin-weighted average uplift. Default is False

    Idea:
        Identify treatment-sensitive customers by, first, reducing the importance
        of last-bin uplift in metric calculation, and, second, taking into account
        the distribution of control response rate across bins (ideal is a uniform
        distribution, and for a propensity situation, decreasing distribution)

    Returns:
        float: Bin-weighted average uplift score

    Examples:
        >>> from AUF.metrics import bin_weighted_average_uplift
        >>> weighted_uplift = bin_weighted_average_uplift(target, uplift, treatment)
    """

    check_consistent_length(y_true, uplift, treatment)
    check_is_binary(treatment)
    check_is_binary(y_true)

    strategy_methods = ["overall", "by_group"]
    uplift_types = ["absolute", "relative"]

    n_samples = len(y_true)

    if strategy not in strategy_methods:
        raise ValueError(
            f"Response rate supports only calculating methods in {strategy_methods},"
            f" got {strategy}."
        )

    if uplift_type not in uplift_types:
        raise ValueError(
            f"Uplift supports only calculating methods in {uplift_types},"
            f" got {uplift_type}."
        )

    if uplift_type not in uplift_types:
        raise ValueError(
            f"Uplift supports only calculating methods in {uplift_types},"
            f" got {uplift_type}."
        )

    if not isinstance(bins, int) or bins <= 0:
        raise ValueError(
            f"Bins should be positive integer." f" Invalid value bins: {bins}"
        )

    if bins >= n_samples:
        raise ValueError(
            f"Number of bins = {bins} should be smaller than the length of y_true {n_samples}"
        )

    bins_response_rate_trmnt, bins_variance_trmnt, bins_n_trmnt = (
        response_rate_by_percentile(
            y_true, uplift, treatment, group="treatment", strategy=strategy, bins=bins
        )
    )

    bins_response_rate_ctrl, bins_variance_ctrl, bins_n_ctrl = (
        response_rate_by_percentile(
            y_true, uplift, treatment, group="control", strategy=strategy, bins=bins
        )
    )

    if uplift_type == "absolute":
        uplift_scores = bins_response_rate_trmnt - bins_response_rate_ctrl
        weighted_avg_uplift = np.dot(1 / np.arange(1, 1 + bins), uplift_scores)

    else:
        uplift_scores = bins_response_rate_trmnt / bins_response_rate_ctrl - 1
        weighted_avg_uplift = np.dot(1 / np.arange(1, 1 + bins), uplift_scores)
        weighted_avg_uplift = (weighted_avg_uplift - min(uplift_scores)) / (
            max(uplift_scores) - min(uplift_scores)
        )

    if control_stability:
        response_rate_ctrl_stability = 1 - np.std(bins_response_rate_ctrl)
        weighted_avg_uplift = (
            2 * response_rate_ctrl_stability * weighted_avg_uplift
        ) / (response_rate_ctrl_stability + weighted_avg_uplift)

    return weighted_avg_uplift


def calculate_control_target_averages(df: pd.DataFrame, bins: int = 10):
    """
    Calculate the average control response rate in the bin compared to the whole sample
    """

    bins_avg_cntrl_target = []
    bin_nums = list(range(1, bins + 1))

    for idx in range(1, bins):
        bins_avg_cntrl_target.append(
            df[(df["treatment"] == 0) & (df["bin"].isin(bin_nums[:idx]))][
                "target"
            ].mean()
        )

    avg_cntrl_target = df[df["treatment"] == 0]["target"].mean()
    bins_diff_cntrl_target = bins_avg_cntrl_target - avg_cntrl_target

    return bins_diff_cntrl_target


# TODO : rename function
#        returned value != uplift_rel / uplift_rel by bin
# TODO : rewrite docstring
#        returned value != cumulative uplift_rel since group by operation used
def calculate_relative_uplift(df: pd.DataFrame):
    """
    Calculate the average cumulative relative uplift in the all bins before
    the current one compared to the whole sample
    """

    bins_mean_target = df.groupby(["bin", "treatment"])["target"].mean().unstack()
    bins_mean_target.columns = ["mean_target_treatment_0", "mean_target_treatment_1"]

    bins_rel_uplift = (
        bins_mean_target["mean_target_treatment_1"]
        / bins_mean_target["mean_target_treatment_0"]
    )
    data_rel_uplift = (
        df[df["treatment"] == 1]["target"].mean()
        / df[df["treatment"] == 0]["target"].mean()
    )

    bins_rel_uplift_diff = bins_rel_uplift - data_rel_uplift

    return bins_rel_uplift_diff


def weighted_average_uplift_auc(
    y_true: tp.Sequence[float],
    uplift: tp.Sequence[float],
    treatment: tp.Sequence[float],
    bins: int = 10,
):
    """Harmonic weighted areas under the curves of control response rate and relative uplift

        Control response rate curve is the control response rate calculated by percentile bins,
        from which the control response rate for the whole sample is subtracted
        Relative uplift curve is the relative uplift calculated by percentile bins,
        from which the  relative uplift for the whole sample is subtracted
        Treatment response rate ia a target mean in the treatment group
        Control response rate is a target mean in the control group
        Uplift score is a difference between treatment response rate and control response rate

    Args:
        y_true (1d array-like): Correct (true) binary target values
        uplift (1d array-like): Predicted uplift, as returned by a model
        treatment (1d array-like): Treatment labels
        bins (int): Determines а number of bins (and the relative percentile)
            in the test data. Default is 10

    Idea:
        Identify treatment-sensitive customers by looking for each bin, first, at the change
        in the average control response rate in the bin compared to the whole sample, and second,
        at the change in the average cumulative relative uplift in the all bins before the current
        one compared to the whole sample

    Returns:
        float: Harmonic weighted control response rate and relative uplift AUCs score

    Examples:
        >>> from AUF.metrics import weighted_average_uplift_auc
        >>> weighted_uplift_auc = weighted_average_uplift_auc(target, uplift, treatment)
    """

    check_consistent_length(y_true, uplift, treatment)
    check_is_binary(y_true)
    check_is_binary(treatment)

    percentiles = np.arange(0, 1 + 1 / bins, 1 / bins)
    df = pd.DataFrame(
        {"target": y_true, "uplift": uplift, "treatment": treatment}
    ).sort_values(by="uplift", ascending=True)
    df["bin"] = pd.cut(
        df.uplift,
        bins=df.uplift.quantile(percentiles).values,
        labels=False,
        duplicates="drop",
    )
    df["bin"].fillna(0, inplace=True)
    df["bin"] = bins - df["bin"]

    bins_diff_cntrl_target = calculate_control_target_averages(df, bins)
    bins_rel_uplift_diff = calculate_relative_uplift(df)

    ctrl_target_auc = np.trapz(bins_diff_cntrl_target, dx=1)
    rel_uplift_auc = np.trapz(bins_rel_uplift_diff, dx=1)
    weighted_auc_uplift = (
        2 * (ctrl_target_auc * rel_uplift_auc) / (ctrl_target_auc + rel_uplift_auc)
    )

    return weighted_auc_uplift
