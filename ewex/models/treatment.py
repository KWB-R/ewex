from __future__ import annotations

import dataclasses as dtc
from enum import Enum
from typing import Iterator

import numpy as np

import ewex.models.mixture as mixture_model
import ewex.models.removal_percent as removal_model
from ewex.models.matrix import Matrices, Matrix


class TreatmentGroup(Enum):
    DWT = "Drinking Water"
    GWT = "Groundwater"
    WWT = "Wastewater"
    NAP = "Natural Process"
    MIX = "Mixing and Separation"


@dtc.dataclass
class Treatment:
    id: str
    group: TreatmentGroup
    name: str
    input_matrix: list[Matrix]
    output_matrix: Matrix
    with_lit_data: bool = True
    removal: removal_model.RemovalPercent | None = None
    mixture: mixture_model.Mixture | None = None

    def __post_init__(self):
        if Matrices.no_change in self.input_matrix:
            raise ValueError("MatrixEnum.no_change is not allowed in input_matrix")
        if self.removal is None:
            self.removal = removal_model.RemovalPercent(np.array([]))

    def get_output_matrix(self, input_matrix: Matrix) -> Matrix:
        if self.output_matrix == Matrices.no_change:
            return input_matrix
        return self.output_matrix

    @property
    def requires_mixture(self):
        return self.id.startswith("dil") or self.id == "sepev"

    def without_lit_data(self) -> "Treatment":
        self.with_lit_data = False
        return self

    def with_removal(self, removal: removal_model.RemovalPercent):
        if self.requires_mixture:
            raise TypeError(f"Treatment '{self.id}' doesn't support setting its removal. "
                            f"It expects a Mixture object.")
        self.removal = removal
        return self

    def with_mixture(self, mixture: mixture_model.Mixture):
        if not self.requires_mixture:
            raise TypeError(f"Treatment '{self.id}' doesn't support mixtures. It expects a RemovalPercent object."
                            f" Mixtures are supported by 'dil*' and 'sepev' treatments")
        self.mixture = mixture
        return self

    def clone(
            self,
            id: str | None = None,
            name: str | None = None,
            input_matrix: list[Matrix] | None = None,
            output_matrix: Matrix | None = None,
            with_lit_data: bool | None = None,
            removal: removal_model.RemovalPercent | None = None,
            mixture: mixture_model.Mixture | None = None
    ):
        id = id or self.id
        name = name or self.name
        input_matrix = input_matrix or self.input_matrix
        output_matrix = output_matrix or self.output_matrix
        with_lit_data = with_lit_data if with_lit_data is not None else self.with_lit_data
        removal = removal or self.removal
        mixture = mixture or self.mixture
        return Treatment(id, self.group, name, input_matrix, output_matrix, with_lit_data, removal, mixture)

    def __hash__(self):
        return hash(self.id)


@dtc.dataclass
class TreatmentTrain:
    treatments: list[Treatment]

    def copy(self):
        return TreatmentTrain([t.clone() for t in self.treatments])

    def validate_matrices(self, input_matrix: Matrix):
        for i in range(len(self)):
            if input_matrix not in self[i].input_matrix:
                raise ValueError(f"incompatible input matrix ('{input_matrix.id}') for treatment '{self[i].id}'"
                                 f" at index {i}.\n"
                                 f"Expected one of [{' '.join([m.id for m in self[i].input_matrix])}]")
            input_matrix = self[i].get_output_matrix(input_matrix)

    def validate_mixtures(self):
        for i, treatment in enumerate(self):
            if treatment.requires_mixture and treatment.mixture is None:
                raise ValueError(f"Expected treatment '{treatment.id}' at index {i} to contain mixture data"
                                 f" but treatment.mixture was None.")

    def output_matrix(self, input_matrix: Matrix) -> Matrix:
        out_mat = input_matrix
        for t in self:
            out_mat = t.get_output_matrix(out_mat)
        return out_mat

    def __getitem__(self, item) -> Treatment:
        return self.treatments[item]

    def __len__(self):
        return len(self.treatments)

    def __iter__(self) -> Iterator[Treatment]:
        for t in self.treatments:
            yield t


class Treatments:
    wwt1 = Treatment("wwt1", TreatmentGroup.WWT, "Primary wastewater treatment",
                     [Matrices.rww, Matrices.iww, Matrices.hww, Matrices.stw, Matrices.lww],
                     Matrices.no_change)
    wwt2 = Treatment("wwt2", TreatmentGroup.WWT, "Secondary wastewater treatment",
                     [Matrices.rww, Matrices.iww, Matrices.hww, Matrices.stw, Matrices.lww], Matrices.tww)
    wwtt = Treatment("wwtt", TreatmentGroup.WWT, "Combination of primary and secondary wastewater treatment",
                     [Matrices.rww, Matrices.iww, Matrices.hww, Matrices.stw, Matrices.lww], Matrices.tww)
    wwco = Treatment("wwco", TreatmentGroup.WWT, "Tertiary wastewater treatment: Coagulation and filtration",
                     [Matrices.tww, Matrices.iww], Matrices.tww)
    wwel = Treatment("wwel", TreatmentGroup.WWT, "Tertiary wastewater treatment: Electro-oxidation (e-peroxone)",
                     [Matrices.tww, Matrices.iww], Matrices.tww)
    wwuf = Treatment("wwuf", TreatmentGroup.WWT, "Tertiary wastewater treatment: Ultrafiltration",
                     [Matrices.tww, Matrices.iww], Matrices.tww)
    wwnf = Treatment("wwnf", TreatmentGroup.WWT, "Tertiary wastewater treatment: Nanofiltration",
                     [Matrices.tww, Matrices.iww], Matrices.tww)
    wwro = Treatment("wwro", TreatmentGroup.WWT, "Tertiary wastewater treatment: Reverse Osmosis",
                     [Matrices.tww, Matrices.iww], Matrices.tww)
    wwmb = Treatment("wwmb", TreatmentGroup.WWT, "Tertiary wastewater treatment: Membrane bioreactor",
                     [Matrices.rww, Matrices.iww, Matrices.hww, Matrices.stw, Matrices.tww, Matrices.lww],
                     Matrices.tww)
    wwsl = Treatment("wwsl", TreatmentGroup.WWT,
                     "Combination of primary and secondary wastewater treatment: dewatered sludge",
                     [Matrices.rww, Matrices.hww], Matrices.sdg)
    wetl = Treatment("wetl", TreatmentGroup.WWT, "Additional treatment: Constructed wetland",
                     [Matrices.rww, Matrices.iww, Matrices.hww, Matrices.stw, Matrices.tww, Matrices.lww],
                     Matrices.tww)
    dilsw = Treatment("dilsw", TreatmentGroup.MIX, "Dilution by surface water", [Matrices.tww, Matrices.stw],
                      Matrices.suw)
    dilww = Treatment("dilww", TreatmentGroup.MIX, "Dilution by household wastewater",
                      [Matrices.iww, Matrices.lww, Matrices.rww, Matrices.tww], Matrices.rww)
    dilgw = Treatment("dilgw", TreatmentGroup.MIX, "Dilution by groundwater", [Matrices.bfw, Matrices.pow, Matrices.grw],
                      Matrices.grw)
    dilpr = Treatment("dilpr", TreatmentGroup.MIX, "Dilution by process water (from minor secondary stream)",
                      [Matrices.tww, Matrices.iww, Matrices.hww, Matrices.rww, Matrices.lww, Matrices.drw],
                      Matrices.no_change)
    dilrw = Treatment("dilrw", TreatmentGroup.MIX, "Dilution by soil irrigation water",
                      [Matrices.suw, Matrices.tww, Matrices.stw, Matrices.sdg], Matrices.pow)
    sepev = Treatment("sepev", TreatmentGroup.MIX, "Separation dueto evaporation", [Matrices.suw, Matrices.pow],
                      Matrices.no_change)
    npdgw = Treatment("npdgw", TreatmentGroup.NAP, "NaturalProcess: Degradation in surface water (biotic and abiotic)",
                      [Matrices.suw], Matrices.no_change)
    npdgg = Treatment("npdgg", TreatmentGroup.NAP, "NaturalProcess: Degradation in groundwater (biotic and abiotic)",
                      [Matrices.grw], Matrices.no_change)
    npbk = Treatment("npbk", TreatmentGroup.NAP, "Natural Process: Bank filtration", [Matrices.suw], Matrices.bfw)
    npdgs = Treatment("npdgs", TreatmentGroup.NAP, "NaturalProcess: Degradation in soil(biotic and abiotic)",
                      [Matrices.pow], Matrices.no_change)
    dwex = Treatment("dwex", TreatmentGroup.DWT, "Drinking water treatment: anion exchange",
                     [Matrices.suw, Matrices.bfw, Matrices.grw, Matrices.drw, Matrices.tww, Matrices.stw],
                     Matrices.drw)
    dwcy = Treatment("dwcy", TreatmentGroup.DWT, "Drinking water treatment: cyclodextrin",
                     [Matrices.suw, Matrices.bfw, Matrices.grw, Matrices.drw, Matrices.tww, Matrices.stw],
                     Matrices.drw)
    dwae = Treatment("dwae", TreatmentGroup.DWT, "Drinking water treatment: aeration",
                     [Matrices.suw, Matrices.bfw, Matrices.grw, Matrices.drw, Matrices.tww, Matrices.stw],
                     Matrices.drw)
    dwrf = Treatment("dwrf", TreatmentGroup.DWT, "Drinking water treatment: rapid filtration",
                     [Matrices.suw, Matrices.bfw, Matrices.grw, Matrices.drw, Matrices.tww, Matrices.stw],
                     Matrices.drw)
    dwro = Treatment("dwro", TreatmentGroup.DWT, "Drinking water treatment: reverse osmosis",
                     [Matrices.suw, Matrices.bfw, Matrices.grw, Matrices.drw, Matrices.tww,
                      Matrices.stw], Matrices.drw)
    dwcl = Treatment("dwcl", TreatmentGroup.DWT, "Drinking water treatment: chloride",
                     [Matrices.suw, Matrices.bfw, Matrices.grw, Matrices.drw,
                      Matrices.tww, Matrices.stw], Matrices.drw)
    dwna = Treatment("dwna", TreatmentGroup.DWT, "Drinking water treatment: NaOCl",
                     [Matrices.suw, Matrices.bfw, Matrices.grw, Matrices.drw, Matrices.tww, Matrices.stw],
                     Matrices.drw)
    dwuv = Treatment("dwuv", TreatmentGroup.DWT, "Drinking water treatment: UV",
                     [Matrices.suw, Matrices.bfw, Matrices.grw, Matrices.drw, Matrices.tww, Matrices.stw],
                     Matrices.drw)
    dwac = Treatment("dwac", TreatmentGroup.DWT, "Drinking water treatment: granular activated carbon",
                     [Matrices.suw, Matrices.bfw, Matrices.grw, Matrices.drw, Matrices.tww, Matrices.stw],
                     Matrices.drw)
    dwuf = Treatment("dwuf", TreatmentGroup.DWT, "Drinking water treatment: ultra filtration",
                     [Matrices.suw, Matrices.bfw, Matrices.grw, Matrices.drw, Matrices.tww, Matrices.stw],
                     Matrices.drw)
    dwde = Treatment("dwde", TreatmentGroup.DWT, "Drinking water treatment: decantation",
                     [Matrices.suw, Matrices.bfw, Matrices.grw, Matrices.drw, Matrices.tww, Matrices.stw],
                     Matrices.drw)
    dwoz = Treatment("dwoz", TreatmentGroup.DWT, "Drinking water treatment: disinfection with chlorineor ozone",
                     [Matrices.suw, Matrices.bfw, Matrices.grw, Matrices.drw, Matrices.tww, Matrices.stw],
                     Matrices.drw)
    dwpr = Treatment("dwpr", TreatmentGroup.DWT,
                     "Drinking water treatment: pretreatment with pre disinfection (chlorine)",
                     [Matrices.suw, Matrices.bfw, Matrices.grw, Matrices.drw, Matrices.tww, Matrices.stw],
                     Matrices.drw)
    dwco = Treatment("dwco", TreatmentGroup.DWT, "Drinking water treatment: coagulation and flocculation",
                     [Matrices.suw, Matrices.bfw, Matrices.grw, Matrices.drw, Matrices.tww, Matrices.stw],
                     Matrices.drw)
    grpz = Treatment("grpz", TreatmentGroup.GWT,
                     "Groundwater treatment: Persulfate-based insitu chemical oxidation- (n)ZVI",
                     [Matrices.grw],
                     Matrices.no_change)
    grpf = Treatment("grpf", TreatmentGroup.GWT,
                     "Groundwater treatment: Persulfate-based insitu chemical oxidation- (n)ZVI+Fe(VI)",
                     [Matrices.grw], Matrices.no_change)
    gren = Treatment("gren", TreatmentGroup.GWT,
                     "Groundwater treatment: catalysis by extra cellular ligninolytic enzymes",
                     [Matrices.grw], Matrices.no_change)
    gruc = Treatment("gruc", TreatmentGroup.GWT, "Groundwater treatment: ultrasonic cavitation",
                     [Matrices.grw], Matrices.no_change)

