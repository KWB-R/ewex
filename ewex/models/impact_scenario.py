import dataclasses as dtc

from ewex.simulate_removal import SimulationResult
from ewex.models.treatment import Treatment
from ewex.models.substance import HazardGroup

@dtc.dataclass
class ImpactMixtureScenario:
    exposure_results: list[SimulationResult]
    hazard_group: HazardGroup
    name: str | None = None
    assessment_point: str | None = None
    include_single_substances: bool = True

    def with_assessment_point(self, tt_point: Treatment):
        """
         Set the point of assessment within the treatment train.
         Args:
             tt_point (Treatment Model): The Treatment after which the
             water is compared to the reference value
         Returns:
             ImpactAssessment including the treatment ID of the assessment point in tids.

         """
        self.assessment_point = tt_point.id
        return self

    def simulated_substances(self):
        subs = []
        for i, expo in enumerate(self.exposure_results):
                subs += [self.exposure_results[i].exposure_scenario.substance]
        return subs

    def hazard_group_substances(self):
        hg = self.hazard_group
        expo_results = []
        for i, expo in enumerate(self.exposure_results):
            if self.exposure_results[i].exposure_scenario.substance.hazard_group == hg:
                expo_results += [self.exposure_results[i]]
        return expo_results

@dtc.dataclass
class ImpactScenario:
    exposure_result: SimulationResult
    name: str | None = None
    assessment_point: str | None = None

    def with_assessment_point(self, tt_point: Treatment):
        """
         Set the point of assessment within the treatment train.
         Args:
             tt_point (Treatment Model): The Treatment after which the
             water is compared to the reference value
         Returns:
             ImpactAssessment including the treatment ID of the assessment point in tids.

         """
        self.assessment_point = tt_point.id
        return self

    def output_concentration(self):
        ap = self.assessment_point
        sim_res = self.exposure_result

        if self.name is None:
            self.name = sim_res.exposure_scenario.name

        tids = sim_res.exposure_scenario.treatment_train.show_treatment_ids()
        if ap is None:
            ap_i = len(tids) - 1
        else:
            ap_i = tids.index(ap)

        self.assessment_point = tids[ap_i]
        return sim_res.intermediate_results[ap_i].output_concentration
