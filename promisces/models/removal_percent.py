from __future__ import annotations
import os

import numpy as np
import pandas as pd
import dataclasses as dtc

from promisces.models.array_container import ArrayContainer
from promisces.models.substance import Substance
import promisces.models.treatment as treatment_model


@dtc.dataclass
class RemovalPercent(ArrayContainer):

    arr: np.ndarray

    @staticmethod
    def from_lit(treatment: treatment_model.Treatment, substance: Substance) -> "RemovalPercent":
        if not treatment.with_lit_data:
            return RemovalPercent(np.array([]))
        df = pd.read_csv(
            os.path.join("data", "process_removal_lit.csv"),
            encoding='cp1252',
            sep=';',
            na_values="",
            keep_default_na=False,
            dtype={"removal_percent": float}
        )
        rmv_percent = df.loc[
            (df.substance_id == substance.id) & (df.treatment_id == treatment.id)
            ].removal_percent
        return RemovalPercent(np.round(rmv_percent.values).astype(int))

