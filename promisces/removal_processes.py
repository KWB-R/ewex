import dataclasses as dtc
from asyncio.windows_events import INFINITE
from enum import Enum
from numpy.random import choice

import numpy as np
from scipy.stats import norm, beta, truncnorm, lognorm

from promisces.models.removal_percent import RemovalPercent


class ProcessType(Enum):
    generic = "Generic Process"
    mixture = "Mixture Process"
    separation = "Separation Process"
    separation_sludge = "Separation Sludge"


class DominantDistribution(Enum):
    prior = "Prior"
    literature = "Literature"
    case_study = "Case Study"
    combination = "Combination"


@dtc.dataclass
class ProcessResult:
    process_type: ProcessType
    output_concentration: np.ndarray
    rmv_factors: np.ndarray
    dominant_distribution: DominantDistribution
    average_out: bool


def to_likelihood(rmv_values: RemovalPercent, rmv_factor_resolution=1000):
    rmv_factor = np.arange(1, rmv_factor_resolution) / rmv_factor_resolution
    if len(rmv_values) > 0:
        conservative_starting = np.r_[0.001, rmv_values / 100]
        conservative_starting_mean = conservative_starting.mean()
        data = np.r_[conservative_starting_mean, rmv_values / 100]
        likelihood = norm.pdf(x=rmv_factor, loc=data.mean(),
                              # !important! ddof=1 ==> sample std (vs population std)
                              scale=np.std(data, ddof=1))
        # print(f"mean: {data.mean()}, std: {np.std(data, ddof=1)}")
        likelihood = likelihood / sum(likelihood)
    else:
        likelihood = np.repeat(a=1, repeats=rmv_factor_resolution-1)
    return rmv_factor*100, likelihood


def prior_beta(power=100, rmv_factor_resolution=1000):
    x_range = np.arange(1, rmv_factor_resolution) / rmv_factor_resolution
    prior_beta_fit = beta.fit(
        data=(0 + 1 / power, 1 - 1 / power),
        floc=0,  # minimum (fixed)
        fscale=1  # maximum (fixed)
    )
    # print(f"prior beta: a, b = {prior_beta_fit}")
    prior = beta.pdf(
        x=x_range,
        a=prior_beta_fit[0],
        b=prior_beta_fit[1])
    return prior / sum(prior)


def apply_generic_process(
        input_c: np.ndarray,
        lit_rmv: RemovalPercent,
        cs_rmv: RemovalPercent,
        rmv_factor_resolution: int | float,
        power: int | float = 100,
        n_runs: int = 10000
) -> ProcessResult:
    """
    calculates the substance concentration after a process defined only by a removal factor.
    the removal factor has to be in %
    """
    # print(lit_rmv.arr)
    # print(cs_rmv.arr)
    # print("---------------------------")
    lit_rmv = np.where(lit_rmv < 0, 0, lit_rmv)
    lit_rmv_factor, lit_lkl = to_likelihood(rmv_values=lit_rmv,
                                            rmv_factor_resolution=rmv_factor_resolution)
    cs_rmv_factor, cs_lkl = to_likelihood(rmv_values=cs_rmv,
                                          rmv_factor_resolution=rmv_factor_resolution)

    # print(lit_lkl)
    # print(cs_lkl)
    prior_probs = prior_beta(power=power, rmv_factor_resolution=rmv_factor_resolution)
    probs_both = lit_lkl * cs_lkl
    posterior = probs_both * prior_probs
    posterior /= sum(posterior)

    posterior_max: object = cs_rmv_factor[posterior.argmax()]
    max_cs_prob = (cs_lkl == cs_lkl.max()).nonzero()[0]
    cs_max = cs_rmv_factor[cs_lkl.argmax()] if len(max_cs_prob) == 1 else 1000 # needs to be outside removal factor range
    max_lit_prob = (lit_lkl == lit_lkl.max()).nonzero()[0]
    lit_max = lit_rmv_factor[lit_lkl.argmax()] if len(max_lit_prob) == 1 else 1000

    if abs(cs_max - posterior_max) < 0.05 * 100:
        dominant_distribution = DominantDistribution.case_study
    elif abs(lit_max - posterior_max) < 0.05 * 100:
        dominant_distribution = DominantDistribution.literature
    elif (posterior_max <= (0 + 1 / rmv_factor_resolution * 100)) | (
            posterior_max >= (1 - 1 / rmv_factor_resolution * 100)):
        dominant_distribution = DominantDistribution.prior
    else:
        dominant_distribution = DominantDistribution.combination

    # Draw removal factors from distributions
    rmv_factor = choice(
        a=lit_rmv_factor,  # should be equal to cs_rmv_factor
        size=n_runs,
        replace=True,
        p=posterior  # posterior equal prior if no data is available
    )
    # import matplotlib.pyplot as plt
    # #
    # plt.figure()
    # plt.plot(prior_probs, label="prior", alpha=.5, linestyle="--")
    # plt.plot(lit_lkl, label="lit")
    # plt.plot(posterior, label="posterior", alpha=.75)
    # plt.legend()
    # plt.show()
    # if CS distribution is dominant, the average of the posterior distribution can be expected to be
    # the real site-specific average. --> no sorting of removal factors
    if not dominant_distribution == DominantDistribution.case_study:
        rmv_factor = np.sort(rmv_factor)
        av_out = False
    else:
        av_out = True

    # TODO: CHECK SORTING
    input_c = np.sort(input_c)[::-1]
    output_c = input_c * (1 - rmv_factor / 100)

    return ProcessResult(
        ProcessType.generic,
        # TODO: CHECK SORTING
        np.sort(output_c)[::-1], # not needed for calculations
        rmv_factor,
        dominant_distribution,
        av_out
    )


def apply_mixture_process(input_c, x2_mean, x2_sd, c2_mean, c2_sd, distribution) -> ProcessResult:
    """
    calculates the substance concentration after a mixture process of the main stream into a diluting liquid.
    """
    n_runs = input_c.size

    if x2_sd == 0:
        x2_dist = np.array([x2_mean] * n_runs)
    else:
        x2_dist = distribution.rvs(
            a=(0 - x2_mean) / x2_sd,
            b=(1 - x2_mean) / x2_sd,
            loc=x2_mean,
            scale=x2_sd,
            size=n_runs
        )

    if c2_sd == 0:
        c2_dist = np.array([c2_mean] * n_runs)
    else:
        c2_dist = distribution.rvs(
            a=(0 - c2_mean) / c2_sd,
            b=100,  # the upper limit of distribution is 100 * sd of the normal distribution
            loc=c2_mean,
            scale=c2_sd,
            size=n_runs
        )

    output_c = input_c * (1 - x2_dist) + c2_dist * x2_dist
    rmv_factor = (1 - output_c / input_c) * 100
    return ProcessResult(
        ProcessType.mixture,
        np.sort(output_c)[::-1],
        rmv_factor,
        DominantDistribution.case_study,
        average_out=True
    )


# case study specific data of separation processes are saved and loaded with "mixture" functions
def apply_separation_process(input_c, x2_mean, x2_sd, c2_mean, c2_sd, distribution) -> ProcessResult:
    """
    calculates the substance concentration after a mixture process of the main stream into a diluting liquid.
    """
    n_runs = input_c.size

    if x2_sd == 0:
        x2_dist = np.array([x2_mean] * n_runs)
    else:
        x2_dist = distribution.rvs(
            a=(0 - x2_mean) / x2_sd,
            b=(1 - x2_mean) / x2_sd,
            loc=x2_mean,
            scale=x2_sd,
            size=n_runs
        )

    if c2_sd == 0:
        c2_dist = np.array([c2_mean] * n_runs)
    else:
        c2_dist = distribution.rvs(
            a=(0 - c2_mean) / c2_sd,  # lower limit is 0
            b=(input_c - c2_mean) / c2_sd,  # the upper limit is the concentration of the inlet
            loc=c2_mean,
            scale=c2_sd,
            size=n_runs
        )

    output_c = (input_c - c2_dist * x2_dist) / (1 - x2_dist)
    rmv_factor = (1 - output_c / input_c) * 100
    return ProcessResult(
        ProcessType.mixture,
        np.sort(output_c)[::-1],
        rmv_factor,
        DominantDistribution.case_study,
        average_out=True
    )


def apply_separation_sludge_process(
        input_c: np.ndarray,
        lit_rmv: RemovalPercent,
        cs_rmv: RemovalPercent,
        rmv_factor_resolution: int | float,
        prior_power: int | float = 100,
        x_eff_mean=0.9,
        x_eff_sd=0.02
) -> ProcessResult:
    """
    calculates the substance concentration in sludge after dewatering
    """
    # separation_sludge
    n_runs = input_c.size

    x_eff_dist = np.sort(truncnorm.rvs(
        a=(0 - x_eff_mean) / x_eff_sd,
        b=(1 - x_eff_mean) / x_eff_sd,
        loc=x_eff_mean,
        scale=x_eff_sd,
        size=n_runs
    ))

    # concentration of effluent can be estimated by the process wwtt
    # update prior distribution by literature and case study data
    result = apply_generic_process(
        input_c,
        lit_rmv,  # TODO: in this case we might need an other t.id ("wwtt")?
        cs_rmv,
        rmv_factor_resolution,
        power=prior_power, n_runs=n_runs
    )
    c_eff_dist = result.output_concentration
    output_c = (input_c - c_eff_dist * x_eff_dist) / (1 - x_eff_dist)
    rmv_factor = (1 - output_c / input_c) * 100
    return ProcessResult(
        ProcessType.separation_sludge,
        np.sort(output_c)[::-1],
        rmv_factor,
        result.dominant_distribution,
        result.average_out
    )
