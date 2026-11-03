import dataclasses as dtc
import numpy as np

from ewex.models.impact_scenario import ImpactScenario, ImpactMixtureScenario


@dtc.dataclass
class AssessmentResult:
    impact_scenario: ImpactScenario
    assessment: np.ndarray | list[np.ndarray]

    def summarize(self):
        sim_res = self.impact_scenario.exposure_result
        tids = sim_res.exposure_scenario.treatment_train.show_treatment_ids()
        ap = self.impact_scenario.assessment_point
        ap_i = tids.index(ap)
        step = sim_res.exposure_scenario.treatment_train[ap_i]

        return dict(
            Scenario_name = self.impact_scenario.name,
            Treatment_train = tids[:(ap_i+1)],
            Assessment_point =  "after " + step.name,
            Water_matrix = step.get_output_matrix(input_matrix=step.input_matrix),
            Hazard = sim_res.exposure_scenario.substance.name,
            RQ_50 = np.round(np.percentile(self.assessment,50), 3),
            RQ_75 = np.round(np.percentile(self.assessment,75), 3),
            RQ_95 = np.round(np.percentile(self.assessment, 95), 3),
            RQ_99 = np.round(np.percentile(self.assessment, 99), 3),
            RQ_mean = np.round(np.mean(self.assessment), 3)
        )


def asses_exposure(
    impact_scenario: ImpactScenario
) -> AssessmentResult:

    sim_res = impact_scenario.exposure_result
    if impact_scenario.name is None:
        impact_scenario.name = impact_scenario.exposure_result.exposure_scenario.name
    sub = sim_res.exposure_scenario.substance
    output_array = impact_scenario.output_concentration()
    rq = output_array / sub.reference.ref_value
    return AssessmentResult(
        impact_scenario,
        rq
    )

@dtc.dataclass
class MixtureAssessmentResult:
    impact_mixture_scenario: ImpactMixtureScenario
    assessment: np.ndarray
    single_assessments: list[np.ndarray] | None = None

    def summarize(self):
        sim_res = self.impact_mixture_scenario.exposure_results
        tids = sim_res[0].exposure_scenario.treatment_train.show_treatment_ids()
        ap = self.impact_mixture_scenario.assessment_point
        ap_i = tids.index(ap)
        step = sim_res[0].exposure_scenario.treatment_train[ap_i]
        h_group = self.impact_mixture_scenario.hazard_group.name

        subs_included = []
        for i in range(0, len(sim_res)):
            subs_included += [sim_res[i].exposure_scenario.substance.id]
        if self.impact_mixture_scenario.hazard_group.use_equivalence:
            group_reference = self.impact_mixture_scenario.hazard_group.reference
        else:
            group_reference = None

        return dict(
            Scenario_name = self.impact_scenario.name,
            Group_reference = group_reference,
            Treatment_train = tids[:(ap_i+1)],
            Assessment_point =  "after " + step.name,
            Water_matrix = step.get_output_matrix(input_matrix=step.input_matrix),
            Hazard = h_group,
            Substances_included=subs_included,
            RQ_50 = np.round(np.percentile(self.assessment,50), 3),
            RQ_75 = np.round(np.percentile(self.assessment,75), 3),
            RQ_95 = np.round(np.percentile(self.assessment, 95), 3),
            RQ_99 = np.round(np.percentile(self.assessment, 99), 3),
            RQ_mean = np.round(np.mean(self.assessment), 3),
            RQ_sd = np.round(np.sdt(self.assessment), 3)
        )


def asses_mixture_exposure(
    impact_mixture_scenario: ImpactMixtureScenario,
    random_combination: bool = True
) -> MixtureAssessmentResult:
    ap = impact_mixture_scenario.assessment_point
    # filter exposure results for hazard group substances
    single_exposures = impact_mixture_scenario.hazard_group_substances()
    eq = impact_mixture_scenario.hazard_group.use_equivalence

    if impact_mixture_scenario.name is None:
        single_names = [r.exposure_scenario.name for r in impact_mixture_scenario.exposure_results]
        suffix = longest_common_substring(single_names)
        impact_mixture_scenario.name = impact_mixture_scenario.hazard_group.name + suffix

    substance_list_results = []
    substance_output = []
    for i, expo in enumerate(single_exposures):
        assessment_scenario = ImpactScenario(
            exposure_result = expo,
            assessment_point = ap
        )
        output_array = assessment_scenario.output_concentration()
        if eq:
            # All exposure concentrations are multiplied by equivalence factors
            substance_result = AssessmentResult(
                assessment_scenario,
                output_array * assessment_scenario.exposure_result.exposure_scenario.substance.equivalence_factor.equivalent_value
            )
        else:
            # A RQ is calculated for each substance
            substance_result = asses_exposure(assessment_scenario)

        substance_array = substance_result.assessment
        if random_combination:
            np.random.shuffle(substance_array)
        else:
            substance_array = np.sort(substance_array)[::-1]

        substance_list_results += [substance_result]
        substance_output += [substance_array]

    if eq:
        whole_group_ref = impact_mixture_scenario.hazard_group.reference.ref_value
        rq = np.sum(substance_output, axis=0) / whole_group_ref
        # substance_output / len(single_exposures) / whole_group_ref
    else:
        rq = np.sum(substance_output, axis=0)


    single_impact_scenario = ImpactMixtureScenario(
        exposure_results = single_exposures,
        hazard_group = impact_mixture_scenario.hazard_group,
        name = impact_mixture_scenario.name,
        assessment_point = impact_mixture_scenario.assessment_point
    )

    return MixtureAssessmentResult(
        impact_mixture_scenario = single_impact_scenario,
        assessment = rq,
        single_assessments = substance_output # either a reference quotient or a weighted concentration
    )

# utils
def longest_common_substring(strings: list[str]):
    shortest = min(strings, key=len)

    for length in range(len(shortest), 0, -1):
        for i in range(len(shortest) - length + 1):
            substring = shortest[i:i + length]

            if all(substring in s for s in strings):
                return substring

    return ""