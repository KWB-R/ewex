from unittest import TestCase

import numpy as np
from assertpy import assert_that

from promisces import Mixture, RemovalPercent
from promisces.models.treatment import Treatments


class TestTreatments(TestCase):

    def test_that_clone_keeps_previously_set_attributes(self):
        given_treatment = Treatments.dilww

        got_clone = given_treatment.clone()

        assert_that(got_clone.id).is_equal_to(given_treatment.id)
        assert_that(got_clone.group).is_equal_to(given_treatment.group)
        assert_that(got_clone.name).is_equal_to(given_treatment.name)
        assert_that(got_clone.input_matrix).is_equal_to(given_treatment.input_matrix)
        assert_that(got_clone.output_matrix).is_equal_to(given_treatment.output_matrix)
        assert_that(got_clone.with_lit_data).is_equal_to(given_treatment.with_lit_data)
        assert_that(got_clone.mixture).is_equal_to(given_treatment.mixture)

    def test_that_clone_overwrites_passed_attributes(self):
        given_treatment = Treatments.dilww.with_mixture(Mixture(1, 2, 3, 4))
        given_id = "dilww2"
        given_name = "My new clone tes"
        given_mixture = Mixture(5, 6, 7, 8)
        got_clone = given_treatment.clone(id=given_id, name=given_name, mixture=given_mixture)

        assert_that(got_clone.id).is_equal_to(given_id)
        assert_that(got_clone.group).is_equal_to(given_treatment.group)
        assert_that(got_clone.name).is_equal_to(given_name)
        assert_that(got_clone.input_matrix).is_equal_to(given_treatment.input_matrix)
        assert_that(got_clone.output_matrix).is_equal_to(given_treatment.output_matrix)
        assert_that(got_clone.with_lit_data).is_equal_to(given_treatment.with_lit_data)
        assert_that(got_clone.mixture).is_equal_to(given_mixture)

    def test_that_a_removal_can_be_added(self):
        given_removal = RemovalPercent(np.array([1, 2, 3]))
        given_treatment = Treatments.wwt1.with_removal(given_removal)

        assert_that(given_treatment.removal == given_removal).is_true()
        assert_that(given_treatment.removal.treatment).is_equal_to(given_treatment)

    def test_that_a_mixture_can_be_added(self):
        given_mixture = Mixture(1, 2, 3, 4)
        given_treatment = Treatments.dilww.with_mixture(given_mixture)

        assert_that(given_treatment.mixture).is_equal_to(given_mixture)
        assert_that(given_treatment.mixture.treatment).is_equal_to(given_treatment)
