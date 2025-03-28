import json
import os
import tempfile
import typing as tp

import mlflow
from mlflow.pyfunc import PythonModel


def skip_none_input(func):
    def wrapper(*args, **kwargs):
        # Проверяем, есть ли None среди аргументов
        if any(arg is None for arg in args) or any(
            value is None for value in kwargs.values()
        ):
            return None
        return func(*args, **kwargs)

    return wrapper


class AUFModel(PythonModel):
    """Model wrapper for legacy Mlflow version"""

    def __init__(self, model, model_name, features, uplift_prediction_type):
        self.model = model
        self.model_name = model_name
        self.features = features
        self.uplift_prediction_type = uplift_prediction_type

    def predict(self, context, model_input):
        """Predict model scores"""
        output = model_input
        if self.model_name == "CatBoostClassifier":
            output["score_raw"] = self.model.predict_proba(model_input[self.features])[
                :, 1
            ].reshape(-1)
        elif self.model_name in (
            "SoloModel",
            "TwoModels",
            "AufRandomForestClassifier",
            "AufTreeClassifier",
        ):
            uplift_abs = self.model.predict(model_input[self.features]).reshape(-1)
            output["trmnt_preds"] = self.model.trmnt_preds_
            output["ctrl_preds"] = self.model.ctrl_preds_
            if self.uplift_prediction_type == "abs":
                output["score_raw"] = uplift_abs
            else:
                output["score_raw"] = output["trmnt_preds"] / output["ctrl_preds"] - 1
        else:
            raise ValueError(
                "Available models for auf: 'CatBoostClassifier', 'SoloModel', 'TwoModels', 'AufRandomForestClassifier', 'AufTreeClassifier'"
            )
        return output


@skip_none_input
def get_or_create_experiment(experiment_name):
    current_experiment = mlflow.get_experiment_by_name(experiment_name)
    if current_experiment is None:
        current_experiment = mlflow.create_experiment(experiment_name)
        print(f"Experiment '{experiment_name}' created with ID: {current_experiment}")
    else:
        current_experiment = dict(current_experiment)["experiment_id"]
        print(
            f"Experiment '{experiment_name}' already exists with ID: {current_experiment}"
        )
    print(
        f"Mlflow link: https://mlflow-autotrain.mdp.moscow.alfaintra.net/#/experiments/{current_experiment}"
    )
    return current_experiment


@skip_none_input
def generate_run(
    experiment_name: str,
    experiment_id: str,
    run_name: str,
    description: tp.Optional[str] = None,
):
    with mlflow.start_run(
        run_name=run_name, experiment_id=experiment_id, description=description
    ) as run:
        run_id = run.info.run_id
    print(f"RunID {run_id}")
    print(
        f"Mlflow run link: https://mlflow-autotrain.mdp.moscow.alfaintra.net/#/experiments/{experiment_id}/runs/{run_id}"
    )
    return run_id


@skip_none_input
def save_json(data, name, artifact_path, run_id):
    with mlflow.start_run(run_id=run_id) as run:
        with tempfile.TemporaryDirectory() as temp_dir:
            custom_file_path = os.path.join(temp_dir, f"{name}.json")
            with open(custom_file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)
            mlflow.log_artifact(custom_file_path, artifact_path=artifact_path)


@skip_none_input
def save_dataframe_html(df, name, artifact_path, run_id):
    with mlflow.start_run(run_id=run_id) as run:
        with tempfile.TemporaryDirectory() as temp_dir:
            custom_file_path = os.path.join(temp_dir, f"{name}.html")
            df.to_html(custom_file_path, escape=False)
            mlflow.log_artifact(custom_file_path, artifact_path=artifact_path)


@skip_none_input
def save_figure(fig, name, artifact_path, run_id):
    with mlflow.start_run(run_id=run_id) as run:
        with tempfile.TemporaryDirectory() as temp_dir:
            custom_file_path = os.path.join(temp_dir, f"{name}.png")
            fig.savefig(custom_file_path, bbox_inches="tight")
            mlflow.log_artifact(custom_file_path, artifact_path=artifact_path)


@skip_none_input
def save_pdf_figures(file_path, artifact_path, run_id):
    with mlflow.start_run(run_id=run_id) as run:
        mlflow.log_artifact(file_path, artifact_path=artifact_path)


@skip_none_input
def save_params_dict(params, run_id):
    with mlflow.start_run(run_id=run_id) as run:
        mlflow.log_params(params)


@skip_none_input
def save_metrics(metrics, run_id):
    with mlflow.start_run(run_id=run_id) as run:
        mlflow.log_metrics(metrics)


@skip_none_input
def save_model(model, artifact_path, run_id, experiment_name):
    with mlflow.start_run(run_id=run_id) as run:
        mlflow.pyfunc.log_model(
            python_model=model,
            artifact_path=artifact_path,
            registered_model_name=experiment_name,
        )
