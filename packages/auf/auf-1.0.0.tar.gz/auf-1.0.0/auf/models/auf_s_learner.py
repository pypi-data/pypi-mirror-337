import warnings

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.utils.multiclass import type_of_target
from sklearn.utils.validation import check_consistent_length
from sklift.utils import check_is_binary

"""S-learner with mulltitreatment

1) multitreatment = treatment flag as a categorical feature
2) uplift prediction = uplift for every treatment
3) is treatment interaction approach possible?
        {feats} -> {feats_T_1} + {feats_T_2} + ...
        {feats_T_1} = {feature * T_1_flag for feature in feats}
        10 treatments --> 2_000 feats = 20_000 feats...
4) trmnt_preds_ & ctrl_preds_ == ? dict[treat, proba]?
5) 
"""


class AufSoloModel(BaseEstimator):
    """aka Treatment Dummy approach, or Single model approach, or S-Learner.

    Fit solo model on whole dataset with 'treatment' as an additional feature.

    Each object from the test sample is scored twice: with the communication flag equal to 1 and equal to 0.
    Subtracting the probabilities for each observation, we get the uplift.

    Return delta of predictions for each example.

    Read more in the :ref:`User Guide <SoloModel>`.

    Args:
        estimator (estimator object implementing 'fit'): The object to use to fit the data.
        method (string, ’dummy’ or ’treatment_interaction’, default='dummy'): Specifies the approach:

            * ``'dummy'``:
                Single model;
            * ``'treatment_interaction'``:
                Single model including treatment interactions.

    Attributes:
        trmnt_preds_ (array-like, shape (n_samples, )): Estimator predictions on samples when treatment.
        ctrl_preds_ (array-like, shape (n_samples, )): Estimator predictions on samples when control.

    Example::

        # import approach
        from auf.models import AufSoloModel
        # import any estimator adheres to scikit-learn conventions
        from catboost import CatBoostClassifier


        asm = AufSoloModel(CatBoostClassifier(verbose=100, random_state=777))  # define approach
        asm = asm.fit(X_train, y_train, treat_train, estimator_fit_params={{'plot': True})  # fit the model
        uplift_asm = asm.predict(X_val)  # predict uplift

    References (binary treatment):
        Lo, Victor. (2002). The True Lift Model - A Novel Data Mining Approach to Response Modeling
        in Database Marketing. SIGKDD Explorations. 4. 78-86.

    See Also:

        **Other approaches:**

        * :class:`.ClassTransformation`: Class Variable Transformation approach.
        * :class:`.ClassTransformationReg`: Transformed Outcome approach.
        * :class:`.TwoModels`: Double classifier approach.

        **Other:**

        * :func:`.plot_uplift_preds`: Plot histograms of treatment, control and uplift predictions.
    """

    def __init__(self, estimator, method="dummy"):
        self.estimator = estimator
        self.method = method
        self.trmnt_preds_ = None
        self.ctrl_preds_ = None
        self._type_of_target = None

        self._treatment_values = None
        self._control_group = None

        all_methods = ["dummy", "treatment_interaction"]
        if method not in all_methods:
            raise ValueError(
                "SoloModel approach supports only methods in %s, got"
                " %s." % (all_methods, method)
            )

    def _preprocess_data(self, X, treatment):
        if self.method == "dummy":
            if isinstance(X, np.ndarray):
                X_mod = np.column_stack((X, treatment))
            elif isinstance(X, pd.DataFrame):
                X_mod = X.assign(treatment=treatment)
            else:
                raise TypeError(
                    "Expected numpy.ndarray or pandas.DataFrame in training vector X, got %s"
                    % type(X)
                )

        if self.method == "treatment_interaction":
            # TODO : add features * indicators(treatment == T_i)
            X_mod = X.copy()

            for treatment_id in sorted(self._treatment_values):
                if treatment_id == self._control_group:
                    continue

                if isinstance(X_mod, np.ndarray):
                    X_mod = np.column_stack(
                        (
                            X_mod,
                            np.multiply(
                                X, np.array(treatment == treatment_id).reshape(-1, 1)
                            ),
                            # treatment
                        )
                    )
                elif isinstance(X_mod, pd.DataFrame):
                    X_mod = pd.concat(
                        [
                            X_mod,
                            X.apply(lambda x: x * (treatment == treatment_id)).rename(
                                columns=lambda x: str(x)
                                + f"_{treatment_id}"
                                + "_treatment_interaction"
                            ),
                        ],
                        axis=1,
                    )
                    # .assign(treatment=treatment)
                else:
                    raise TypeError(
                        "Expected numpy.ndarray or pandas.DataFrame in training vector X, got %s"
                        % type(X)
                    )

            if isinstance(X_mod, np.ndarray):
                X_mod = np.column_stack((X_mod, treatment))
            elif isinstance(X_mod, pd.DataFrame):
                X_mod = X_mod.assign(treatment=treatment)

        return X_mod

    def fit(self, X, y, treatment, control_group, estimator_fit_params=None):
        """Fit the model according to the given training data.

        For each test example calculate predictions on new set twice: by the first and second models.
        After that calculate uplift as a delta between these predictions.

        Return delta of predictions for each example.

        Args:
            X (array-like, shape (n_samples, n_features)): Training vector, where n_samples is the number of
                samples and n_features is the number of features.
            y (array-like, shape (n_samples,)): Binary target vector relative to X.
            treatment (array-like, shape (n_samples,)): Binary treatment vector relative to X.
            estimator_fit_params (dict, optional): Parameters to pass to the fit method of the estimator.

        Returns:
            object: self
        """

        check_consistent_length(X, y, treatment)
        # check_is_binary(treatment)
        treatment_values = np.unique(treatment)

        self._treatment_values = treatment_values.copy()
        self._control_group = control_group

        # now we expect any treatment groups number except 1
        # if len(treatment_values) != 2:
        #     raise ValueError("Expected only two unique values in treatment vector, got %s" % len(treatment_values))
        if len(treatment_values) == 1:
            raise ValueError("Expected more than one unique values in treatment vector")

        X_mod = self._preprocess_data(X, treatment)

        self._type_of_target = type_of_target(y)

        if estimator_fit_params is None:
            estimator_fit_params = {}
        self.estimator.fit(X_mod, y, **estimator_fit_params)
        return self

    def predict(self, X):
        """Perform uplift on samples in X.

        Args:
            X (array-like, shape (n_samples, n_features)): Training vector, where n_samples is the number of samples
                and n_features is the number of features.

        Returns:
            array (shape (n_samples,)): uplift
        """

        self._preds = {}

        for treatment_id in sorted(self._treatment_values):
            treatment = np.full(X.shape[0], treatment_id)
            X_mod = self._preprocess_data(X, treatment)

            if self._type_of_target == "binary":
                self._preds[treatment_id] = self.estimator.predict_proba(X_mod)[:, 1]
            else:
                self._preds[treatment_id] = self.estimator.predict(X_mod)

        uplifts = {}

        for treatment_id in sorted(self._treatment_values):
            if treatment_id == self._control_group:
                continue
            uplifts[treatment_id] = (
                self._preds[treatment_id] - self._preds[self._control_group]
            )

        return uplifts
