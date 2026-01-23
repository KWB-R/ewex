from unittest import TestCase

import numpy as np
from assertpy import assert_that

from ewex import Scenario
from ewex.models.mixture import Mixture
from ewex.models.removal_percent import RemovalPercent
from ewex.models.starting_concentration import StartingConcentration
from ewex.models.treatment import Treatments, TreatmentTrain
from ewex.models.matrix import Matrices
from ewex.models.substance import Substances, Substance
from ewex.removal_processes import ProcessType, DominantDistribution
from ewex.simulate_removal import simulate_removal, SimulationResult
from ewex.plots import er_profiles, spider_plot


class TestSimulateRemoval(TestCase):

    def test_should_go_through_without_errors(self):
        treatment_train: TreatmentTrain = TreatmentTrain([
            Treatments.wwt1,
            Treatments.wwmb,
            Treatments.wwuf,
            Treatments.wwro,
        ])
        substance: Substance = Substances.pfoa
        input_matrix = Matrices.rww
        scenario = Scenario("test scenario", input_matrix, substance, treatment_train)

        result = simulate_removal(scenario)

        assert_that(result).is_instance_of(SimulationResult)
        er_profiles([result])
        spider_plot([result])
        # TODO: more assertions!

    def test_should_validate_input_matrix(self):
        treatment_train: TreatmentTrain = TreatmentTrain([
            Treatments.gruc
        ])
        substance: Substance = Substances.pfoa
        # wrong input matrix for the treatment
        input_matrix = Matrices.rww

        assert_that(Scenario).raises(ValueError).when_called_with(
            "test scenario", input_matrix, substance, treatment_train
        )

    def test_should_raise_on_missing_starting_concentration(self):
        treatment_train: TreatmentTrain = TreatmentTrain([
            Treatments.gruc
        ])
        substance: Substance = Substances.pfoa

        # no lit data for this input
        input_matrix = Matrices.grw
        scenario = Scenario("test scenario", input_matrix, substance, treatment_train)

        assert_that(simulate_removal).raises(ValueError).when_called_with(
            scenario
        )

    def test_should_require_mixture_data(self):
        treatment_train: TreatmentTrain = TreatmentTrain([
            Treatments.wwt1,
            Treatments.dilww,  # requires mixture
        ])
        substance: Substance = Substances.pfoa
        input_matrix = Matrices.rww
        scenario = Scenario("test scenario", input_matrix, substance, treatment_train)

        assert_that(simulate_removal).raises(ValueError).when_called_with(
            scenario
        )

    def test_should_use_cs_mixture_data(self):
        # TODO
        substance = Substances.pfoa
        input_matrix = Matrices.rww
        treatment_train: TreatmentTrain = TreatmentTrain([
            Treatments.wwt1,
            Treatments.dilww.with_mixture(Mixture(1, 1, 1, 1)),
        ])
        scenario = Scenario("test scenario", input_matrix, substance, treatment_train)
        result = simulate_removal(scenario)

        assert_that(result).is_instance_of(SimulationResult)

        rmv_type_1 = result.intermediate_results[1].process_type
        assert_that(rmv_type_1).is_equal_to(ProcessType.mixture)

    def test_should_use_cs_starting_concentration(self):
        treatment_train: TreatmentTrain = TreatmentTrain([
            Treatments.wwt1,
            Treatments.wwtt,
        ])
        substance: Substance = Substances.pfoa
        input_matrix = Matrices.rww
        start_c = StartingConcentration(
            np.array([100]),  # we expect all the start_c samples == 100
        )
        scenario = Scenario("test scenario", input_matrix, substance, treatment_train, start_c)

        result = simulate_removal(scenario)

        assert_that(result).is_instance_of(SimulationResult)

        assert_that(np.all(result.starting_concentration == 100))

    def test_should_use_cs_removal(self):
        treatment_train: TreatmentTrain = TreatmentTrain([
            Treatments.wwt1.with_removal(
                RemovalPercent(np.array([100, 100, 100]))
            ),
        ])
        substance: Substance = Substances.pfoa
        input_matrix = Matrices.rww
        start_c = StartingConcentration(
            np.array([100]),  # we expect all the start_c samples == 100
        )
        scenario = Scenario("test scenario", input_matrix, substance, treatment_train, start_c)
        result = simulate_removal(scenario)

        assert_that(result).is_instance_of(SimulationResult)

        assert_that(np.all(result.intermediate_results[-1].output_concentration == 0))

    def test_that_treatment_can_be_without_lit_data(self):
        treatment_train: TreatmentTrain = TreatmentTrain([
            Treatments.wwt1.with_removal(
                # we expect 0 in the output_c
                RemovalPercent(np.array([100, 100, 100]))).without_lit_data(),
        ])
        substance: Substance = Substances.pfoa
        input_matrix = Matrices.rww
        start_c = StartingConcentration(
            np.array([100]),  # we expect all the start_c samples == 100
        )
        scenario = Scenario("test scenario", input_matrix, substance, treatment_train, start_c)

        result = simulate_removal(scenario)

        assert_that(result).is_instance_of(SimulationResult)

        assert_that(np.all(result.intermediate_results[-1].output_concentration == 0))

        assert_that(result.intermediate_results[0].dominant_distribution).is_equal_to(DominantDistribution.case_study)