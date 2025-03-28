import typing as tp
from dataclasses import dataclass

import numpy as np
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
from .gridsearch import ModelResult, OptuneUpliftDefault

# from functools import partical


def fit_model(
    estimator: Pipeline,
    df_train: pd.DataFrame,
    features: tp.List[str],
    target_col: str,
    treatment_col: str,
    # uplift_type: tp.Literal["abs", "rel"] = "abs"
    uplift_type: str = "abs",
):
    """
    Train the provided model on the training data and evaluate its performance on the validation data

    Args:
        estimator: model to be trained. It should be compatible with the scikit-learn interface

        df_train (pd.DataFrame): data for training the model. It should contain both features
            and the target variable

        df_valid (pd.DataFrame): data for validating the model. It is used to assess performance
            after training

        df_test (pd.DataFrame): data for testing the model. It is used for final evaluation of
            the model's performance

        features (1d array-like): list of feature names to be used for training the model

        target_col (string): name of the column representing the target variable that the model
            should predict

        treatment_col (string): name of the column representing treatment or group that should
            be considered during training

        uplift_type: type of uplift, if abs use TR_1-TR2 , if rel use TR_1/TR_2 -1

    Returns: dataclass ModelResults containing the trained model, its predictions, and the
             features on which it was trained
    """
    if type(estimator).__name__ == "CatBoostClassifier":
        estimator.fit(X=df_train[features], y=df_train[target_col])
    # elif type(estimator).__name__ == "UpliftRandomForestClassifier":
    #     estimator.fit(
    #         X=df_train[features].values,
    #         y=df_train[target_col].values,
    #         treatment=df_train[treatment_col].astype("str").values,
    #     )
    else:
        estimator.fit(
            X=df_train[features],
            y=df_train[target_col],
            treatment=df_train[treatment_col],
        )

    result = ModelResult(
        estimator=estimator,
        features=features,
        uplift_prediction_type=uplift_type,
        median_test_metric_value=None,
    )
    return result


def generate_model_from_classes(
    model_class: object,
    df_train: pd.DataFrame,
    df_valid: pd.DataFrame,
    df_test: pd.DataFrame,
    features: tp.Dict[str, tp.List[str]],
    target_col: str,
    treatment_col: str,
    feature_nums: tp.List[int],
    timeout: int,
    metric: object,
    use_default_params: bool,
    search_class: object,
    overfit_metric: object = None,
    # uplift_type: tp.Literal["abs", "rel"] = "abs"
    uplift_type: str = "abs",
):
    """
    Generate and train a model from the specified class, using the provided training and validation datasets

    Args:
        model_class: model class to be instantiated and trained

        df_train (pd.DataFrame): the dataset used for training the model. It should contain both features
            and the target variable

        df_valid (pd.DataFrame): the dataset used for hyperparameter tuning. It is used to evaluate the
            model's performance during training

        df_test (pd.DataFrame): the dataset used for final evaluation of the model's performance after training

        features (dict): a dictionary where each key corresponds to a specific feature set to be used
            for training the model

        target_col (string): the name of the column representing the target variable that the model should predict

        treatment_col (string): the name of the column representing treatment or group that should be considered
            during training

        feature_nums (1d array-like): an optional parameter specifying the number of features to use for
            training. If provided, the model will be trained using only this number of features

        timeout (integer): an optional parameter specifying the maximum time (in seconds) allowed for
            training if use_default_params is set to False

        metric: an optional parameter specifying the metric to optimize if use_default_params is set to False

        use_default_params (bool): a flag indicating whether to use default parameters for the model. If
            set to False, hyperparameter tuning will be performed

        search_class: the class responsible for hyperparameter tuning. It should implement methods to search
            for optimal parameters based on the provided metric

        overfit_metric: an optional parameter specifying the overfit_metric to optimize if use_default_params is set to False

        uplift_type: type of uplift, if abs use TR_1-TR2 , if rel use TR_1/TR_2 -1

    Returns: dict
        A dictionary containing lists of ModelResults for each model trained, indexed by their corresponding feature sets
    """
    fast_fit_result = dict()

    for key in features.keys():
        if feature_nums is None:
            feature_nums = [len(features[key])]

        result_n = list()

        for n in feature_nums:
            assert n <= len(
                features[key]
            ), f"Число признаков {n} в feature_nums, не может быть больше числа признаков {len(features[key])}"

            for uplift_type in ["propensity", "abs", "rel"]:

                if uplift_type == "rel" and model_class.__name__ in [
                    "CatBoostClassifier",
                    "UpliftRandomForestClassifier",
                    "AufXLearner",
                ]:
                    break

                if (
                    uplift_type == "propensity"
                    and model_class.__name__ != "CatBoostClassifier"
                ):
                    continue

                if use_default_params:
                    mc = get_default_model(model_class)
                else:
                    finder_class = search_class(
                        df_train,
                        df_valid,
                        metric,
                        treatment_col,
                        target_col,
                        overfit_metric,
                        uplift_type,
                    )

                    mc = finder_class.find_best_params(
                        model_class, features[key][:n], timeout
                    )

                result_n.append(
                    fit_model(
                        mc,
                        df_train,
                        features[key][:n],
                        target_col,
                        treatment_col,
                        uplift_type,
                    )
                )

        fast_fit_result[key] = result_n

    return fast_fit_result


def models_fast_fit(
    estimator: Pipeline,
    df_train: pd.DataFrame,
    df_valid: pd.DataFrame,
    df_test: pd.DataFrame,
    features: tp.Dict[str, tp.List[str]],
    target_col: str,
    treatment_col: str,
    feature_nums: tp.List[int],
):
    """
    Train specified model using several numbers of TOP features from each feature ranker.

    Args:
        estimator: the model to be trained

        df_train (pd.DataFrame): the dataset used for training the model. It should contain both features and the
            target variable

        df_valid (pd.DataFrame): the dataset used for hyperparameter tuning. It is used to evaluate the model's
            performance during training

        df_test (pd.DataFrame): the dataset used for final evaluation of the model's performance after training

        features (dict): a dictionary where each key corresponds to a specific feature set to be used for training
            the model

        target_col (string): the name of the column representing the target variable that the model should predict

        treatment_col (string): the name of the column representing treatment or group that should be considered
            during training

        feature_nums (1d array-like): an optional parameter specifying the number of features to use for
            training. If provided, the model will be trained using only this number of features

    Returns: dict
        A dictionary containing lists of ModelResults for each model trained, indexed by their corresponding
        feature sets
    """
    fast_fit_result = dict()

    for key in features.keys():
        if feature_nums is None:
            feature_nums = [len(features[key])]

        result_n = list()

        for n in feature_nums:
            assert n <= len(
                features[key]
            ), f"Число признаков {n} в feature_nums, не может быть больше числа признаков {len(features[key])}"

            for uplift_type in ["propensity", "abs", "rel"]:

                if uplift_type == "rel" and type(estimator).__name__ in [
                    "CatBoostClassifier",
                    "UpliftRandomForestClassifier",
                    "AufXLearner",
                ]:
                    break

                if (
                    uplift_type == "propensity"
                    and type(estimator).__name__ != "CatBoostClassifier"
                ):
                    continue

                result_n.append(
                    fit_model(
                        estimator,
                        df_train,
                        features[key][:n],
                        target_col,
                        treatment_col,
                        uplift_type,
                    )
                )

        fast_fit_result[key] = result_n

    return fast_fit_result


def get_default_model(model_class: Pipeline):
    """Get default model for each class"""
    import copy

    if model_class == SoloModel:
        return copy.deepcopy(SOLO_MODEL)
    if model_class == TwoModels:
        return copy.deepcopy(TWO_MODEL)
    if model_class == AufTreeClassifier:
        return copy.deepcopy(UPLIFT_TREE)
    if model_class == AufRandomForestClassifier:
        return copy.deepcopy(UPLIFT_FOREST)
    if model_class == AufXLearner:
        return copy.deepcopy(X_LEARNER)
    raise ValueError("Unexpected value of model_class")


def get_default_params_dict(model_class: Pipeline):
    """Get default model for each class"""
    if model_class == SoloModel:
        return SOLO_MODEL.get_params()
    if model_class == TwoModels:
        return TWO_MODEL.get_params()
    if model_class == AufTreeClassifier:
        return UPLIFT_TREE.get_params()
    if model_class == AufRandomForestClassifier:
        return UPLIFT_FOREST.get_params()
    if model_class == AufXLearner:
        return X_LEARNER.get_params()
    raise ValueError("Unexpected value of model_class")
