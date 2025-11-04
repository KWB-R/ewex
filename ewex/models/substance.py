import dataclasses as dtc
from enum import Enum

import ewex.models.reference as reference_model
import ewex.models.starting_concentration as sc_model


class SubstanceGroup(Enum):
    PFAS = "PFAS"
    iPMT = "iPM(T)"
    Pharmaceutical = "Pharmaceutical"


@dtc.dataclass
class Substance:
    id: str
    group: SubstanceGroup
    name: str
    CAS: str
    starting_concentration: sc_model.StartingConcentration | None = None
    reference: reference_model.Reference | None = None

    def with_starting_concentration(self, starting_concentration: sc_model.StartingConcentration):
        self.starting_concentration = starting_concentration
        return self

    def with_reference(self, reference: reference_model.Reference):
        self.reference = reference
        return self

    def __hash__(self):
        return hash(self.id)


class Substances:
    tfmsa = Substance("tfmsa", SubstanceGroup.PFAS, "Trifluoromethanesulfonic acid", "1493-13-6")
    pfba = Substance("pfba", SubstanceGroup.PFAS, "Perfluorobutanoic acid", "375-22-4")
    pfpea = Substance("pfpea", SubstanceGroup.PFAS, "Perfluoropentanoic acid", "2706-90-3")
    pfhxa = Substance("pfhxa", SubstanceGroup.PFAS, "Perfluorohexanoic acid", "307-24-4")
    pfhpa = Substance("pfhpa", SubstanceGroup.PFAS, "Perfluoroheptanoic acid", "375-85-9")
    pfoa = Substance("pfoa", SubstanceGroup.PFAS, "Perfluorooctanoic acid", "335-67-1")
    pfna = Substance("pfna", SubstanceGroup.PFAS, "Perfluorononanoic acid", "375-95-1")
    pfda = Substance("pfda", SubstanceGroup.PFAS, "Perfluorodecanoic acid", "335-76-2")
    pfunda = Substance("pfunda", SubstanceGroup.PFAS, "Perfluoroundecanoic acid", "2058-94-8")
    pfdoda = Substance("pfdoda", SubstanceGroup.PFAS, "Perfluorododecanoic acid", "307-55-1")
    pftrda = Substance("pftrda", SubstanceGroup.PFAS, "Perfluorotridecanoic acid", "72629-94-8")
    pfteda = Substance("pfteda", SubstanceGroup.PFAS, "Perfluoro-n-tetradecanoic acid ", "376-06-7")
    pfets = Substance("pfets", SubstanceGroup.PFAS, "Pentafluoroethanesulfonic acid", "354-88-1")
    pfprs = Substance("pfprs", SubstanceGroup.PFAS, "Perfluoropropan-1-sulfonic cid", "423-41-6")
    pfbs = Substance("pfbs", SubstanceGroup.PFAS, "Perfluorobutane sulfonic acid", "375-73-5")
    pfpes = Substance("pfpes", SubstanceGroup.PFAS, "Perfluoropentane sulfonic acid", "2706-91-4")
    pfhxs = Substance("pfhxs", SubstanceGroup.PFAS, "Perfluorohexane sulfonic acid", "355-46-4")
    pfhps = Substance("pfhps", SubstanceGroup.PFAS, "Perfluoroheptane sulfonic acid", "375-92-8")
    pfos = Substance("pfos", SubstanceGroup.PFAS, "Perfluorooctane sulfonic acid", "1763-23-1")
    pfns = Substance("pfns", SubstanceGroup.PFAS, "Perfluorononane sulfonic acid ", "01.12.2723")
    pfds = Substance("pfds", SubstanceGroup.PFAS, "Perfluorodecane sulfonic acid", "335-77-3")
    pfunds = Substance("pfunds", SubstanceGroup.PFAS, "Perfluoroundecane sulfonic acid", "749786-16-1")
    pfdods = Substance("pfdods", SubstanceGroup.PFAS, "Perfluorododecane sulfonic acid", "335-77-3")
    pftrds = Substance("pftrds", SubstanceGroup.PFAS, "Perfluorotridecane sulfonic acid", "791563-89-8")
    _10_2ftca = Substance("_10_2ftca", SubstanceGroup.PFAS, "10:2 FTCA, 10:2 fluorotelomer carboxylic acid",
                          "53826-13-4")
    _4_2ftca = Substance("_4_2ftca", SubstanceGroup.PFAS, "4:2 FTCA, 4:2 fluorotelomer carboxylic acid", None)
    _6_2dipap = Substance("_6_2dipap", SubstanceGroup.PFAS, "6:2diPAP, 6:2-Fluortelomerphosphatdiester", "57677-95-9")
    _6_2ftca = Substance("_6_2ftca", SubstanceGroup.PFAS, "6:2 FTCA, 6:2 fluorotelomer carboxylic acid", "99199-59-4")
    _8_2ftca = Substance("_8_2ftca", SubstanceGroup.PFAS, "8:2 FTCA, 8:2 fluorotelomer carboxylic acid", "161094-76-4")
    _8_2ftuca = Substance("_8_2ftuca", SubstanceGroup.PFAS,
                          "(E) 8:2 FTUCA (2E)-3-(Perfluoroheptyl)-3-fluoroprop-2-enoic acid", "70887-84-2")
    nadona = Substance("nadona", SubstanceGroup.PFAS, "NaDONA, Dodecafluoro-3H-4,8-dioxanonanoic Acid", None)
    adona = Substance("adona", SubstanceGroup.PFAS, "ADONA, 3H-Perfluoro-3-[(3-methoxy-propoxy)propanoic acid]",
                      "919005-14-4")
    etfosa = Substance("etfosa", SubstanceGroup.PFAS, "EtFOSA, n-Ethyl perfluorooctane sulfonamide ethanol",
                       "1691-99-2")
    etfosaa = Substance("etfosaa", SubstanceGroup.PFAS, "EtFOSAA, n-Ethyl perfluorooctane sulfonamide acetic acid ",
                        "2991-50-6")
    fosa = Substance("fosa", SubstanceGroup.PFAS,
                     "FOSA, 1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,8-Heptadecafluorooctane-1-sulfonamide (also pfosa)",
                     "754-91-6")
    fosaa = Substance("fosaa", SubstanceGroup.PFAS, "FOSAA, Perfluorooctane sulfonamide acetic acid ", "2806-24-8")
    mefosaa = Substance("mefosaa", SubstanceGroup.PFAS, "MeFOSAA, n-Methyl perfluorooctane sulfonamide acetic acid ",
                        "2355-31-9")
    mefosa = Substance("mefosa", SubstanceGroup.PFAS, "MeFOSA, n-Methyl perfluorooctane sulfonamide", "31506-32-8")
    _8_2dipap = Substance("_8_2dipap", SubstanceGroup.PFAS, "8:2 diPAP, Bis(1H,1H,2H,2H-perfluorodecyl) phosphate",
                          "678-41-1")
    _10_2ftoh = Substance("_10_2ftoh", SubstanceGroup.PFAS, "10:2 FTOH, 10:2 1H,1H,2H,2H-Perfluorododecan-1-ol ",
                          "865-86-1")
    _12_2ftoh = Substance("_12_2ftoh", SubstanceGroup.PFAS, "12:2 FTOH, 1H,1H,2H,2H-Perfluorotetradecan-1-ol",
                          "39239-77-5")
    _14_2ftoh = Substance("_14_2ftoh", SubstanceGroup.PFAS, "14:2 FTOH, 14:2 Fluorotelomer alcohol", "60699-51-6")
    _2_2ftoh = Substance("_2_2ftoh", SubstanceGroup.PFAS, "2:2 FTOH, 2:2 1H,1H,2H,2H-Perfluorobutan-1-ol", "54949-74-5")
    _4_2ftoh = Substance("_4_2ftoh", SubstanceGroup.PFAS, "4:2 FTOH, 2-(Perfluorobutyl)ethanol", "2043-47-2")
    _6_2ftab = Substance("_6_2ftab", SubstanceGroup.PFAS, "6:2 FTAB, 6:2 fluorotelomer sulfonamide alkylbetaine",
                         "34455-29-3")
    _6_2ftoh = Substance("_6_2ftoh", SubstanceGroup.PFAS, "6:2 FTOH, 6:2 Fluorotelomer alcohol", "647-42-7")
    _8_2ftoh = Substance("_8_2ftoh", SubstanceGroup.PFAS, "8:2 FTOH, 8:2 Fluorotelomer alcohol", "678-39-7")
    fts_4_2 = Substance("_4_2fts", SubstanceGroup.PFAS, "4:2 FTS", "757124-72-4")
    fts_6_2 = Substance("_6_2fts", SubstanceGroup.PFAS, "6:2 FTS, Sodium 1H,1H,2H,2H-perfluorooctanesulfonate",
                        "27619-97-2")
    fts_8_2 = Substance("_8_2fts", SubstanceGroup.PFAS, "8:2 FTS", "39108-34-4")
    mefbsa = Substance("mefbsa", SubstanceGroup.PFAS, "MeFBSA, N-Methylperfluoro-1-butanesulfonamide", "68298-12-4")
    fhxsa = Substance("fhxsa", SubstanceGroup.PFAS, "1,1,2,2,3,3,4,4,5,5,6,6,6-tridecafluoro-1-hexanesulfonamide",
                      "41997-13-1")
    _6_2ftsam = Substance("_6_2ftsam", SubstanceGroup.PFAS, "6:2FTSAM, 6:2 sulfonamide alkylbetaine ", "34455-29-3")
    pfmoaa = Substance("pfmoaa", SubstanceGroup.PFAS, "PFMOAA, Perfluoro-2-methoxyacetic acid", "674-13-5")
    pfmopra = Substance("pfmopra", SubstanceGroup.PFAS, "PFMOPrA, Perfluoro-3-methoxy-propanoic acid", "377-73-1")
    pfmoba = Substance("pfmoba", SubstanceGroup.PFAS, "PFMOBA, Perfluoro-4-methoxy-butanic acid", "863090-89-5")
    pfpropra = Substance("pfpropra", SubstanceGroup.PFAS, "PFPrOPrA, Perfluoro-2-propoxypropanoic acid", "13252-13-6")
    pfo2hxa = Substance("pfo2hxa", SubstanceGroup.PFAS,
                        "PFO2HxA, 2-[difluoro(trifluoromethoxy)methoxy]-2,2-difluoroacetic acid", "39492-88-1")
    pfo3oa = Substance("pfo3oa", SubstanceGroup.PFAS, "PFO3OA, Perfluoro-3,5,7-trioxaoctanoic acid", "39492-89-2")
    pfo4da = Substance("pfo4da", SubstanceGroup.PFAS, "PFO4DA,Perfluoro-3,5,7,9-butaoxadecanoic acid", "39492-90-5")
    genx = Substance("genx", SubstanceGroup.PFAS, "GenX, ,3,3,3-tetrafluoro-2-(heptafluoropropoxy) propanoate",
                     "62037-80-3")
    _14_d = Substance("_14_d", SubstanceGroup.iPMT, "1,4-dioxane", "123-91-1")
    benzo = Substance("benzo", SubstanceGroup.iPMT, "Benzotriazole,1H-1,2,3-benzotriazole", "95-14-7")
    bpa = Substance("bpa", SubstanceGroup.iPMT, "Bisphenol A, 4,4'-(propan-2,2-diil)difenolo", "80-05-7")
    cbz = Substance("cbz", SubstanceGroup.Pharmaceutical, "Carbamazepin5H-dibenzo [b,f]azepina-5-carbossammide",
                    "298-46-4")
    dep = Substance("dep", SubstanceGroup.iPMT, "diethylphthalate", "84-66-2")
    dbp = Substance("dbp", SubstanceGroup.iPMT, "dibuthylphthalate", "84-74-2")
    diuron = Substance("diuron", SubstanceGroup.iPMT, "diuron", "330-54-1")
