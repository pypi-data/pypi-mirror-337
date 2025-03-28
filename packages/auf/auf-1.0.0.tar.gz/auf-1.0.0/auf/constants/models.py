from functools import partial
from itertools import chain

from catboost import CatBoostClassifier, CatBoostRegressor
from causalml.inference.tree import UpliftRandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklift.metrics import qini_auc_score
from sklift.models import SoloModel, TwoModels

from ..models import AufRandomForestClassifier, AufTreeClassifier, AufXLearner

RANDOM_STATE = 42

BOOTSTRAP_REPEATS = 300

BASE_MODEL = CatBoostClassifier(iterations=120, depth=3, learning_rate=0.1, silent=True)

SOLO_MODEL = SoloModel(
    estimator=CatBoostClassifier(
        iterations=120,
        depth=3,
        learning_rate=0.1,
        silent=True,
        random_state=RANDOM_STATE,
    )
)

TWO_MODEL = TwoModels(
    estimator_trmnt=CatBoostClassifier(
        iterations=120,
        depth=3,
        learning_rate=0.1,
        silent=True,
        random_state=RANDOM_STATE,
    ),
    estimator_ctrl=CatBoostClassifier(
        iterations=120,
        depth=3,
        learning_rate=0.1,
        silent=True,
        random_state=RANDOM_STATE,
    ),
)

UPLIFT_TREE = AufTreeClassifier(
    control_name="=",
    max_depth=3,
    max_features=7,
    random_state=RANDOM_STATE,
    min_samples_leaf=100,
    min_samples_treatment=10,
    n_reg=100,
    early_stopping_eval_diff_scale=1,
    evaluationFunction="KL",
    normalization=True,
    honesty=False,
    estimation_sample_size=0.5,
)

UPLIFT_FOREST = AufRandomForestClassifier(
    control_name="0",
    n_estimators=10,
    max_depth=3,
    max_features=7,
    random_state=RANDOM_STATE,
    min_samples_leaf=100,
    min_samples_treatment=10,
    n_reg=10,
    early_stopping_eval_diff_scale=1,
    evaluationFunction="KL",
    normalization=True,
    honesty=False,
    estimation_sample_size=0.5,
    n_jobs=-1,
    joblib_prefer="threads",
)

X_LEARNER = AufXLearner(
    model=CatBoostClassifier(
        iterations=120,
        depth=3,
        learning_rate=0.1,
        loss_function="Logloss",
        nan_mode="Min",
        random_seed=RANDOM_STATE,
        verbose=False,
    ),
    uplift_model=CatBoostRegressor(
        iterations=120,
        depth=3,
        learning_rate=0.1,
        loss_function="MAE",
        nan_mode="Min",
        random_state=RANDOM_STATE,
        verbose=False,
    ),
    map_groups={
        "control": 0,
        "treatment": 1,
    },
    features=None,
    cat_features=None,
    group_model=None,
)
