# import dataclasses as dtc
# import warnings
#
# import numpy as np
#
# from ewex.models.reference import Reference
# from ewex.models.starting_concentration import StartingConcentration
# import ewex.models.removal_percent as rmv
# from ewex.models.matrix import Matrix, Matrices
# from ewex.models.substance import Substance, Substances
# from ewex.models.treatment import Treatments, TreatmentTrain
# from ewex.models.mixture import Mixture
# from ewex.models.scenario import Scenario
#
#
# @dtc.dataclass
# class CaseStudy:
#     name: str
#     scenarios: list[Scenario]
#
#
# # {scenario_index: {treatment_index: mixture}}
# mixtures = [
#         #  dilsw
#         Mixture(0.715, 0.058, 0, 0),
#         Mixture(0.5, 0.058, 0, 0),
#         Mixture(0.715, 0.058, 10, 2),
# ]
#
# treatment_dwac = TreatmentTrain([
#     Treatments.wwtt,
#     Treatments.wwco,
#     Treatments.dilsw,
#     Treatments.npbk,
#     Treatments.dilgw.with_mixture(Mixture(0.225, 0.013, 0, 0)),
#     Treatments.dwae,
#     Treatments.dwrf,
#     Treatments.dwac
# ])
# treatment_dwex = TreatmentTrain([
#     Treatments.wwtt,
#     Treatments.wwco,
#     Treatments.dilsw,
#     Treatments.npbk,
#     Treatments.dilgw.with_mixture(Mixture(0.225, 0.013, 0, 0)),
#     Treatments.dwae,
#     Treatments.dwrf,
#     Treatments.dwex
# ])
# dwac, dwex = [], []
# for m in mixtures:
#     ac = treatment_dwac.copy()
#     ac[2].with_mixture(m)
#     dwac += [ac]
#     ex = treatment_dwex.copy()
#     ex[2].with_mixture(m)
#
# removals = {
#     Treatments.dwac: {
#         Substances.pfba: rmv.RemovalPercent(np.array([50])),
#         Substances.pfbs: rmv.RemovalPercent(np.array([50])),
#         Substances.pfda: rmv.RemovalPercent(np.array([50])),
#         Substances.pfhpa: rmv.RemovalPercent(np.array([50])),
#         Substances.pfhxa: rmv.RemovalPercent(np.array([50])),
#         Substances.pfhxs: rmv.RemovalPercent(np.array([50])),
#         Substances.pfna: rmv.RemovalPercent(np.array([50])),
#         Substances.pfoa: rmv.RemovalPercent(np.array([50])),
#         Substances.pfos: rmv.RemovalPercent(np.array([50])),
#         Substances.pfpea: rmv.RemovalPercent(np.array([50])),
#         Substances.pfpes: rmv.RemovalPercent(np.array([50])),
#         Substances.benzo: rmv.RemovalPercent(np.array([50])),
#         Substances.cbz: rmv.RemovalPercent(np.array([50])),
#     },
#     Treatments.dwex: {
#         Substances.pfba: rmv.RemovalPercent(np.array([50])),
#         Substances.pfbs: rmv.RemovalPercent(np.array([50])),
#         Substances.pfda: rmv.RemovalPercent(np.array([50])),
#         Substances.pfhpa: rmv.RemovalPercent(np.array([50])),
#         Substances.pfhxa: rmv.RemovalPercent(np.array([50])),
#         Substances.pfhxs: rmv.RemovalPercent(np.array([50])),
#         Substances.pfna: rmv.RemovalPercent(np.array([50])),
#         Substances.pfoa: rmv.RemovalPercent(np.array([50])),
#         Substances.pfos: rmv.RemovalPercent(np.array([50])),
#         Substances.pfpea: rmv.RemovalPercent(np.array([50])),
#         Substances.pfpes: rmv.RemovalPercent(np.array([50])),
#         Substances.benzo: rmv.RemovalPercent(np.array([50])),
#         Substances.cbz: rmv.RemovalPercent(np.array([50])),
#     }
# }
#
# substances = [
#     Substances.pfba \
#         # .with_starting_concentration(StartingConcentration(np.array([100.]))) \
#         .with_reference(Reference("123", 0, 2020, "")),
#     Substances.pfbs \
# #         .with_starting_concentration(StartingConcentration(np.array([100.]))) \
#         .with_reference(Reference("123", 0, 2020, "")),
#     Substances.pfda \
# #         .with_starting_concentration(StartingConcentration(np.array([100.]))) \
#         .with_reference(Reference("123", 0, 2020, "")),
#     Substances.pfhpa \
# #         .with_starting_concentration(StartingConcentration(np.array([100.]))) \
#         .with_reference(Reference("123", 0, 2020, "")),
#     Substances.pfhxa \
# #         .with_starting_concentration(StartingConcentration(np.array([100.]))) \
#         .with_reference(Reference("123", 0, 2020, "")),
#     Substances.pfhxs \
# #         .with_starting_concentration(StartingConcentration(np.array([100.]))) \
#         .with_reference(Reference("123", 0, 2020, "")),
#     Substances.pfna \
# #         .with_starting_concentration(StartingConcentration(np.array([100.]))) \
#         .with_reference(Reference("123", 0, 2020, "")),
#     Substances.pfoa \
# #         .with_starting_concentration(StartingConcentration(np.array([100.]))) \
#         .with_reference(Reference("123", 0, 2020, "")),
#     Substances.pfos \
# #         .with_starting_concentration(StartingConcentration(np.array([100.]))) \
#         .with_reference(Reference("123", 0, 2020, "")),
#     Substances.pfpea \
# #         .with_starting_concentration(StartingConcentration(np.array([100.]))) \
#         .with_reference(Reference("123", 0, 2020, "")),
#     Substances.pfpes \
# #         .with_starting_concentration(StartingConcentration(np.array([100.]))) \
#         .with_reference(Reference("123", 0, 2020, "")),
#     Substances.benzo \
# #         .with_starting_concentration(StartingConcentration(np.array([100.]))) \
#         .with_reference(Reference("123", 0, 2020, "")),
#     Substances.cbz \
# #         .with_starting_concentration(StartingConcentration(np.array([100.]))) \
#         .with_reference(Reference("123", 0, 2020, "")),
# ]
#
# dwac_scenario = []
# for i, s in enumerate(substances):
#     for j, t in enumerate(dwac):
#         r = removals[Treatments.dwac][s]
#         t[-1].with_removal(r)
#         dwac_scenario += [Scenario(
#             f"berlin-{s.id}-dwac-{j}",
#             input_matrix=Matrices.rww,
#             substance=s,
#             treatment_train=t,
#         )]
#
# dwex_scenario = []
# for i, s in enumerate(substances):
#     for j, t in enumerate(dwac):
#         r = removals[Treatments.dwex][s]
#         t[-1].with_removal(r)
#         dwex_scenario += [Scenario(
#             f"berlin-{s.id}-dwex-{j}",
#             input_matrix=Matrices.rww,
#             substance=s,
#             treatment_train=t,
#         )]
#
# berlin = CaseStudy(
#     "Berlin", [*treatment_dwac, *treatment_dwex]
# )
# #
# # groundwater_remediation = CaseStudy(
# #     "Groundwater Remediation",
# #     [
# #         Scenario(
# #             "persulfate",
# #             Matrices.drw,
# #             Substances.pfoa,
# #             TreatmentTrain([
# #                 Treatments.dilgw.with_mixture(Mixture(0, 0, 0, 0))
# #             ]),
# #             reference=Reference(
# #                 "TrinkwV 2023 + DOI 10.21945/RIVM-2018-0070",
# #                 ref_value_ng_l=5.0,
# #                 year=2023,
# #                 comments="Use of relative potency factors: (20 / 4 / RPF = 1)"
# #             )
# #         ),
# #         Scenario(
# #             "ultra cavitation",
# #             Matrices.grw,
# #             Substances.pfoa,
# #             TreatmentTrain([
# #                 Treatments.dilgw.with_mixture(Mixture(0, 0, 0, 0))
# #             ]),
# #             # https://pd.lubw.de/54057
# #             # Abbildung 5.1
# #             starting_concentration=StartingConcentration(np.array([1000., 3000.]))
# #         )
# #     ]
# # )
# #
# # nutrient_recovery = CaseStudy(
# #     "Nutrient Recovery",
# #     [
# #         Scenario(
# #             "standard",
# #             Matrices.lww,
# #             Substances.pfoa,
# #             TreatmentTrain([
# #                 Treatments.wwro.with_removal(rmv.RemovalPercent(np.array([100]))),
# #                 Treatments.dilww.with_mixture(Mixture(
# #                     0.875, 0.038265306, 45, 22.44897959,
# #                     "x entered as range between 0.8 and 0.95, "
# #                     "c entered as range between 1.0 and 89.0"
# #                 )),
# #                 Treatments.sepev.with_mixture(Mixture(
# #                     0.21, 0.015306122, 0, 0, "x entered as range between 0.18 and 0.24"
# #                 )),
# #                 Treatments.dilpr.with_mixture(Mixture(
# #                     0.16, 0.016, 19180, 2290,
# #                     "x standard deviation assumed to be 10% of mean value,"
# #                     " process water characteristics based on D4.5 table 12"
# #                 )),
# #                 Treatments.dilrw.with_mixture(Mixture(
# #                     0.99948, 9.18E-05, 0, 0, "x entered as range between 0.9993 and 0.99966"
# #                 ))
# #             ]),
# #             starting_concentration=StartingConcentration(
# #                 # PROMISCES D4.5
# #                 # Plant No.3 (Table 12), minimum and maximum from mean +- 1.96 sd
# #                 np.array([3600., 5900.])
# #             ),
# #             reference=Reference(
# #                 "",
# #                 ref_value_ng_l=7.36,
# #                 year=-1,
# #                 comments="Based on EFSA PFAS-4 TWI,"
# #                          " BCF and 70kg Body weights,"
# #                          " 0.26 lettuce consumption and 10% other sources safety factor"
# #             )
# #         ),
# #         Scenario(
# #             "cont_irrigation",
# #             Matrices.lww,
# #             Substances.pfoa,
# #             TreatmentTrain([
# #                 Treatments.wwro.with_removal(rmv.RemovalPercent(np.array([100]))),
# #                 Treatments.dilww.with_mixture(Mixture(
# #                     0.875, 0.038265306, 45, 22.44897959,
# #                     "x entered as range between 0.8 and 0.95, c entered as range between 1.0 and 89.0"
# #                 )),
# #                 Treatments.sepev.with_mixture(Mixture(
# #                     0.21, 0.015306122, 0, 0,
# #                     "x entered as range between 0.18 and 0.24"
# #                 )),
# #                 Treatments.dilpr.with_mixture(Mixture(
# #                     0.16, 0.016, 19180, 2290,
# #                     "x standard deviation assumed to be 10% of mean value,"
# #                     " process water characteristics based on D4.5 table 12"
# #                 )),
# #                 Treatments.dilrw.with_mixture(Mixture(
# #                     0.99948, 9.18e-5, 10, 5,
# #                     "x entered as range between 0.9993 and 0.99966"
# #                 ))
# #             ]),
# #             starting_concentration=StartingConcentration(
# #                 # PROMISCES D4.5
# #                 # Plant No.3 (Table 12), minimum and maximum from mean +- 1.96 sd
# #                 np.array([3600., 5900.])
# #             ),
# #             reference=Reference(
# #                 "",
# #                 ref_value_ng_l=7.36,
# #                 year=-1,
# #                 comments="Based on EFSA PFAS-4 TWI,"
# #                          " BCF and 70kg Body weights,"
# #                          " 0.26 lettuce consumption and 10% other sources safety factor"
# #             )
# #         ),
# #
# #     ]
# # )
# # TODO:
# # water_cycle_b = CaseStudy(
# #     name="Water Cycle B",
# #     mixtures=[
# #         Mixture(0.715, 0.0586734693877551, 0, 0,
# #                 Treatments.dilsw, Substances.pfos, "standard",
# #                 "x entered as range between 0.6 and 0.83"),
# #         Mixture(0.225, 0.0127551020408163, 0, 0,
# #                 Treatments.dilgw, Substances.pfos, "standard",
# #                 "x entered as range between 0.2 and 0.25"),
# #         Mixture(0.715, 0.0586734693877551, 0, 0,
# #                 Treatments.dilsw, Substances.pfoa, "standard",
# #                 "x entered as range between 0.6 and 0.83"),
# #         Mixture(0.225, 0.0127551020408163, 0, 0,
# #                 Treatments.dilgw, Substances.pfoa, "standard",
# #                 "x entered as range between 0.2 and 0.25"),
# #         Mixture(0.715, 0.0586734693877551, 0, 0,
# #                 Treatments.dilsw, Substances.pfna, "standard",
# #                 "x entered as range between 0.6 and 0.8"),
# #         Mixture(0.225, 0.0127551020408163, 0, 0,
# #                 Treatments.dilgw, Substances.pfna, "standard",
# #                 "x entered as range between 0.2 and 0.25"),
# #         Mixture(0.715, 0.0586734693877551, 0, 0,
# #                 Treatments.dilsw, Substances.pfhxs, "standard",
# #                 "x entered as range between 0.6 and 0.83"),
# #         Mixture(0.225, 0.0127551020408163, 0, 0,
# #                 Treatments.dilgw, Substances.pfhxs, "standard",
# #                 "x entered as range between 0.2 and 0.25"),
# #         Mixture(0.715, 0.0586734693877551, 0, 0,
# #                 Treatments.dilsw, Substances.benzo, "standard",
# #                 "x entered as range between 0.6 and 0.83"),
# #         Mixture(0.225, 0.0127551020408163, 0, 0,
# #                 Treatments.dilgw, Substances.benzo, "standard",
# #                 "x entered as range between 0.2 and 0.25"),
# #         Mixture(0.715, 0.0586734693877551, 0, 0,
# #                 Treatments.dilsw, Substances._14_d, "standard",
# #                 "x entered as range between 0.6 and 0.83"),
# #         Mixture(0.225, 0.012755102040816323, 0, 0,
# #                 Treatments.dilgw, Substances._14_d, "standard",
# #                 "x entered as range between 0.2 and 0.25")
# #     ],
# #     removal_percents=[],
# #     references=[
# #         Reference("TrinkwV 2023 + DOI 10.21945/RIVM-2018-0070", Substances.pfos, Matrices.drw, 3.07,
# #                   2023,
# #                   "Use of relative potency factors: (20 / 4 / RPF = 2)"),
# #         Reference("TrinkwV 2023 + DOI 10.21945/RIVM-2018-0070", Substances.pfoa, Matrices.drw, 6.13,
# #                   2023,
# #                   "Use of relative potency factors: (20 / 4 / RPF = 1)"),
# #         Reference("TrinkwV 2023 + DOI 10.21945/RIVM-2018-0070", Substances.pfna, Matrices.drw, 0.61,
# #                   2023,
# #                   "Use of relative potency factors: (20 / 4 / RPF = 10)"),
# #         Reference("TrinkwV 2023 + DOI 10.21945/RIVM-2018-0070", Substances.pfhxs, Matrices.drw, 10.18,
# #                   2023,
# #                   "Use of relative potency factors: (20 / 4 / RPF = 0.6)"),
# #         Reference("UBA GOW (july 2020)", Substances.benzo, Matrices.drw, 3000.0,
# #                   -1, ""),
# #         Reference("CA State Water Board 14dioxane", Substances._14_d, Matrices.drw, 1000.0,
# #                   -1, "")
# #     ],
# #     starting_concentration=[
# #         # Benedikt Master Thesis
# #         StartingConcentration(np.array([0.0, 1793.0]), Substances._14_d, Matrices.rww),
# #         StartingConcentration(np.array([17000.0, 44000.0]), Substances.benzo, Matrices.rww),
# #     ]
# # )
# #
# # water_cycle_let = CaseStudy(
# #     name="Water Cycle LET",
# #     mixtures=[
# #         Mixture(0.715, 0.0586734693877551, 0, 0,
# #                 Treatments.dilsw, Substances.pfos, "small_low_none",
# #                 "x entered as range between 0.6 and 0.83"),
# #         Mixture(0.225, 0.0127551020408163, 0, 0,
# #                 Treatments.dilgw, Substances.pfos, "small_low_none",
# #                 "x entered as range between 0.2 and 0.25"),
# #         Mixture(0.715, 0.0586734693877551, 0, 0,
# #                 Treatments.dilsw, Substances.pfos, "small_low_data",
# #                 "x entered as range between 0.6 and 0.83"),
# #         Mixture(0.225, 0.0127551020408163, 0, 0,
# #                 Treatments.dilgw, Substances.pfos, "small_low_data",
# #                 "x entered as range between 0.2 and 0.25"),
# #         Mixture(0.925, 0.0127551020408163, 0, 0,
# #                 Treatments.dilsw, Substances.pfos, "large_low_data",
# #                 "x entered as range between 0.9 and 0.95"),
# #         Mixture(0.225, 0.0127551020408163, 0, 0,
# #                 Treatments.dilgw, Substances.pfos, "large_low_data",
# #                 "x entered as range between 0.2 and 0.25"),
# #         Mixture(0.925, 0.0127551020408163, 20, 2,
# #                 Treatments.dilsw, Substances.pfos, "large_high_data",
# #                 "x entered as range between 0.9 and 0.95"),
# #         Mixture(0.225, 0.0127551020408163, 0, 0,
# #                 Treatments.dilgw, Substances.pfos, "large_high_data",
# #                 "x entered as range between 0.2 and 0.25")
# #     ],
# #     removal_percents=[
# #         RemovalPercent(np.array([75, 80, 85]), Treatments.dwac, Substances.pfos)
# #     ],
# #     references=[
# #         Reference("TrinkwV 2023 + DOI 10.21945/RIVM-2018-0070", Substances.pfos, Matrices.drw, 2.5,
# #                   2023,
# #                   "Use of relative potency factors: (20 / 4 / RPF = 2)")
# #     ],
# #     starting_concentration=[
# #         # Point value for simple interpretation
# #         StartingConcentration(np.array([100.]), Substances.pfos, Matrices.rww)
# #     ]
# # )
# #
# # water_reuse = CaseStudy(
# #     name="Water Reuse",
# #     mixtures=[
# #         Mixture(0.2, 0.0510204081632653, 0, 0,
# #                 Treatments.dilrw, Substances.pfos, "standard",
# #                 "x entered as range between o and 0.3"),
# #         Mixture(0.21, 0.015306122448979591, 0, 0,
# #                 Treatments.sepev, Substances.pfos, "standard",
# #                 "x entered as range between o and 0.24"),
# #     ],
# #     removal_percents=[],
# #     references=[
# #         Reference("Based on TWI 44 ng/kg bw (EFSA)", Substances.pfos, Matrices.pow, 0.39,
# #                   2020, "")
# #     ],
# #     starting_concentration=[]
# # )
