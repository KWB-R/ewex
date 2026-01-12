from __future__ import annotations
import dataclasses as dtc
import statistics

from scipy.stats import truncnorm, lognorm


@dtc.dataclass
class Mixture:
    x2_mean: float
    x2_sd: float
    c2_mean: float
    c2_sd: float
    log_dist: bool = False
    comments: str = ""

    @staticmethod
    def from_minmax(
            x2_min: float,
            x2_max: float,
            c2_min: float,
            c2_max: float,
    ) -> "Mixture":
        x2_mean = statistics.mean(data=[x2_min, x2_max])
        x2_sd = (x2_max - x2_min) / (2 * 1.96)  # min and max value correspond to 95% interval of normal distribution

        c2_mean = statistics.mean(data=[c2_min, c2_max])
        c2_sd = (c2_max - c2_min) / (2 * 1.96)  # min and max value correspond to 95% interval of normal distribution
        return Mixture(x2_mean, x2_sd, c2_mean, c2_sd, False,
                       f"x entered as range between {x2_min} and {x2_max}; "
                       f"c entered as range between {c2_min} and {c2_max}")

    def asdict(self):
        return dict(
            x2_mean=self.x2_mean,
            x2_sd=self.x2_sd,
            c2_mean=self.c2_mean,
            c2_sd=self.c2_sd,
            log_dist=self.log_dist
        )
