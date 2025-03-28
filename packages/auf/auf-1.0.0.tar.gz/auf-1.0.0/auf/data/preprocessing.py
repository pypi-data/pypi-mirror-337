import typing as tp

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, TargetEncoder


class Preprocessor:
    """
    Class for preprocessing numerical and categorical data.

    Parameters:
        numerical_method (str): method for handling gaps in numerical data ('min', 'mean' or 'max')
        max_categories (int): maximum number of categories to encode
        encoder_type (str): encoder type for categorical features ('target' or 'label')

    Attributes:
        numeric_cols_mapper (dict): dictionary with values ​​to fill gaps in numerical columns
        categorical_cols_mapper (dict): dictionary with encoders and categories for categorical columns

    Examples:
        >>> from AUF.preprocess import Preprocessor
        >>> preprocessor = Preprocessor()
        >>> df = pd.read_csv(filename)
        >>> numeric_cols = df.columns[3:7]
        >>> categorical_cols = df.columns[7:10]
        >>> target_col = 'target'
        >>> preprocessor.fit(df, numeric_cols, categorical_cols, target_col)
        >>> df_transformed = preprocessor.transform(df)
    """

    def __init__(
        self,
        numerical_method: str = "min",
        max_categories: int = 4,
        encoder_type: str = "target",
    ):
        self.numeric_cols_mapper = {}
        self.categorical_cols_mapper = {}
        self.numerical_method = numerical_method
        self.max_categories = max_categories
        self.encoder_type = encoder_type

    def fit(
        self,
        df: pd.DataFrame,
        numeric_cols: tp.List[str],
        categorical_cols: tp.List[str],
        target_col: str = None,
    ):
        """
        Train the preprocessor on the given data.

        Parameters:
            df (pd.DataFrame): original DataFrame
            numeric_cols (list): list of numeric columns
            categorical_cols (list): list of categorical columns
            target_col (str): name of the target variable

        Returns:
            self: trained preprocessor object
        """
        if self.encoder_type == "target" and target_col is None:
            raise ValueError(
                "When encoder_type is 'target', target_col must be specified."
            )
        self._process_numeric_cols(df, numeric_cols)
        self._process_categorical_cols(df, categorical_cols, target_col)
        return self

    def transform(self, df: pd.DataFrame):
        """
        Applying a trained preprocessor to new data.

        Parameters:
            df (pd.DataFrame): DataFrame for trasformation

        Returns:
            pd.DataFrame: trasformed DataFrame
        """
        df = df.fillna(self.numeric_cols_mapper)

        for col, mapper in self.categorical_cols_mapper.items():
            if col in df.columns:
                df = self._apply_categorical_encoding(df, col, mapper)

        return df

    def _get_fill_value(self, series: pd.Series):
        """An auxiliary method for calculating the gap filling value."""
        method = self.numerical_method
        if method == "min":
            return series.min() - 1
        if method == "mean":
            return series.mean()
        if method == "max":
            return series.max() + 1
        raise NameError(
            f"Preprocessor supports only numerical_method in ['min', 'max', 'mean'], got {self.numerical_method}."
        )

    def _process_numeric_cols(self, df: pd.DataFrame, numeric_cols: tp.List[str]):
        """Processing numeric columns."""
        for col in numeric_cols:
            fill_value = self._get_fill_value(df[col])
            self.numeric_cols_mapper[col] = (
                fill_value if not np.isnan(fill_value) else 0
            )

    def _process_categorical_cols(
        self, df: pd.DataFrame, categorical_cols: tp.List[str], target_col: str
    ):
        """Processing categorical columns."""
        for col in categorical_cols:
            processed_series = df[col].astype(str).fillna("ND")
            top_categories = (
                processed_series.value_counts().head(self.max_categories).index.tolist()
            )
            values = processed_series.apply(
                lambda x: x if x in top_categories else "other"
            ).values
            targets = df[target_col].values if target_col is not None else None

            encoder = self._create_encoder(values, targets)
            self.categorical_cols_mapper[col] = {
                "encoder": encoder,
                "top_categories": top_categories,
            }

    def _create_encoder(self, values: np.array, target: np.array):
        """Create and fit encoder"""
        if self.encoder_type == "target":
            encoder = TargetEncoder(target_type="continuous")
            encoder.fit(values.reshape(-1, 1).astype(str), target)
        elif self.encoder_type == "label":
            encoder = LabelEncoder().fit(values.astype(str))
        else:
            raise ValueError(
                f"Preprocessor supports only encoder_type in ['target', 'label'], got {self.encoder_type}."
            )
        return encoder

    def _apply_categorical_encoding(self, df, col: str, mapper: tp.Dict[str, tp.Any]):
        """Applying coding to a categorical column."""
        processed_col = (
            df[col]
            .astype(str)
            .fillna("ND")
            .apply(lambda x: x if x in mapper["top_categories"] else "other")
        )

        if self.encoder_type == "target":
            encoded = mapper["encoder"].transform(processed_col.values.reshape(-1, 1))
            df[col] = encoded.astype(float)
        elif self.encoder_type == "label":
            df[col] = mapper["encoder"].transform(processed_col)
        else:
            raise NameError(
                f"Preprocessor supports only encoder_type in ['target', 'label'], got {self.encoder_type}."
            )
        return df

    def _get_numerical_dict(self, cols: tp.List[str]):
        """Get numerical dict for cols"""
        result = dict()
        for col, fill_value in self.numeric_cols_mapper.items():
            if cols is None or col in cols:
                result[col] = float(fill_value)
        return result

    def _get_categorical_dict(self, cols: tp.List[str]):
        """Get categorical dict for cols"""
        result = dict()
        for col, encoder_dict in self.categorical_cols_mapper.items():
            encoder = encoder_dict["encoder"]
            if cols is None or col in cols:
                result[col] = dict()
                if self.encoder_type == "target":
                    result[col] = {
                        "categories": encoder.categories_[0].tolist(),
                        "encodings": encoder.encodings_[0].tolist(),
                    }
                elif self.encoder_type == "label":
                    result[col] = {
                        "categories": encoder.classes_.tolist(),
                        "encodings": encoder.transform(encoder.classes_)
                        .astype("float")
                        .tolist(),
                    }
                else:
                    raise NameError(
                        f"Preprocessor supports only encoder_type in ['target', 'label'], got {self.encoder_type}."
                    )
        return result

    def _get_categorical_from_dict(
        self, categorical_cols_mapper: tp.Dict[str, tp.List[tp.Any]]
    ):
        """Generate categorical_cols_mappaer from dict"""
        result = dict()
        for col, encoder_dict in categorical_cols_mapper.items():
            top_categories = encoder_dict["categories"]
            categories = np.array(top_categories)
            if self.encoder_type == "target":
                encoder = TargetEncoder()
                encoder.categories_ = [top_categories]
                encoder.target_mean_ = 0
                encoder.target_type_ = "continuous"
                encoder._infrequent_enabled = False
                encoder.encodings_ = [np.array(encoder_dict["encodings"])]
            elif self.encoder_type == "label":
                encoder = LabelEncoder()
                encoder.classes_ = categories
            else:
                raise NameError(
                    f"Preprocessor supports only encoder_type in ['target', 'label'], got {self.encoder_type}."
                )

            result[col] = {"encoder": encoder, "top_categories": top_categories}
        return result

    def get_dict_class(self, cols: tp.List[str] = None):
        """Get class in dict format"""
        params = {}
        params["encoder_type"] = self.encoder_type
        params["numerical_method"] = self.numerical_method
        params["max_categories"] = float(self.max_categories)

        params["numeric_cols_mapper"] = self._get_numerical_dict(cols)
        params["categorical_cols_mapper"] = self._get_categorical_dict(cols)

        return params

    def generate_from_dict(self, params: tp.Dict[str, tp.Any]):
        """Generate class from dict format"""
        self.encoder_type = params["encoder_type"]
        self.numerical_method = params["numerical_method"]
        self.max_categories = int(params["max_categories"])
        self.numeric_cols_mapper = params["numeric_cols_mapper"]

        self.categorical_cols_mapper = self._get_categorical_from_dict(
            params["categorical_cols_mapper"]
        )
        return self
