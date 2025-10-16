import dataclasses as dtc
import numpy as np
import pandas as pd

from promisces.models.removal_percent import RemovalPercent
from promisces.models.starting_concentration import StartingConcentration
from promisces.models.scenario import Scenario
from promisces.removal_processes import (
    ProcessResult,
    apply_generic_process,\
    apply_mixture_process,\
    apply_separation_process,\
    apply_separation_sludge_process
)


@dtc.dataclass
class SimulationResult:
    scenario: Scenario
    n_runs: int
    rmv_factor_resolution: int
    starting_concentration: np.ndarray
    intermediate_results: list[ProcessResult]

    @property
    def final_concentration(self) -> np.ndarray:
        return self.intermediate_results[-1].output_concentration

    @property
    def output_c_df(self):
        df = dict(input=self.starting_concentration)
        for result, treatment in zip(self.intermediate_results, self.scenario.treatment_train):
            df.update({treatment.id: result.output_concentration})
        return pd.DataFrame(df)

    @property
    def rmv_factor_df(self):
        return pd.DataFrame({
            treatment.id: result.rmv_factors
            for result, treatment in zip(self.intermediate_results, self.scenario.treatment_train)
        })

    @property
    def treatment_df(self):
        in_mat, out_mat = [self.scenario.input_matrix], []
        for treatment in self.scenario.treatment_train:
            out_mat += [treatment.get_output_matrix(in_mat[-1])]
            in_mat += [out_mat[-1]]
        in_mat = in_mat[:-1]
        return pd.DataFrame(dict(
            treatment_id=[t.id for t in self.scenario.treatment_train],
            average_out=[r.average_out for r in self.intermediate_results],
            input_matrix=[m.name for m in in_mat],
            output_matrix=[m.name for m in out_mat],
            dominant_data=[r.dominant_distribution.value for r in self.intermediate_results],
            substance=self.scenario.substance.name,
            n_runs=self.n_runs,
            removal_factor_resolution=self.rmv_factor_resolution,

        ))

    def export_excel(self, filename):
        with pd.ExcelWriter(filename) as excel_writer:
            self.treatment_df.to_excel(excel_writer, sheet_name='info', index=False)
            self.output_c_df.describe(
                percentiles=[0.5, 0.75, 0.9, 0.95, 0.975, 0.99]
            ).T.to_excel(excel_writer, sheet_name='output_c', index=False)
            self.rmv_factor_df.describe(
                percentiles=[0.5, 0.75, 0.9, 0.95, 0.975, 0.99]
            ).T.to_excel(excel_writer, sheet_name='removal', index=False)


def simulate_removal(
        scenario: Scenario,
        n_runs: int = 10000,
        rmv_factor_resolution: int = 1000,
) -> SimulationResult:
    input_matrix, substance, treatment_train, starting_concentration, reference = \
        scenario.input_matrix, \
        scenario.substance, \
        scenario.treatment_train, \
        scenario.starting_concentration, \
        scenario.reference

    treatment_train.validate_matrices(input_matrix)
    treatment_train.validate_mixtures()

    if starting_concentration is None:
        starting_concentration = substance.starting_concentration
    if starting_concentration is None:
        starting_concentration = StartingConcentration.from_lit(substance, input_matrix)
        if len(starting_concentration) == 0:
            raise RuntimeError("No starting concentration found in the literature for"
                               f" substance {substance.id} and input matrix {input_matrix.id}.\n"
                               f"Please provide one or try an other substance/matrix pair.")
    start_c = input_c = starting_concentration.n_uniform_samples(n_runs)

    lit_removals = [RemovalPercent.from_lit(treatment, substance) for treatment in treatment_train]

    results = []
    for i, (treatment, lit_rmv) in enumerate(
            zip(treatment_train, lit_removals)
    ):
        # fix input_c based on treatment id
        if treatment.id != "wwsl":
            # TODO: CHECK SORTING
            input_c = np.flip(input_c)
        # dispatch to removal functions:
        if treatment.id.startswith("dil"):
            result = apply_mixture_process(input_c, **treatment.mixture.asdict())
        elif treatment.id == "sepev":
            result = apply_separation_process(input_c, **treatment.mixture.asdict())
        elif treatment.id == "wwsl":
            result = apply_separation_sludge_process(
                input_c,
                lit_rmv,
                treatment.removal,
                rmv_factor_resolution,
            )
        else:
            result = apply_generic_process(
                input_c,
                lit_rmv,
                treatment.removal,
                rmv_factor_resolution,
                n_runs=n_runs
            )

        results += [result]
        # TODO: CHECK SORTING
        input_c = np.sort(result.output_concentration)

    return SimulationResult(
        scenario,
        n_runs,
        rmv_factor_resolution,
        start_c,
        results,
    )
