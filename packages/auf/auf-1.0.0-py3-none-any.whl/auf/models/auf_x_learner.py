import typing as tp

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator


class AufXLearner:
    """X-learner с поддержкой eval_set

    Обучает две различные response модели для группы с взаимодействием и без него
    Затем строим прокси-модели по предсказанию
        uplift = (y_true - control_model  | treatment = 1)
        uplift = (treatment_model- y_true | treatment = 0)

    Итоговый аплифт uplift_final = eps * uplift_control_model + (1-eps)*uplift_treatment_model

    Больше о работе AufXLearner:
        https://habr.com/ru/companies/glowbyte/articles/686398/

    Args:
        model (estimator object implementing 'fit'):
            The object to use to fit the treatment data.
        uplift_model (estimator object implementing 'fit'):
            The object to use to fit the control data.
        map_groups (dict):
            словарь "группа из данных - группа для Xlearner"
            обязательно должен присутствовать ключ control
        features (list):
            фичи которые будут использовать модели
        cat_features (list):
            категориальные фичи которые будут использовать модели
        group_model (estimator object implementing 'fit'):
            The object to use to fit the control data.

    Attributes:
        trmnt_preds_ (array-like, shape (n_samples, )):
            Estimator predictions uplift by uplift_treatment_model
        ctrl_preds_ (array-like, shape (n_samples, )):
            Estimator predictions uplift by uplift_control_model

    Example:

        from rb_ds_tools.uplift.uplift_models import XLearnerWeight
        from catboost import CatBoostClassifier, CatBoostRegressor

        params = {
            "iterations": 500,
            "depth": 8,
            "learning_rate": 0.1,
            "loss_function": 'Logloss',
            'early_stopping_rounds': 50,
            'eval_metric': 'AUC',
            'random_seed': RANDOM_SEED,
        }

        params_reg = {
            "iterations": 300,
            "depth": 8,
            "learning_rate": 0.01,
            "loss_function": 'MAE',
            'nan_mode': 'Min',
            'eval_metric': 'MAE',
            'use_best_model': True,
            'verbose': False,
            'random_state': RANDOM_SEED,
        }


        clf = XLearnerGroup(
            model=CatBoostClassifier(**params),
            uplift_model=CatBoostRegressor(**params_reg),
            map_groups = {'control': 0, 'treatment1': 1},
            features=int_cols + cat_cols,
            cat_features=cat_cols,
            group_model = CatBoostClassifier(**params)
        )

        '''
            Если у нас есть готовые response модели для каждой из групп

            treat_model = load_model(path1)
            cntrl_model = load_model(path2)
            response_features = list(set(treat_model.feature_names_) + set(treat_model.feature_names_))
            models = {'control': treat_model, 'treatment1':cntrl_model}
            clf.add_fit_response(models=models, features=response_features)
        '''

        clf.fit(
            pd.concat([x_train, y_train], axis = 1),
            pd.concat([x_val, y_val], axis = 1),
            treat_col='treatment',
            target_col='target',
            cost_dict={
                'control': 1,
                'treatment1': 1
            }
        )

        uplift = clf.predict(x_test)['treatment1']

    """

    def __init__(
        self,
        model,
        uplift_model,
        map_groups={"control": 0, "treatment1": 1, "treatment2": 2},
        features=None,
        cat_features=None,
        group_model=None,
    ):
        self._model = {}
        self._uplift_model = {}
        self._params = {
            "model": model.copy(),
            "uplift_model": uplift_model.copy(),
        }

        self._map_groups = map_groups
        self._features = features
        self._response_features = features
        self._cat_features = cat_features
        self._feature_importances = None
        self._group_model = group_model

        assert (
            "control" in self._map_groups.keys()
        ), "map_groups должен содержать ключ control"

        for key in self._map_groups.keys():
            self._model[key] = model.copy()
            self._uplift_model[key] = {
                "control": uplift_model.copy(),
                "treatment": uplift_model.copy(),
            }

    def get_params(self):
        return self._params

    def get_feature_importances(self):
        if self._feature_importances is None:
            return self._get_feature_importances()
        return self._feature_importances

    def _get_feature_importances(self):
        self._feature_importances = {}

        for key in self._map_groups.keys():
            if key != "control":
                fi_cntrl = self._uplift_model[key]["control"].get_feature_importance(
                    prettified=True
                )
                fi_treat = self._uplift_model[key]["treatment"].get_feature_importance(
                    prettified=True
                )

                fi = pd.merge(fi_cntrl, fi_treat, on="Feature Id", how="inner")
                fi["Importances"] = fi.Importances_x + fi.Importances_y
                fi.Importances = fi.Importances.apply(lambda x: round(x, 3))
                fi.index = fi["Feature Id"]
                fi = fi.drop(
                    ["Feature Id", "Importances_x", "Importances_y"], axis=1
                ).to_dict()["Importances"]

                self._feature_importances[key] = fi

        return self._feature_importances

    def fit(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        treatment: pd.Series,
        cost_dict: tp.Optional[tp.Dict[tp.Any, float]] = None,
        **qwargs,
    ):
        """Обучение модели

        Args:
            X:
                должен содержать фичи из self._features и self._response_features
            y:
                колонка с таргетом
            treatment:
                колонка с информацией о группе клиента
            cost_dict:
                доходность утилизаций для разных групп

        Returns:
            object: self
        """

        if cost_dict is None:
            cost_dict = {}
            for group in self._map_groups:
                cost_dict[group] = 1

        assert (
            len(set(self._map_groups.keys()).symmetric_difference(cost_dict.keys()))
            == 0
        ), f"Ключи cost_dict:{cost_dict.keys()} не совпадают с ключами групп map_groups:{self._map_groups.keys()}"

        if self._features is None:
            self._features = X.columns.tolist()

        if self._cat_features is None:
            self._cat_features = [f for f in self._features if X[f].dtype == "object"]

        if self._response_features is None:
            self._response_features = X.columns.tolist()

        assert set(X.columns) == set(self._features) | set(
            self._response_features
        ), "X должен содержать все фичи из self._features и self._response_features"

        y = np.array(y)
        treatment = np.array(treatment)

        if cost_dict is None:
            for key in self._map_groups.keys():
                cost_dict[key] = 1

        if self._group_model is not None:
            self._group_model = self._group_model.fit(
                X=X.loc[:, self._features],
                y=treatment,
                cat_features=self._cat_features,
                **qwargs,
            )

        # обучили все response модели
        for key in self._map_groups.keys():
            treat_name = self._map_groups[key]
            mask = treatment == treat_name
            self._model[key] = self._model[key].fit(
                X=X.loc[mask, self._features],
                y=y[mask],
                cat_features=self._cat_features,
                **qwargs,
            )

        cntrl_name = self._map_groups["control"]
        cntrl_mask = treatment == cntrl_name
        cntrl_X_resp = X.loc[cntrl_mask, self._response_features]
        cntrl_X = X.loc[cntrl_mask, self._features]

        for key in self._map_groups.keys():
            if key != "control":
                trmnt_name = self._map_groups[key]

                sj = cost_dict[key]
                s0 = cost_dict["control"]

                # fit uplift model for control group
                cntrl_probas = self._model[key].predict_proba(cntrl_X_resp)[:, 1]
                cntrl_uplift = sj * cntrl_probas - s0 * y[cntrl_mask]

                self._uplift_model[key]["control"] = self._uplift_model[key][
                    "control"
                ].fit(
                    X=cntrl_X, y=cntrl_uplift, cat_features=self._cat_features, **qwargs
                )

                # fit uplift model for treatment group
                trmnt_mask = treatment == trmnt_name
                trmnt_X_resp = X.loc[trmnt_mask, self._response_features]
                trmnt_X = X.loc[trmnt_mask, self._features]

                trmnt_probas = self._model["control"].predict_proba(trmnt_X_resp)[:, 1]
                trmnt_uplift = -s0 * trmnt_probas + sj * y[trmnt_mask]

                self._uplift_model[key]["treatment"] = self._uplift_model[key][
                    "treatment"
                ].fit(
                    X=trmnt_X, y=trmnt_uplift, cat_features=self._cat_features, **qwargs
                )

        return self

    def predict(self, X: pd.DataFrame, eps: float = 0.5):
        """Get Xlearner uplift prediction

        Args:
            X:
                sample for uplift prediction
            eps:
                is used only if self._group_model is not None
                weight for control uplift model predictions
                (1 - eps) = weight for treatment uplift model predictions

        Returns:
            dict of arrays:
                uplift for different treatment groups
        """

        uplifts = {}

        for key in self._map_groups.keys():
            if key != "control":

                if self._group_model is not None:
                    eps = self._group_model.predict_proba(X[self._features])[:, 0]

                t0 = self._uplift_model[key]["control"].predict(X[self._features])
                t1 = self._uplift_model[key]["treatment"].predict(X[self._features])
                uplifts[key] = eps * t0 + (1 - eps) * t1

        if len(uplifts) == 1:
            treatment_group_name = [group for group in uplifts if group != "control"][0]
            assert (
                len(uplifts[treatment_group_name]) == X.shape[0]
            ), f"len(uplifts[treatment_group_name]) = {len(uplifts[treatment_group_name])}, X.shape[0] = {X.shape[0]}"
            return uplifts[treatment_group_name]

        return uplifts
