import dataclasses as dtc
from itertools import product
from typing import Iterator

from ewex.models.matrix import Matrix
from ewex.models.substance import Substance
from ewex.models.treatment import TreatmentTrain
from ewex.models.starting_concentration import StartingConcentration
from ewex.models.reference import Reference


@dtc.dataclass
class Scenario:
    name: str
    input_matrix: Matrix
    substance: Substance
    treatment_train: TreatmentTrain
    starting_concentration: StartingConcentration | None = None
    reference: Reference | None = None

    def __post_init__(self):
        self.treatment_train.validate_matrices(self.input_matrix)
        if self.substance.starting_concentration is not None:
            self.starting_concentration = self.substance.starting_concentration
        if self.starting_concentration is None:
            self.starting_concentration = StartingConcentration.from_lit(self.substance, self.input_matrix)
        if self.substance.reference is not None:
            self.reference = self.substance.reference
        if self.reference is None:
            self.reference = Reference.from_lit(self.treatment_train.output_matrix(self.input_matrix), self.substance)

    def simulate_removal(self,
                         n_runs: int = 10000,
                         rmv_factor_resolution: int = 1000,
                         ):
        from ewex.simulate_removal import simulate_removal
        return simulate_removal(
            self,
            n_runs,
            rmv_factor_resolution
        )

    @staticmethod
    def from_grid(
            name_prefix: str,
            input_matrices: list[Matrix],
            substances: list[Substance],
            treatment_trains: list[TreatmentTrain],
            starting_concentrations: list[StartingConcentration | None],
            references: list[Reference | None]
    ) -> Iterator["Scenario"]:
        for i, (mat, sub, train, start_c, ref) in enumerate(product(
                input_matrices, substances, treatment_trains, starting_concentrations, references
        )):
            yield Scenario(
                f"{name_prefix}-{i}",
                mat, sub, train, start_c, ref
            )
