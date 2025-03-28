from functools import partial
from itertools import chain

from catboost import CatBoostClassifier, CatBoostRegressor
from causalml.inference.tree import UpliftRandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklift.metrics import qini_auc_score
from sklift.models import SoloModel, TwoModels

from ..metrics import (
    abs_rel_uplift_growth_at_k,
    bin_weighted_average_uplift,
    control_treatment_ones_ratios_at_k,
    qini_auc_score_clip,
    uplift_at_k,
)

METRICS_UPLIFT_AT_K = dict(
    {
        f"uplift@{k:02d}": partial(
            uplift_at_k,
            strategy="overall",
            k=k / 100,
            output_transform=lambda x, y: x - y,
        )
        for k in range(1, 100)
    }
)

METRICS_UPLIFT_REL_AT_K = dict(
    {
        f"uplift_rel@{k:02d}": partial(
            uplift_at_k,
            strategy="overall",
            k=k / 100,
            output_transform=lambda x, y: x / y - 1,
        )
        for k in range(1, 100)
    }
)

METRICS_WEIGHTED_UPLIFT = dict(
    {
        f"weighted_uplift_{k}_bins": partial(
            bin_weighted_average_uplift,
            uplift_type="absolute",
            strategy="overall",
            bins=k,
            control_stability=False,
        )
        for k in range(2, 100)
    }
)

METRICS_WEIGHTED_UPLIFT_STABLE = dict(
    {
        f"weighted_uplift_{k}_bins_stable": partial(
            bin_weighted_average_uplift,
            uplift_type="absolute",
            strategy="overall",
            bins=k,
            control_stability=True,
        )
        for k in range(2, 100)
    }
)

METRICS_WEIGHTED_UPLIFT_REL = dict(
    {
        f"weighted_relative_uplift_{k}_bins": partial(
            bin_weighted_average_uplift,
            uplift_type="relative",
            strategy="overall",
            bins=k,
            control_stability=False,
        )
        for k in range(2, 100)
    }
)

METRICS_WEIGHTED_UPLIFT_REL_STABLE = dict(
    {
        f"weighted_relative_uplift_{k}_bins_stable": partial(
            bin_weighted_average_uplift,
            uplift_type="relative",
            strategy="overall",
            bins=k,
            control_stability=True,
        )
        for k in range(2, 100)
    }
)

METRICS_CONTROL_TREATMENT_TARGET_RATIOS_AT_K = dict(
    {
        f"control_treatment_ones_ratios@{k:02d}": partial(
            control_treatment_ones_ratios_at_k, strategy="overall", k=k / 100
        )
        for k in range(1, 100)
    }
)

METRICS_ABS_UPLIFT_GROWTH_AT_K = dict(
    {
        f"abs_uplift_growth@{k:02d}": partial(
            abs_rel_uplift_growth_at_k, uplift_type="abs", strategy="overall", k=k / 100
        )
        for k in range(1, 100)
    }
)

METRICS_REL_UPLIFT_GROWTH_AT_K = dict(
    {
        f"rel_uplift_growth@{k:02d}": partial(
            abs_rel_uplift_growth_at_k, uplift_type="rel", strategy="overall", k=k / 100
        )
        for k in range(1, 100)
    }
)

METRICS_ABS_REL_UPLIFT_GROWTH_AT_K = dict(
    {
        f"abs_rel_uplift_growth@{k:02d}": partial(
            abs_rel_uplift_growth_at_k,
            uplift_type="both",
            strategy="overall",
            k=k / 100,
        )
        for k in range(1, 100)
    }
)

METRICS_OTHERS = dict(
    {
        "qini_auc": qini_auc_score,
    }
)

METRICS_OTHERS_MY = dict(
    {
        "qini_auc_20": qini_auc_score_clip,
    }
)

METRICS = dict(
    list(
        chain(
            METRICS_UPLIFT_AT_K.items(),
            METRICS_UPLIFT_REL_AT_K.items(),
            METRICS_WEIGHTED_UPLIFT.items(),
            METRICS_WEIGHTED_UPLIFT_STABLE.items(),
            METRICS_WEIGHTED_UPLIFT_REL.items(),
            METRICS_WEIGHTED_UPLIFT_REL_STABLE.items(),
            METRICS_CONTROL_TREATMENT_TARGET_RATIOS_AT_K.items(),
            METRICS_ABS_UPLIFT_GROWTH_AT_K.items(),
            METRICS_REL_UPLIFT_GROWTH_AT_K.items(),
            METRICS_ABS_REL_UPLIFT_GROWTH_AT_K.items(),
            METRICS_OTHERS.items(),
            METRICS_OTHERS_MY.items(),
        )
    )
)
