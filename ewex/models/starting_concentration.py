import os
import warnings

import numpy as np
import pandas as pd
import dataclasses as dtc

from ewex.models.array_container import ArrayContainer
from ewex.models.matrix import Matrix


@dtc.dataclass
class StartingConcentration(ArrayContainer):
    arr: np.ndarray

    @staticmethod
    def from_lit(substance, matrix: Matrix) -> "StartingConcentration":
        df = pd.read_csv(os.path.join("data", "starting_concentration.csv"),
                         encoding='cp1252',
                         sep=';',
                         na_values="",
                         keep_default_na=False,
                         dtype={"removal_percent": float}
                         )
        dff = df.loc[
            (df.substance_id == substance.id) &
            (df.matrix_id == matrix.id)
            ]
        lit_values = np.concatenate((
            dff.min_value_ng_l.values,
            dff.point_value_ng_l.values,
            dff.max_value_ng_l.values)
        )
        if len(~np.isnan(lit_values)) == 0:
            warnings.warn(f"no starting concentration found for {substance.id} - {matrix.id}")
        return StartingConcentration(lit_values[~np.isnan(lit_values)])

    def n_uniform_samples(self, n_samples: int):
        # TODO: CHECK SORTING
        return np.sort(np.random.uniform(self.arr.min(), self.arr.max(), n_samples))[::-1]
