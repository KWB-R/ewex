import dataclasses as dtc
from ewex.models.reference import Reference


@dtc.dataclass
class HazardGroup:
    name: str
    reference: Reference | None = None
    use_equivalence: bool = False

    def with_reference(self, reference: Reference):
        self.use_equivalence = True
        self.reference = reference
        return self

@dtc.dataclass
class Equivalence:
    name: str
    equivalent_value: float
    hazard_group: HazardGroup
    year: int
    comment: str = ""