import typing as tp
from dataclasses import dataclass

import numpy as np
import optuna
import pandas as pd
from catboost import CatBoostClassifier, CatBoostRegressor
from causalml.inference.tree import UpliftRandomForestClassifier
from sklearn.pipeline import Pipeline
from sklift.models import SoloModel, TwoModels

from ..constants import (
    RANDOM_STATE,
    SOLO_MODEL,
    TWO_MODEL,
    UPLIFT_FOREST,
    UPLIFT_TREE,
    X_LEARNER,
)
from ..models import AufRandomForestClassifier, AufTreeClassifier, AufXLearner

# from functools import partical


@dataclass
class ModelResult:
    estimator: Pipeline
    features: tp.List[str]
    uplift_prediction_type: str  # same on training & prediction
    median_test_metric_value: float


class OptuneUpliftDefault:
    "Find the best parameters for a given model class using a user-supplied metric for optimization"

    def __init__(
        self,
        df_train: pd.DataFrame,
        df_valid: pd.DataFrame,
        metric: object,
        treatment_col: str,
        target_col: str,
        overfit_metric: object,
        uplift_type: str,
    ):
        self.df_train = df_train
        self.df_valid = df_valid
        self.metric = metric
        self.treatment_col = treatment_col
        self.target_col = target_col
        self.overfit_metric = overfit_metric
        self.uplift_type = uplift_type

    def objective_slearner(self, trial):
        param = {
            "objective": trial.suggest_categorical(
                "objective", ["Logloss", "CrossEntropy"]
            ),
            "depth": trial.suggest_int("depth", 1, 8),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
            "n_estimators": trial.suggest_int("n_estimators", 30, 240),
            "boosting_type": trial.suggest_categorical(
                "boosting_type", ["Ordered", "Plain"]
            ),
            "bootstrap_type": trial.suggest_categorical(
                "bootstrap_type", ["Bayesian", "Bernoulli", "MVS"]
            ),
        }

        if param["bootstrap_type"] == "Bayesian":
            param["bagging_temperature"] = trial.suggest_float(
                "bagging_temperature", 0, 10
            )
        elif param["bootstrap_type"] == "Bernoulli":
            param["subsample"] = trial.suggest_float("subsample", 0.1, 1)
        solo_method = trial.suggest_categorical(
            "method", ["dummy", "treatment_interaction"]
        )

        # Создание и обучение модели
        estimator = CatBoostClassifier(random_state=RANDOM_STATE, silent=True, **param)
        model = self.model_class(method=solo_method, estimator=estimator)

        model.fit(
            X=self.df_train[self.features],
            y=self.df_train[self.target_col],
            treatment=self.df_train[self.treatment_col],
        )
        uplift_valid = model.predict(self.df_valid[self.features])
        if self.uplift_type == "rel":
            uplift_valid = model.trmnt_preds_ / model.ctrl_preds_

        metric_result = self.metric(
            y_true=self.df_valid[self.target_col],
            uplift=uplift_valid,
            treatment=self.df_valid[self.treatment_col],
        )
        if self.overfit_metric is not None:
            uplift_train = model.predict(self.df_train[self.features])
            if self.uplift_type == "rel":
                uplift_train = model.trmnt_preds_ / model.ctrl_preds_

            metric_result_train = self.metric(
                y_true=self.df_train[self.target_col],
                uplift=uplift_train,
                treatment=self.df_train[self.treatment_col],
            )
            return self.overfit_metric(metric_result, metric_result_train)

        return metric_result

    def objective_tlearner(self, trial):
        param = {
            "objective": trial.suggest_categorical(
                "objective", ["Logloss", "CrossEntropy"]
            ),
            "depth": trial.suggest_int("depth", 1, 8),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
            "n_estimators": trial.suggest_int("n_estimators", 30, 240),
            "boosting_type": trial.suggest_categorical(
                "boosting_type", ["Ordered", "Plain"]
            ),
            "bootstrap_type": trial.suggest_categorical(
                "bootstrap_type", ["Bayesian", "Bernoulli", "MVS"]
            ),
        }

        if param["bootstrap_type"] == "Bayesian":
            param["bagging_temperature"] = trial.suggest_float(
                "bagging_temperature", 0, 10
            )
        elif param["bootstrap_type"] == "Bernoulli":
            param["subsample"] = trial.suggest_float("subsample", 0.1, 1)

        param2 = {
            "objective": trial.suggest_categorical(
                "objective2", ["Logloss", "CrossEntropy"]
            ),
            "depth": trial.suggest_int("depth2", 1, 8),
            "learning_rate": trial.suggest_float("learning_rate2", 0.01, 0.3),
            "n_estimators": trial.suggest_int("n_estimators2", 30, 240),
            "boosting_type": trial.suggest_categorical(
                "boosting_type2", ["Ordered", "Plain"]
            ),
            "bootstrap_type": trial.suggest_categorical(
                "bootstrap_type2", ["Bayesian", "Bernoulli", "MVS"]
            ),
        }

        if param2["bootstrap_type"] == "Bayesian":
            param2["bagging_temperature"] = trial.suggest_float(
                "bagging_temperature2", 0, 10
            )
        elif param2["bootstrap_type"] == "Bernoulli":
            param2["subsample"] = trial.suggest_float("subsample2", 0.1, 1)
        two_method = trial.suggest_categorical(
            "method", ["vanilla", "ddr_control", "ddr_treatment"]
        )

        # Создание и обучение модели
        estimator = CatBoostClassifier(random_state=RANDOM_STATE, silent=True, **param)
        estimator2 = CatBoostClassifier(
            random_state=RANDOM_STATE, silent=True, **param2
        )
        model = self.model_class(
            method=two_method, estimator_trmnt=estimator, estimator_ctrl=estimator2
        )

        model.fit(
            X=self.df_train[self.features],
            y=self.df_train[self.target_col],
            treatment=self.df_train[self.treatment_col],
        )

        uplift_valid = model.predict(self.df_valid[self.features])
        if self.uplift_type == "rel":
            uplift_valid = model.trmnt_preds_ / model.ctrl_preds_

        metric_result = self.metric(
            y_true=self.df_valid[self.target_col],
            uplift=uplift_valid,
            treatment=self.df_valid[self.treatment_col],
        )
        if self.overfit_metric is not None:
            uplift_train = model.predict(self.df_train[self.features])
            if self.uplift_type == "rel":
                uplift_train = model.trmnt_preds_ / model.ctrl_preds_

            metric_result_train = self.metric(
                y_true=self.df_train[self.target_col],
                uplift=uplift_train,
                treatment=self.df_train[self.treatment_col],
            )
            return self.overfit_metric(metric_result, metric_result_train)

        return metric_result

    def objective_tree(self, trial):
        param = {
            "max_depth": trial.suggest_int("max_depth", 1, 10),
            "max_features": trial.suggest_int(
                "max_features", 2, int(max(np.sqrt(len(self.features)), 3))
            ),
            "estimation_sample_size": trial.suggest_float(
                "estimation_sample_size", 0.1, 0.9
            ),
            "evaluationFunction": trial.suggest_categorical(
                "evaluationFunction",
                ["KL", "ED", "Chi", "CTS", "DDP", "IT", "CIT", "IDDP"],
            ),
        }
        model = self.model_class(control_name="0", random_state=RANDOM_STATE, **param)
        model.fit(
            X=self.df_train[self.features],
            y=self.df_train[self.target_col],
            treatment=self.df_train[self.treatment_col],
        )
        uplift_valid = model.predict(self.df_valid[self.features])

        metric_result = self.metric(
            y_true=self.df_valid[self.target_col],
            uplift=uplift_valid,
            treatment=self.df_valid[self.treatment_col],
        )

        if self.overfit_metric is not None:
            uplift_train = model.predict(self.df_train[self.features])

            metric_result_train = self.metric(
                y_true=self.df_train[self.target_col],
                uplift=uplift_train,
                treatment=self.df_train[self.treatment_col],
            )
            return self.overfit_metric(metric_result, metric_result_train)

        return metric_result

    def objective_random_forest(self, trial):
        param = {
            "max_depth": trial.suggest_int("max_depth", 1, 4),
            "max_features": trial.suggest_int(
                "max_features", 2, int(max(np.sqrt(len(self.features)), 3))
            ),
            "n_estimators": trial.suggest_int("n_estimators", 30, 100),
            "estimation_sample_size": trial.suggest_float(
                "estimation_sample_size", 0.2, 0.8
            ),
            "evaluationFunction": trial.suggest_categorical(
                "evaluationFunction",
                ["KL", "ED", "Chi", "CTS", "DDP", "IT", "CIT", "IDDP"],
            ),
        }
        model = self.model_class(control_name="0", random_state=RANDOM_STATE, **param)
        model.fit(
            X=self.df_train[self.features],
            y=self.df_train[self.target_col],
            treatment=self.df_train[self.treatment_col],
        )
        uplift_valid = model.predict(self.df_valid[self.features])

        metric_result = self.metric(
            y_true=self.df_valid[self.target_col],
            uplift=uplift_valid,
            treatment=self.df_valid[self.treatment_col],
        )

        if self.overfit_metric is not None:
            uplift_train = model.predict(self.df_train[self.features])

            metric_result_train = self.metric(
                y_true=self.df_train[self.target_col],
                uplift=uplift_train,
                treatment=self.df_train[self.treatment_col],
            )
            return self.overfit_metric(metric_result, metric_result_train)

        return metric_result

    def objective_catboost(self, trial):
        param = {
            "objective": trial.suggest_categorical(
                "objective", ["Logloss", "CrossEntropy"]
            ),
            "depth": trial.suggest_int("depth", 1, 8),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
            "n_estimators": trial.suggest_int("n_estimators", 30, 240),
            "boosting_type": trial.suggest_categorical(
                "boosting_type", ["Ordered", "Plain"]
            ),
            "bootstrap_type": trial.suggest_categorical(
                "bootstrap_type", ["Bayesian", "Bernoulli", "MVS"]
            ),
        }

        if param["bootstrap_type"] == "Bayesian":
            param["bagging_temperature"] = trial.suggest_float(
                "bagging_temperature", 0, 10
            )
        elif param["bootstrap_type"] == "Bernoulli":
            param["subsample"] = trial.suggest_float("subsample", 0.1, 1)

        # Создание и обучение модели
        estimator = CatBoostClassifier(random_state=RANDOM_STATE, silent=True, **param)

        estimator.fit(
            X=self.df_train[self.features],
            y=self.df_train[self.target_col],
        )

        score_vld = estimator.predict_proba(self.df_valid[self.features])[:, 1]
        try:
            metric_result = self.metric(
                y_true=self.df_valid[self.target_col],
                y_score=score_vld,
            )
            if self.overfit_metric is not None:
                score_train = estimator.predict_proba(self.df_train[self.features])[
                    :, 1
                ]

                metric_result_train = self.metric(
                    y_true=self.df_train[self.target_col],
                    y_score=score_train,
                )
                return self.overfit_metric(metric_result, metric_result_train)
        except:
            metric_result = self.metric(
                y_true=self.df_valid[self.target_col],
                y_pred=(score_vld >= 0.5).astype("int"),
            )
            if self.overfit_metric is not None:
                score_train = estimator.predict_proba(self.df_train[self.features])[
                    :, 1
                ]

                metric_result_train = self.metric(
                    y_true=self.df_train[self.target_col],
                    y_pred=(score_train >= 0.5).astype("int"),
                )
                return self.overfit_metric(metric_result, metric_result_train)
        return metric_result

    def objective_x_learner(self, trial):
        # param grid for the first step model of x-learner
        # CatBoostClassifier
        model_params = {
            "objective": trial.suggest_categorical(
                "objective", ["Logloss", "CrossEntropy"]
            ),
            "depth": trial.suggest_int("depth", 1, 8),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
            "n_estimators": trial.suggest_int("n_estimators", 30, 240),
            "boosting_type": trial.suggest_categorical(
                "boosting_type", ["Ordered", "Plain"]
            ),
            "bootstrap_type": trial.suggest_categorical(
                "bootstrap_type", ["Bayesian", "Bernoulli", "MVS"]
            ),
        }

        if model_params["bootstrap_type"] == "Bayesian":
            model_params["bagging_temperature"] = trial.suggest_float(
                "bagging_temperature", 0, 10
            )
        elif model_params["bootstrap_type"] == "Bernoulli":
            model_params["subsample"] = trial.suggest_float("subsample", 0.1, 1)

        # param grid for the second step model of x-learner
        # CatBoostRegressor
        uplift_model_params = {
            "objective": trial.suggest_categorical(
                "objective2", ["MAE", "MAPE", "RMSE"]
            ),
            "depth": trial.suggest_int("depth2", 1, 8),
            "learning_rate": trial.suggest_float("learning_rate2", 0.01, 0.3),
            "n_estimators": trial.suggest_int("n_estimators2", 30, 240),
            "boosting_type": trial.suggest_categorical(
                "boosting_type2", ["Ordered", "Plain"]
            ),
            "bootstrap_type": trial.suggest_categorical(
                "bootstrap_type2", ["Bayesian", "Bernoulli", "MVS"]
            ),
        }

        if uplift_model_params["bootstrap_type"] == "Bayesian":
            uplift_model_params["bagging_temperature"] = trial.suggest_float(
                "bagging_temperature2", 0, 10
            )
        elif uplift_model_params["bootstrap_type"] == "Bernoulli":
            uplift_model_params["subsample"] = trial.suggest_float("subsample2", 0.1, 1)

        # create base models and x-learner
        model = CatBoostClassifier(
            random_state=RANDOM_STATE, silent=True, **model_params
        )
        uplift_model = CatBoostRegressor(
            random_state=RANDOM_STATE, silent=True, **uplift_model_params
        )
        x_learner = self.model_class(
            model=model,
            uplift_model=uplift_model,
            map_groups={"control": 0, "treatment": 1},
        )

        x_learner.fit(
            X=self.df_train[self.features],
            y=self.df_train[self.target_col],
            treatment=self.df_train[self.treatment_col],
        )

        uplift_valid = x_learner.predict(self.df_valid[self.features])

        # TODO : think about relative uplift for x_learner
        #        1) 2nd step = uplift regressors --> division not needed
        #        2) 1st step = propensities --> division = usual two-models
        # if self.uplift_type == 'rel':
        #     uplift_valid = x_learner.trmnt_preds_ / model.ctrl_preds_

        metric_result = self.metric(
            y_true=self.df_valid[self.target_col],
            uplift=uplift_valid,
            treatment=self.df_valid[self.treatment_col],
        )
        if self.overfit_metric is not None:
            uplift_train = x_learner.predict(self.df_train[self.features])

            # TODO : look at previous todo
            # if self.uplift_type == 'rel':
            #     uplift_train = model.trmnt_preds_ / model.ctrl_preds_

            metric_result_train = self.metric(
                y_true=self.df_train[self.target_col],
                uplift=uplift_train,
                treatment=self.df_train[self.treatment_col],
            )
            return self.overfit_metric(metric_result, metric_result_train)

        return metric_result

    def objective_custom(self, trial):
        """
        Custom  object function for custom class

        Args:
            optuna trial

        Returns: None
        """
        assert (
            -1 > 1
        ), "Для использования своего objective для своего класса модели определите objective_custom"

    def find_best_params(
        self, model_class: Pipeline, features: tp.List[str], timeout: int
    ):
        """
        Finds the optimal parameters for the given model class to maximize the specified function

        Args:
            model_class (pipeline): the model class for which the optimal parameters
                will be found. It should be a scikit-learn compatible pipeline or model

            features (1d array-like): a list of feature names to be used in the model. These features
                will be considered during the parameter optimization process

            timeout (int): the maximum time in seconds allowed for the optimization
                process. If the optimization exceeds this time, it will be terminated

        Returns: estimator with optimal values
        """
        optuna.logging.set_verbosity(optuna.logging.WARNING)
        sampler = optuna.samplers.TPESampler(seed=RANDOM_STATE)
        study = optuna.create_study(direction="maximize", sampler=sampler)
        self.model_class = model_class
        self.features = features

        if model_class.__name__ == "SoloModel":
            study.optimize(self.objective_slearner, timeout=timeout)
            params = study.best_params
            method = params["method"]
            del params["method"]
            estimator = CatBoostClassifier(
                random_state=RANDOM_STATE, silent=True, **params
            )
            slearner = model_class(method=method, estimator=estimator)
            return slearner

        elif model_class.__name__ == "TwoModels":
            study.optimize(self.objective_tlearner, timeout=timeout)
            params = study.best_params
            method = params["method"]
            del params["method"]
            param1 = {k: v for k, v in params.items() if k[-1] != "2"}
            param2 = {k[:-1]: v for k, v in params.items() if k[-1] == "2"}
            estimator = CatBoostClassifier(
                random_state=RANDOM_STATE, silent=True, **param1
            )
            estimator2 = CatBoostClassifier(
                random_state=RANDOM_STATE, silent=True, **param2
            )
            tlearner = model_class(
                method=method, estimator_trmnt=estimator, estimator_ctrl=estimator2
            )
            return tlearner

        elif model_class.__name__ == "AufRandomForestClassifier":
            study.optimize(self.objective_random_forest, timeout=timeout)
            params = study.best_params
            forest = model_class(control_name="0", random_state=RANDOM_STATE, **params)
            return forest

        elif model_class.__name__ == "AufTreeClassifier":
            study.optimize(self.objective_tree, timeout=timeout)
            params = study.best_params
            tree = model_class(control_name="0", random_state=RANDOM_STATE, **params)
            return tree

        elif model_class.__name__ == "CatBoostClassifier":
            study.optimize(self.objective_catboost, timeout=timeout)
            params = study.best_params
            response_model = model_class(
                random_state=RANDOM_STATE, silent=True, **params
            )
            return response_model

        elif model_class.__name__ == "AufXLearner":
            study.optimize(self.objective_x_learner, timeout=timeout)
            params = study.best_params
            model_params = {k: v for k, v in params.items() if k[-1] != "2"}
            uplift_model_params = {k[:-1]: v for k, v in params.items() if k[-1] == "2"}
            model = CatBoostClassifier(
                random_state=RANDOM_STATE, silent=True, **model_params
            )
            uplift_model = CatBoostRegressor(
                random_state=RANDOM_STATE, silent=True, **uplift_model_params
            )
            x_learner = model_class(
                model=model,
                uplift_model=uplift_model,
                map_groups={"control": 0, "treatment": 1},
            )
            return x_learner

        else:
            study.optimize(self.objective_custom, timeout=timeout)
            params = study.best_params
            forest = model_class(**params)
            return forest
