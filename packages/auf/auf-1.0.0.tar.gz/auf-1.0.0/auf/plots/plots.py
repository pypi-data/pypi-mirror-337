import typing as tp

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.utils.validation import check_consistent_length
from sklift.metrics import uplift_by_percentile
from sklift.utils import check_is_binary

from auf.constants import RANDOM_STATE

plt.style.use("default")


def plot_uplift_by_percentile(
    y_true,
    uplift,
    treatment,
    strategy="overall",
    kind="line",
    bins=10,
    string_percentiles=True,
    axes=None,
    draw_bars="both",
):
    """Scikit-uplift implementation with 2 modifications:
        1. add axes parameter
        2. add flag for drawing only one of bar plots : with uplift or with response rates

    Args:
        y_true (1d array-like): Correct (true) binary target values
        uplift (1d array-like): Predicted uplift, as returned by a model
        treatment (1d array-like): Treatment labels
        strategy (string, ['overall', 'by_group']): Determines the calculating strategy. Default is 'overall'

            * ``'overall'``:
                The first step is taking the first k observations of all test data ordered by uplift prediction
                (overall both groups - control and treatment) and conversions in treatment and control groups
                calculated only on them. Then the difference between these conversions is calculated
            * ``'by_group'``:
                Separately calculates conversions in top k observations in each group (control and treatment)
                sorted by uplift predictions. Then the difference between these conversions is calculated

        kind (string, ['line', 'bar']): The type of plot to draw. Default is 'line'

            * ``'line'``:
                Generates a line plot
            * ``'bar'``:
                Generates a traditional bar-style plot

        bins (int): Determines а number of bins (and the relative percentile) in the test data. Default is 10
        string_percentiles (bool): type of xticks: float or string to plot. Default is True (string)
        axes: axes obtained from matplotlib.pyplot.subplots
        draw_bars (string, ['both', 'uplift', 'rates']): a parameter to be divided into bins and
            plotted on the graph. Default is 'both'

    Returns:
        Object that stores computed values.
    """

    strategy_methods = ["overall", "by_group"]
    kind_methods = ["line", "bar"]

    check_consistent_length(y_true, uplift, treatment)
    check_is_binary(treatment)
    check_is_binary(y_true)
    n_samples = len(y_true)

    if strategy not in strategy_methods:
        raise ValueError(
            f"Response rate supports only calculating methods in {strategy_methods},"
            f" got {strategy}."
        )

    if kind not in kind_methods:
        raise ValueError(
            f"Function supports only types of plots in {kind_methods}," f" got {kind}."
        )

    if not isinstance(bins, int) or bins <= 0:
        raise ValueError(f"Bins should be positive integer. Invalid value bins: {bins}")

    if bins >= n_samples:
        raise ValueError(
            f"Number of bins = {bins} should be smaller than the length of y_true {n_samples}"
        )

    if not isinstance(string_percentiles, bool):
        raise ValueError(
            f"string_percentiles flag should be bool: True or False."
            f" Invalid value string_percentiles: {string_percentiles}"
        )

    df = uplift_by_percentile(
        y_true,
        uplift,
        treatment,
        strategy=strategy,
        std=True,
        total=False,
        bins=bins,
        string_percentiles=False,
    )

    percentiles = df.index[:bins].values.astype(float)

    response_rate_trmnt = df.loc[percentiles, "response_rate_treatment"].values
    std_trmnt = df.loc[percentiles, "std_treatment"].values

    response_rate_ctrl = df.loc[percentiles, "response_rate_control"].values
    std_ctrl = df.loc[percentiles, "std_control"].values

    uplift_score = df.loc[percentiles, "uplift"].values
    std_uplift = df.loc[percentiles, "std_uplift"].values

    # uplift_weighted_avg = df.loc['total', 'uplift']

    check_consistent_length(
        percentiles,
        response_rate_trmnt,
        response_rate_ctrl,
        uplift_score,
        std_trmnt,
        std_ctrl,
        std_uplift,
    )

    if kind == "line":
        if axes is None:
            _, axes = plt.subplots(ncols=1, nrows=1, figsize=(8, 6))
        axes.errorbar(
            percentiles,
            response_rate_trmnt,
            yerr=std_trmnt,
            linewidth=2,
            color="forestgreen",
            label="treatment\nresponse rate",
        )
        axes.errorbar(
            percentiles,
            response_rate_ctrl,
            yerr=std_ctrl,
            linewidth=2,
            color="orange",
            label="control\nresponse rate",
        )
        axes.errorbar(
            percentiles,
            uplift_score,
            yerr=std_uplift,
            linewidth=2,
            color="red",
            label="uplift",
        )
        axes.fill_between(
            percentiles, response_rate_trmnt, response_rate_ctrl, alpha=0.1, color="red"
        )

        if np.amin(uplift_score) < 0:
            axes.axhline(y=0, color="black", linewidth=1)

        if string_percentiles:  # string percentiles for plotting
            percentiles_str = [f"0-{percentiles[0]:.0f}"] + [
                f"{percentiles[i]:.0f}-{percentiles[i + 1]:.0f}"
                for i in range(len(percentiles) - 1)
            ]
            axes.set_xticks(percentiles)
            axes.set_xticklabels(percentiles_str, rotation=45)
        else:
            axes.set_xticks(percentiles)

        axes.legend(loc="upper right")
        axes.set_title(f"Uplift by percentile\n")
        axes.set_xlabel("Percentile")
        axes.set_ylabel("Uplift = treatment response rate - control response rate")

    elif draw_bars == "both":  # kind == 'bar'
        delta = percentiles[0]

        # don't check axes if None : draw both plots on big figure
        fig, axes = plt.subplots(
            ncols=1, nrows=2, figsize=(8, 6), sharex=True, sharey=True
        )
        fig.text(
            0.04,
            0.5,
            "Uplift = treatment response rate - control response rate",
            va="center",
            ha="center",
            rotation="vertical",
        )

        axes[1].bar(
            np.array(percentiles) - delta / 6,
            response_rate_trmnt,
            delta / 3,
            yerr=std_trmnt,
            color="forestgreen",
            label="treatment\nresponse rate",
        )
        axes[1].bar(
            np.array(percentiles) + delta / 6,
            response_rate_ctrl,
            delta / 3,
            yerr=std_ctrl,
            color="orange",
            label="control\nresponse rate",
        )
        axes[0].bar(
            np.array(percentiles),
            uplift_score,
            delta / 1.5,
            yerr=std_uplift,
            color="red",
            label="uplift",
        )

        axes[0].legend(loc="upper right")
        axes[0].tick_params(axis="x", bottom=False)
        axes[0].axhline(y=0, color="black", linewidth=1)
        axes[0].set_title(f"Uplift by percentile\n")

        if string_percentiles:  # string percentiles for plotting
            percentiles_str = [f"0-{percentiles[0]:.0f}"] + [
                f"{percentiles[i]:.0f}-{percentiles[i + 1]:.0f}"
                for i in range(len(percentiles) - 1)
            ]
            axes[1].set_xticks(percentiles)
            axes[1].set_xticklabels(percentiles_str, rotation=45)

        else:
            axes[1].set_xticks(percentiles)

        axes[1].legend(loc="upper right")
        axes[1].axhline(y=0, color="black", linewidth=1)
        axes[1].set_xlabel("Percentile")
        axes[1].set_title("Response rate by percentile")

    elif draw_bars == "uplift":  # kind == 'bar'
        delta = percentiles[0]

        if axes is None:
            fig, axes = plt.subplots(
                ncols=1, nrows=1, figsize=(5, 5), sharex=True, sharey=True
            )
        fig.text(
            0.04,
            0.5,
            "Uplift = treatment response rate - control response rate",
            va="center",
            ha="center",
            rotation="vertical",
        )

        axes.bar(
            np.array(percentiles),
            uplift_score,
            delta / 1.5,
            yerr=std_uplift,
            color="red",
            label="uplift",
        )

        axes.legend(loc="upper right")
        axes.tick_params(axis="x", bottom=False)
        axes.axhline(y=0, color="black", linewidth=1)
        axes.set_title(f"Uplift by percentile\n")

    elif draw_bars == "rates":  # kind == 'bar'
        delta = percentiles[0]

        if axes is None:
            fig, axes = plt.subplots(
                ncols=1, nrows=1, figsize=(5, 5), sharex=True, sharey=True
            )
            fig.text(
                0.04,
                0.5,
                "Uplift = treatment response rate - control response rate",
                va="center",
                ha="center",
                rotation="vertical",
            )

        axes.bar(
            np.array(percentiles) - delta / 6,
            response_rate_trmnt,
            delta / 3,
            yerr=std_trmnt,
            color="forestgreen",
            label="treatment\nresponse rate",
        )
        axes.bar(
            np.array(percentiles) + delta / 6,
            response_rate_ctrl,
            delta / 3,
            yerr=std_ctrl,
            color="orange",
            label="control\nresponse rate",
        )

        if string_percentiles:  # string percentiles for plotting
            percentiles_str = [f"0-{percentiles[0]:.0f}"] + [
                f"{percentiles[i]:.0f}-{percentiles[i + 1]:.0f}"
                for i in range(len(percentiles) - 1)
            ]
            axes.set_xticks(percentiles)
            axes.set_xticklabels(percentiles_str, rotation=45)

        else:
            axes.set_xticks(percentiles)

        axes.legend(loc="upper right")
        axes.axhline(y=0, color="black", linewidth=1)
        axes.set_xlabel("Percentile")
        axes.set_title("Response rate by percentile")

    return axes


def plot_portrait_tree(
    x: pd.DataFrame,
    uplift: np.array,
    feature_names_dict: tp.Optional[tp.Dict[str, str]] = None,
    max_depth: int = 3,
    max_leaf_nodes: int = 6,
    min_samples_leaf: tp.Union[float, int] = 0.05,
    axes=None,
):
    """Builds a portrait of a high- and low-uplift clients using a decision tree

    Args:
        x (pd.DataFrame): sample with features on which the uplift model was trained
        uplift (1d array-like): predicted uplift, as returned by a model
        feature_names_dict (dict): dictionary of matching feature names, where
            keys are names of features in the data and values are names of
            features to be displayed in the plot
        max_depth (int): the maximum depth of the tree. Default is 3
        max_leaf_nodes (int): grow a tree with ``max_leaf_nodes`` in best-first
            fashion. Best nodes are defined as relative reduction in impurity. Default is 6
        min_samples_leaf (float or int): the minimum number of samples required
            to be at a leaf node. A split point at any depth will only be
            considered if it leaves at least ``min_samples_leaf`` training
            samples in each of the left and right branches. Default is 0.05

            - If int, then consider `min_samples_leaf` as the minimum number
            - If float, then `min_samples_leaf` is a fraction and
              `ceil(min_samples_leaf * n_samples)` are the minimum
              number of samples for each node
        axes: axes obtained from matplotlib.pyplot.subplots

    Idea:
        Train the decision tree on the same features as the uplift model,
        passing the uplift predicted by the uplift model as a target.
        Visualize the decision tree and see how it separates high- from
        low-uplift clients

    Returns:
        None
    """
    check_consistent_length(x, uplift)

    # encoder = OrdinalEncoder()
    # x_transformed = pd.DataFrame(encoder.fit_transform(x), columns=x.columns)

    # max_num_len = len(str(int(x_transformed.max(axis=None).max())))
    # x_transformed.fillna(int('9' * max_num_len), inplace=True)

    if isinstance(min_samples_leaf, float):
        min_samples_leaf = int(min_samples_leaf * len(x))

    if feature_names_dict:
        feats = [
            feature_names_dict[col] if col in feature_names_dict else col
            for col in x.columns
        ]
    else:
        feats = x.columns

    tree = DecisionTreeRegressor(
        max_depth=max_depth,
        max_leaf_nodes=max_leaf_nodes,
        min_samples_leaf=min_samples_leaf,
        random_state=RANDOM_STATE,
    )

    # tree.fit(x_transformed, uplift)
    tree.fit(x, uplift)

    fig = None
    if axes is None:
        fig, axes = plt.subplots(1, 1, figsize=(12, 8))

    plot_tree(tree, filled=True, feature_names=feats, ax=axes)

    plt.title("Client portrait: uplift depending on model features")
    plt.tight_layout()
    plt.show()
    return fig


def plot_uplift_by_feature_bins(
    feature: tp.Sequence[float],
    treatment: tp.Sequence[float],
    target: tp.Sequence[float],
    feature_name: str,
    amount_of_bins: int = 7,
    round_const: int = 2,
    axes=None,
):
    """Make plots of the distribution of the number of observations and mean target
       depending on the treatment type and feature bin

    Args:
        feature (1d array-like): feature values which values from 0.02 to 0.98
            percentile will be divided into bins and depending on the
            bin of which the graph is plotted
        treatment (1d array-like): treatment labels
        target (1d array-like): correct (true) binary target values
        feature_name (str, optional): feature name depending on the bin of
            which the graph is plotted
        amount_of_bins (int): number of bins into which the attribute will be
            divided. Default is 7
        round_const (int): number of digits after decimal point to which the
            values of numerical signs are rounded off. Default is 2
        axes: axes obtained from matplotlib.pyplot.subplots

    Returns:
        None
    """
    check_consistent_length(feature, treatment, target)

    if feature_name is None:
        feature_name = "feature"
    df = pd.DataFrame({feature_name: feature, "target": target, "treatment": treatment})

    amount_of_nans = df.loc[df[feature_name].isna()].shape[0]

    if df[feature_name].dtype == "object":
        category_counts = (
            df[feature_name]
            .value_counts(dropna=False)
            .nlargest(amount_of_bins)
            .index.tolist()
        )

        if df[feature_name].nunique() > amount_of_bins:
            category_counts.pop()

            if amount_of_nans > 0 and np.nan not in category_counts:
                category_counts.pop()

            category_counts.append(np.nan)
            category_counts.append("Other")

        df[feature_name] = df[feature_name].apply(
            lambda x: x if x in category_counts or pd.isna(x) else "Other"
        )

        if amount_of_nans > 0:
            df[feature_name] = (
                pd.Categorical(df[feature_name], categories=category_counts)
                .add_categories("NAN")
                .fillna("NAN")
            )
            df[feature_name] = df[feature_name].cat.reorder_categories(
                ["NAN"] + category_counts
            )
        else:
            df[feature_name] = pd.Categorical(
                df[feature_name], categories=category_counts
            )

    else:
        if amount_of_bins > df[feature_name].dropna().unique().shape[0]:
            df[feature_name] = df[feature_name].astype("object")
            sort_hist_by_object_cnt = False

        bins = np.linspace(
            df[feature_name].quantile(q=0.02),
            df[feature_name].quantile(q=0.98),
            amount_of_bins,
        )
        df = df.loc[
            (df[feature_name] >= df[feature_name].quantile(q=0.02))
            & (df[feature_name] <= df[feature_name].quantile(q=0.98))
            | (df[feature_name].isna())
        ]

        feature_cat = pd.cut(
            x=df[feature_name],
            bins=bins,
            precision=round_const,
            include_lowest=True,
            ordered=True,
        )

        interval_labels = [
            f"{intv.left:.{round_const}f} - {intv.right:.{round_const}f}"
            for intv in feature_cat.cat.categories
        ]

        category_mapping = {
            old: new for old, new in zip(feature_cat.cat.categories, interval_labels)
        }

        # Модифицированная часть: добавляем NAN только при необходимости
        if amount_of_nans > 0:
            df[feature_name] = (
                feature_cat.map(category_mapping)
                .cat.rename_categories(interval_labels)
                .cat.add_categories("NAN")
                .fillna("NAN")
            )
            categories_order = ["NAN"] + interval_labels
        else:
            df[feature_name] = feature_cat.map(category_mapping).cat.rename_categories(
                interval_labels
            )
            categories_order = interval_labels

        df[feature_name] = df[feature_name].cat.reorder_categories(categories_order)

    grouped = (
        df.groupby([feature_name, "treatment"])
        .agg(count=("target", "size"), mean_target=("target", "mean"))
        .reset_index()
    )

    if df[feature_name].dtype == "object":
        grouped.sort_values(by="count", inplace=True, ascending=False)

        if amount_of_nans > 0:
            nan_mask = grouped[feature_name] == "NAN"
            grouped = pd.concat(
                [grouped[nan_mask], grouped[~nan_mask]], ignore_index=True
            )

        other_mask = grouped[feature_name] == "Other"
        grouped = pd.concat(
            [grouped[~other_mask], grouped[other_mask]], ignore_index=True
        )

    else:
        grouped[feature_name] = pd.Categorical(
            grouped[feature_name],
            categories=df[feature_name].cat.categories,
            ordered=True,
        )
        grouped = grouped.sort_values(feature_name)

    treatment_1 = grouped[grouped["treatment"] == 1]
    treatment_0 = grouped[grouped["treatment"] == 0]

    fig = None
    if axes is None:
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    ax1 = axes[0]
    width = 0.35  # Ширина столбцов
    x1 = np.arange(len(treatment_1[feature_name]))
    x0 = x1 + width

    ax1.bar(
        x1,
        treatment_1["count"],
        width,
        color="forestgreen",
        edgecolor="black",
        label="Treatment",
    )
    ax1.bar(
        x0,
        treatment_0["count"],
        width,
        color="orange",
        edgecolor="black",
        label="Control",
    )

    ax1.set_title("Treatment and control group sizes")
    # ax1s.set_xlabel("Bin")
    # ax1.set_xlabel(feature_name)
    ax1.set_ylabel("Number of observations")
    ax1.set_xticks(x1 + width / 2)
    ax1.set_xticklabels(treatment_1[feature_name])
    ax1.legend(loc="upper right")

    ax2 = axes[1]
    ax2.plot(
        treatment_1[feature_name],
        treatment_1["mean_target"],
        color="forestgreen",
        label="Treatment\ntarget rate",  # "Treatment 1",
        marker="o",
    )
    ax2.plot(
        treatment_0[feature_name],
        treatment_0["mean_target"],
        color="orange",
        label="Control\ntarget rate",  # "Treatment 0",
        marker="o",
    )
    ax2.set_title(f"Uplift")
    # ax2.set_xlabel("Bin")
    # ax2.set_xlabel(feature_name)
    # ax2.set_ylabel("Average target")
    ax2.legend(loc="upper right")

    fig.suptitle(f"Uplift and observations count by {feature_name} buckets")

    for ax in axes:
        ax.tick_params(axis="x", rotation=45)

    return fig
