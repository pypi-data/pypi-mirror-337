import typing as tp

import pandas as pd
from sklearn.model_selection import train_test_split


def train_val_test_split(
    df: pd.DataFrame,
    size_ratios: tp.List[float] = [0.6, 0.2, 0, 2],
    stratify_cols: tp.List[str] = ["target", "treatment"],
):

    df_train_idx, df_val_test_idx = train_test_split(
        df.index,
        test_size=0.4,
        random_state=8,
        shuffle=True,
        stratify=df[stratify_cols],
    )

    df_val_idx, df_test_idx = train_test_split(
        df_val_test_idx,
        test_size=0.5,
        random_state=8,
        shuffle=True,
        stratify=df.loc[df_val_test_idx, stratify_cols],
    )

    return df_train_idx, df_val_idx, df_test_idx
