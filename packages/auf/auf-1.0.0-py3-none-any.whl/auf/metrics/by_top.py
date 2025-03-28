import typing as tp

import numpy as np
import pandas as pd
from sklearn.utils.validation import check_consistent_length
from sklift.metrics import qini_auc_score, response_rate_by_percentile
from sklift.utils import check_is_binary


def uplift_at_k(
    y_true: tp.Sequence[float],
    uplift: tp.Sequence[float],
    treatment: tp.Sequence[float],
    strategy: tp.Union["overall", "by_group"] = "overall",
    k: tp.Union[float, int] = 0.3,
    output_transform: tp.Callable = lambda x, y: x - y,
):
    """Scikit-uplift implementation that computes uplift at first k
        observations by uplift of the total sample with adding result
        divergence function for mean response rates

    Args:
        y_true (1d array-like): Correct (true) binary target values
        uplift (1d array-like): Predicted uplift, as returned by a model
        treatment (1d array-like): Treatment labels
        k (float or int): If float, should be between 0.0 and 1.0 and represent
            the proportion of the dataset to include in the computation of uplift
            If int, represents the absolute number of samples
        strategy (string, ['overall', 'by_group']): Determines the calculating strategy

            * `'overall'`:
                The first step is taking the first k observations of all test data
                ordered by uplift prediction (overall both groups - control and treatment)
                and conversions in treatment and control groups calculated only on them.
                Then the difference between these conversions is calculated.

            * `'by_group'`:
                Separately calculates conversions in top k observations in each group
                (control and treatment) sorted by uplift predictions. Then the difference
                between these conversions is calculated

        output_transform (bool): Function applied to treatment and control response rates
                before the return statement

    Returns:
        float: Uplift score at first k observations of the total sample

    Examples:
        >>> from AUF.metrics import uplift_at_k
        >>> uplift_20 = uplift_at_k(target, uplift, treatment, k=0.2)
    """

    # TODO: checker all groups is not empty
    check_consistent_length(y_true, uplift, treatment)
    check_is_binary(treatment)
    check_is_binary(y_true)
    y_true, uplift, treatment = np.array(y_true), np.array(uplift), np.array(treatment)

    strategy_methods = ["overall", "by_group"]
    if strategy not in strategy_methods:
        raise ValueError(
            f"Uplift score supports only calculating methods in {strategy_methods},"
            f" got {strategy}."
        )

    n_samples = len(y_true)
    order = np.argsort(uplift, kind="mergesort")[::-1]
    _, treatment_counts = np.unique(treatment, return_counts=True)
    n_samples_ctrl = treatment_counts[0]
    n_samples_trmnt = treatment_counts[1]

    k_type = np.asarray(k).dtype.kind

    if (
        k_type == "i"
        and (k >= n_samples or k <= 0)
        or k_type == "f"
        and (k <= 0 or k >= 1)
    ):
        raise ValueError(
            f"k={k} should be either positive and smaller"
            f" than the number of samples {n_samples} or a float in the "
            f"(0, 1) range"
        )

    if k_type not in ("i", "f"):
        raise ValueError(f"Invalid value for k: {k_type}")

    if strategy == "overall":
        if k_type == "f":
            n_size = int(n_samples * k)
        else:
            n_size = k

        # ToDo: _checker_ there are observations among two groups among first k
        score_ctrl = y_true[order][:n_size][treatment[order][:n_size] == 0].mean()
        score_trmnt = y_true[order][:n_size][treatment[order][:n_size] == 1].mean()

    else:
        if k_type == "f":
            n_ctrl = int((treatment == 0).sum() * k)
            n_trmnt = int((treatment == 1).sum() * k)

        else:
            n_ctrl = k
            n_trmnt = k

        if n_ctrl > n_samples_ctrl:
            raise ValueError(
                f"With k={k}, the number of the first k observations"
                " bigger than the number of samples"
                f"in the control group: {n_samples_ctrl}"
            )
        if n_trmnt > n_samples_trmnt:
            raise ValueError(
                f"With k={k}, the number of the first k observations"
                " bigger than the number of samples"
                f"in the treatment group: {n_samples_ctrl}"
            )

        score_ctrl = y_true[order][treatment[order] == 0][:n_ctrl].mean()
        score_trmnt = y_true[order][treatment[order] == 1][:n_trmnt].mean()

    return output_transform(score_trmnt, score_ctrl)


def qini_auc_score_clip(
    y_true: tp.Sequence[float],
    uplift: tp.Sequence[float],
    treatment: tp.Sequence[float],
    strategy: tp.Union["overall", "by_group"] = "overall",
    k: tp.Union[float, int] = 0.2,
    border_const: tp.Union[float, int] = 1.3,
):

    rel_all = uplift_at_k(
        y_true, uplift, treatment, strategy, 0.99, lambda x, y: x / y - 1
    )
    rel_k = uplift_at_k(y_true, uplift, treatment, strategy, k, lambda x, y: x / y - 1)
    if rel_k <= border_const * rel_all:
        return -1
    else:
        return qini_auc_score(y_true, uplift, treatment)


def control_treatment_ones_ratios_at_k(
    y_true: tp.Sequence[float],
    uplift: tp.Sequence[float],
    treatment: tp.Sequence[float],
    strategy: tp.Union["overall", "by_group"] = "overall",
    k: tp.Union[float, int] = 0.3,
):
    """Returns F1-score of ratios of treatment targets in top and control targets in bottom.

    Calculates F1-score of 2 numbers from 0 to 1:
        - ratio of treatment targets which are in chosen top of the sample by uplift
        - ratio of control targets which are out of chosen top of the sample by uplift

    Args:
        y_true (1d array-like): Correct (true) binary target values
        uplift (1d array-like): Predicted uplift, as returned by a model
        treatment (1d array-like): Treatment labels
        k (float or int): If float, should be between 0.0 and 1.0 and represent
            the proportion of the dataset to include in the computation of uplift
            If int, represents the absolute number of samples
        strategy (string, ['overall', 'by_group']): Determines the calculating strategy

            * `'overall'`:
                The first step is taking the first k observations of all test data
                ordered by uplift prediction (overall both groups - control and treatment)
                and conversions in treatment and control groups calculated only on them.
                Then the difference between these conversions is calculated.

            * `'by_group'`:
                Separately calculates conversions in top k observations in each group
                (control and treatment) sorted by uplift predictions. Then the difference
                between these conversions is calculated

    Returns:
        float: F1-score of 2 described numbers

    Examples:
        >>> from AUF.metrics import control_treatment_ones_ratios_at_k
        >>> score = control_treatment_ones_ratios_at_k(target, uplift, treatment, k=0.2)
    """

    # TODO: checker all groups is not empty
    check_consistent_length(y_true, uplift, treatment)
    check_is_binary(treatment)
    check_is_binary(y_true)
    y_true, uplift, treatment = np.array(y_true), np.array(uplift), np.array(treatment)

    strategy_methods = ["overall", "by_group"]
    if strategy not in strategy_methods:
        raise ValueError(
            f"Uplift score supports only calculating methods in {strategy_methods},"
            f" got {strategy}."
        )

    n_samples = len(y_true)
    order = np.argsort(uplift, kind="mergesort")[::-1]
    _, treatment_counts = np.unique(treatment, return_counts=True)
    n_samples_ctrl = treatment_counts[0]
    n_samples_trmnt = treatment_counts[1]

    k_type = np.asarray(k).dtype.kind

    if (
        k_type == "i"
        and (k >= n_samples or k <= 0)
        or k_type == "f"
        and (k <= 0 or k >= 1)
    ):
        raise ValueError(
            f"k={k} should be either positive and smaller"
            f" than the number of samples {n_samples} or a float in the "
            f"(0, 1) range"
        )

    if k_type not in ("i", "f"):
        raise ValueError(f"Invalid value for k: {k_type}")

    ones_ctrl = y_true[treatment == 0].sum()
    ones_trmnt = y_true[treatment == 1].sum()

    if strategy == "overall":
        if k_type == "f":
            n_size = int(n_samples * k)
        else:
            n_size = k

        down_ones_ctrl = y_true[order][n_size:][treatment[order][n_size:] == 0].sum()
        top_ones_trmnt = y_true[order][:n_size][treatment[order][:n_size] == 1].sum()

        score_ctrl = down_ones_ctrl / ones_ctrl
        score_trmnt = top_ones_trmnt / ones_trmnt

    else:
        if k_type == "f":
            n_ctrl = int((treatment == 0).sum() * k)
            n_trmnt = int((treatment == 1).sum() * k)
        else:
            n_ctrl = k
            n_trmnt = k

        if n_ctrl > n_samples_ctrl:
            raise ValueError(
                f"With k={k}, the number of the first k observations"
                " bigger than the number of samples"
                f"in the control group: {n_samples_ctrl}"
            )
        if n_trmnt > n_samples_trmnt:
            raise ValueError(
                f"With k={k}, the number of the first k observations"
                " bigger than the number of samples"
                f"in the treatment group: {n_samples_ctrl}"
            )

        down_ones_ctrl = y_true[order][treatment[order] == 0][n_ctrl:].sum()
        top_ones_trmnt = y_true[order][treatment[order] == 1][:n_trmnt].sum()

        score_ctrl = down_ones_ctrl / ones_ctrl
        score_trmnt = top_ones_trmnt / ones_trmnt

    # we want to have in top X% of samples sorted descending by uplift:
    # 1) big ratio of treatment targets
    # 2) little ratio of control targets
    # --> use F1-score (the aims are equally important)
    score = 2 * (score_ctrl * score_trmnt) / (score_ctrl + score_trmnt)
    return score


def abs_rel_uplift_growth_at_k(
    y_true: tp.Sequence[float],
    uplift: tp.Sequence[float],
    treatment: tp.Sequence[float],
    uplift_type: tp.Union["abs", "rel", "both"] = "both",
    strategy: tp.Union["overall", "by_group"] = "overall",
    k: tp.Union[float, int] = 0.3,
):
    """Returns relative growth of absolute or relative (or their total) uplift in top w.r.t. out of the top samples.

    Calculates one of the two numbers (or their sum):
        - absolute uplift for top k percent of sample divided by absolute uplift for other objects
        - relative uplift for top k percent of sample divided by relative uplift for other objects

    Args:
        y_true (1d array-like): Correct (true) binary target values
        uplift (1d array-like): Predicted uplift, as returned by a model
        treatment (1d array-like): Treatment labels
        k (float or int): If float, should be between 0.0 and 1.0 and represent
            the proportion of the dataset to include in the computation of uplift
            If int, represents the absolute number of samples
        strategy (string, ['overall', 'by_group']): Determines the calculating strategy

            * `'overall'`:
                The first step is taking the first k observations of all test data
                ordered by uplift prediction (overall both groups - control and treatment)
                and conversions in treatment and control groups calculated only on them.
                Then the difference between these conversions is calculated.

            * `'by_group'`:
                Separately calculates conversions in top k observations in each group
                (control and treatment) sorted by uplift predictions. Then the difference
                between these conversions is calculated

    Returns:
        float: described function of mean target rates in top and bottom samples in treatment and control groups

    Examples:
        >>> from AUF.metrics import abs_rel_uplift_growth_at_k
        >>> score = abs_rel_uplift_growth_at_k(target, uplift, treatment, k=0.2)
    """
    assert uplift_type in ["abs", "rel", "both"], f"{uplift_type}"

    # TODO: checker all groups is not empty
    check_consistent_length(y_true, uplift, treatment)
    check_is_binary(treatment)
    check_is_binary(y_true)
    y_true, uplift, treatment = np.array(y_true), np.array(uplift), np.array(treatment)

    strategy_methods = ["overall", "by_group"]
    if strategy not in strategy_methods:
        raise ValueError(
            f"Uplift score supports only calculating methods in {strategy_methods},"
            f" got {strategy}."
        )

    n_samples = len(y_true)
    order = np.argsort(uplift, kind="mergesort")[::-1]
    _, treatment_counts = np.unique(treatment, return_counts=True)
    n_samples_ctrl = treatment_counts[0]
    n_samples_trmnt = treatment_counts[1]

    k_type = np.asarray(k).dtype.kind

    if (
        k_type == "i"
        and (k >= n_samples or k <= 0)
        or k_type == "f"
        and (k <= 0 or k >= 1)
    ):
        raise ValueError(
            f"k={k} should be either positive and smaller"
            f" than the number of samples {n_samples} or a float in the "
            f"(0, 1) range"
        )

    if k_type not in ("i", "f"):
        raise ValueError(f"Invalid value for k: {k_type}")

    # tr_ctrl = y_true[treatment == 0].mean()
    # tr_trmnt = y_true[treatment == 1].mean()

    if strategy == "overall":
        if k_type == "f":
            n_size = int(n_samples * k)
        else:
            n_size = k

        tr_ctrl_top = y_true[order][:n_size][treatment[order][:n_size] == 0].mean()
        tr_trmnt_top = y_true[order][:n_size][treatment[order][:n_size] == 1].mean()

        tr_ctrl_bottom = y_true[order][n_size:][treatment[order][n_size:] == 0].mean()
        tr_trmnt_bottom = y_true[order][n_size:][treatment[order][n_size:] == 1].mean()

    else:
        if k_type == "f":
            n_ctrl = int((treatment == 0).sum() * k)
            n_trmnt = int((treatment == 1).sum() * k)
        else:
            n_ctrl = k
            n_trmnt = k

        if n_ctrl > n_samples_ctrl:
            raise ValueError(
                f"With k={k}, the number of the first k observations"
                " bigger than the number of samples"
                f"in the control group: {n_samples_ctrl}"
            )
        if n_trmnt > n_samples_trmnt:
            raise ValueError(
                f"With k={k}, the number of the first k observations"
                " bigger than the number of samples"
                f"in the treatment group: {n_samples_ctrl}"
            )

        tr_ctrl_top = y_true[order][treatment[order] == 0][:n_ctrl].mean()
        tr_trmnt_top = y_true[order][treatment[order] == 1][:n_trmnt].mean()

        tr_ctrl_bottom = y_true[order][treatment[order] == 0][n_ctrl:].mean()
        tr_trmnt_bottom = y_true[order][treatment[order] == 1][n_trmnt:].mean()

    abs_uplift_growth = (tr_trmnt_top - tr_ctrl_top) / (
        tr_trmnt_bottom - tr_ctrl_bottom
    )
    rel_uplift_growth = (tr_trmnt_top / tr_ctrl_top - 1) / (
        tr_trmnt_bottom / tr_ctrl_bottom - 1
    )

    if uplift_type == "abs":
        score = abs_uplift_growth
    elif uplift_type == "rel":
        score = rel_uplift_growth
    else:
        score = abs_uplift_growth + rel_uplift_growth

    return score
