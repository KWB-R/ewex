import math
from math import pi
import warnings

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt, patches as mpatches
import seaborn as sns
from matplotlib.ticker import FixedLocator

from ewex.simulate_removal import SimulationResult
from ewex.asses_impact import MixtureAssessmentResult, AssessmentResult


def concentration_profile(
        sim_result: SimulationResult,
        title: str | None = None,
        save_as: str | None = None,
        c_scale: str | None = None,
        color: str = '#DC540C',
        unit: str = "ng/L",
        font_size: int = 12,
        reference_value: float | None = None
):
    substance_name = sim_result.exposure_scenario.substance.name
    if title is None:
        title = sim_result.exposure_scenario.name

    output_c_df = pd.melt(sim_result.output_c_df)

    if reference_value is not None and c_scale is None:
        max_c = output_c_df.max(numeric_only=True).max()
        if (max_c / reference_value) > 100:
            c_scale = "log"
        else:
            c_scale = "linear"

    if c_scale is None:
        c_scale = "linear"

    plt.figure(
        figsize=(1.2 * len(sim_result.exposure_scenario.treatment_train),
                 len(sim_result.exposure_scenario.treatment_train)))

    ax = sns.violinplot(
        x="variable",
        y="value",
        data=output_c_df,
        color=color,
        cut=0,
        density_norm="width",
        inner=None,
        saturation=1
    )


    plt.xticks(fontsize=font_size, rotation=0)
    plt.yticks(fontsize=font_size, rotation=0)

    ax.set_title(title, fontsize = font_size + 2)
    ax.set_ylabel(substance_name + " (" + unit + ")", fontsize=font_size)
    if reference_value is not None:
        ax.axhline(y=reference_value, color='black', linestyle='--')
        ax.annotate(
            "Reference value",
            xy=(0.02, reference_value),
            xycoords=ax.get_yaxis_transform(),
            xytext=(0, 4),
            textcoords="offset points",
            ha="left",
            va="bottom",
            fontsize=font_size
        )
    ax.set_xlabel('Treatment step outlet', fontsize=font_size)
    ax.set_yscale(c_scale)

    if save_as is not None:
        plt.savefig(save_as, dpi=300, bbox_inches = "tight")
        plt.close()



def removal_profile(
    sim_results: list[SimulationResult],
    no_mixture: bool = True,
    long_substance_name: bool = True,
    save_as: str | None = None,
    color_palette: str | list = "viridis",
    font_size: int = 12
):
    if isinstance(sim_results, SimulationResult):
        sim_results = [sim_results]
        
    rmv_factor_df = pd.concat([r.rmv_factor_df.assign(
        scenario=r.exposure_scenario.name,
        sub_name=r.exposure_scenario.substance.name,
        sub_id=r.exposure_scenario.substance.id) for r in sim_results])
    if no_mixture:
        mixture_columns = [rmv_factor_df.columns.get_loc(col) for col in rmv_factor_df.columns if "dil" in col]
        rmv_factor_df = rmv_factor_df.drop(rmv_factor_df.columns[mixture_columns], axis=1)

    rmv_factor_df = pd.melt(rmv_factor_df, id_vars=["scenario", "sub_name", "sub_id"])

    n1 = rmv_factor_df["scenario"].nunique()
    n2 = rmv_factor_df["sub_name"].nunique()
    n3 = rmv_factor_df["sub_id"].nunique()
    if not (n1 == n2 == n3):
        color_factor = "scenario"
    elif long_substance_name:
        color_factor = "sub_name"
    else:
        color_factor = "sub_id"

    plt.figure(
        figsize=(8, 1.2 * len(sim_results) + 2))

    axs = sns.violinplot(
        x="value", y="variable",
        data=rmv_factor_df,
        hue=color_factor,
        cut=0,
        density_norm="width",
        inner=None,
        saturation=1,
        palette=color_palette,
        orient="h",
        legend="brief" if len(sim_results) > 1 else False
    )

    if len(sim_results) > 1:
        sns.move_legend(
            axs,
            "lower left",
            bbox_to_anchor=(0, 1.02, 1, 0.2),
            mode="expand",
            borderaxespad=0,
            ncol=3,
            title=None,
            fontsize=font_size,
            title_fontsize=font_size,
            frameon=True,
            fancybox=False,
            framealpha=1,
            facecolor="white",
            edgecolor="black",
            borderpad=0.5
        )

    if no_mixture:
        xstr = 'Removal factor in %'
    else:
        xstr = 'Reduction of concentration (removal or dilution) in %'

    axs.set_xlabel(xstr, fontsize=font_size)
    axs.set_ylabel('', fontsize=font_size)
    plt.xticks(fontsize=font_size, rotation=0)
    plt.yticks(fontsize=font_size, rotation=0)

    left, right = plt.xlim()
    if left < -1000:
        axs[1].set_xlim(-1000, 150)
    if save_as is not None:
        plt.savefig(save_as, dpi=300, bbox_inches = "tight")
        plt.close()


def spider_plot(
        assessment_results: list[MixtureAssessmentResult|AssessmentResult],
        case_study_name: str | None = None,
        draw_legend: bool = True,
        save_as: str | None = None
):
    rq = []
    sc_name = []
    sub_name = []
    for i, impact in enumerate(assessment_results):
        if isinstance(impact, MixtureAssessmentResult):
            rq += [impact.assessment]
            sc_name += [impact.impact_mixture_scenario.name]
            sub_name += [impact.impact_mixture_scenario.hazard_group.name]
        else:
            rq += [impact.assessment]
            sc_name += [impact.impact_scenario.name]
            sub_name += [impact.impact_scenario.exposure_result.exposure_scenario.substance.id]

    if case_study_name is not None and len(set(sub_name)) == len(set(sc_name)):
        column_names = sub_name
        title = case_study_name
    else:
        column_names = sc_name
        title = ""

    output_c_df = pd.DataFrame(
        np.column_stack(rq),
        columns = column_names
    )

    percentiles = [0.50, 0.75, 0.95, 0.99]
    stats = output_c_df.describe(percentiles)
    categories = stats.columns
    n_cat = len(categories)
    angles = np.linspace(0, 2 * pi, n_cat, endpoint=False)
    fig = plt.figure(figsize=(8, 9))
    ax = plt.subplot(111, polar=True)
    fig.patch.set_facecolor("white")
    ax.set_facecolor('white')
    ax.grid(False)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles)
    ax.set_xticklabels(categories, fontweight='bold', fontsize=12)
    ax.xaxis.set_minor_locator(FixedLocator(angles))

    x_ticks = ax.xaxis.get_major_ticks()
    for tick in x_ticks:
        tick.set_pad(15)
    y_max = math.ceil(stats.loc['50%'].max())
    ax.set_ylim(0, y_max)
    y4 = y_max / 2
    y3 = y_max / 4
    y2 = y_max / 8
    ax.set_rlabel_position(0)

    yticks = [0, y2, y3, y4, y_max]
    ax.set_yticks(yticks)
    cat = ['50th', '75th', '95th', '99th', '']
    ax.set_yticklabels(cat[::-1], fontsize=12)

    intervals = [0.1, 1, 5, 10]
    colors = ['#2ED812', '#AEFF00', '#F4EF34', '#FC8604', '#FF4A37']
    bar_width = 2 * np.pi / n_cat

    # 99percentile 
    start_y = yticks[0]
    end_y = yticks[1]
    for j, column in enumerate(stats.columns):
        value_at_99_percentile = stats.loc['99%', column]
        if value_at_99_percentile < intervals[0]:
            ax.bar(angles[j], end_y, width=bar_width, bottom=start_y, facecolor=colors[0], alpha=1,
                   edgecolor='k')
        elif intervals[0] <= value_at_99_percentile < intervals[1]:
            ax.bar(angles[j], end_y, width=bar_width, bottom=start_y, facecolor=colors[1], alpha=1,
                   edgecolor='k')
        elif intervals[1] <= value_at_99_percentile < intervals[2]:
            ax.bar(angles[j], end_y, width=bar_width, bottom=start_y, facecolor=colors[2], alpha=1,
                   edgecolor='k')
        elif intervals[2] <= value_at_99_percentile < intervals[3]:
            ax.bar(angles[j], end_y, width=bar_width, bottom=start_y, facecolor=colors[3], alpha=1,
                   edgecolor='k')
        elif value_at_99_percentile >= intervals[3]:
            ax.bar(angles[j], end_y, width=bar_width, bottom=start_y, facecolor=colors[4], alpha=1,
                   edgecolor='k')

    # 95percentile 
    start_y_95 = yticks[1]
    end_y_95 = yticks[2]
    for j, column in enumerate(stats.columns):
        value_at_95_percentile = stats.loc['95%', column]
        if value_at_95_percentile < intervals[0]:
            ax.bar(angles[j], end_y_95, width=bar_width, bottom=start_y_95, facecolor=colors[0], alpha=1,
                   edgecolor='k')
        elif intervals[0] <= value_at_95_percentile < intervals[1]:
            ax.bar(angles[j], end_y_95, width=bar_width, bottom=start_y_95, facecolor=colors[1], alpha=1,
                   edgecolor='k')
        elif intervals[1] <= value_at_95_percentile < intervals[2]:
            ax.bar(angles[j], end_y_95, width=bar_width, bottom=start_y_95, facecolor=colors[2], alpha=1,
                   edgecolor='k')
        elif intervals[2] <= value_at_95_percentile < intervals[3]:
            ax.bar(angles[j], end_y_95, width=bar_width, bottom=start_y_95, facecolor=colors[3], alpha=1,
                   edgecolor='k')
        elif value_at_95_percentile >= intervals[3]:
            ax.bar(angles[j], end_y_95, width=bar_width, bottom=start_y_95, facecolor=colors[4], alpha=1,
                   edgecolor='k')

            # 75percentile 
    start_y_75 = yticks[2]
    end_y_75 = yticks[3]
    for j, column in enumerate(stats.columns):
        value_at_75_percentile = stats.loc['75%', column]
        if value_at_75_percentile < intervals[0]:
            ax.bar(angles[j], end_y_75, width=bar_width, bottom=start_y_75, facecolor=colors[0], alpha=1,
                   edgecolor='k')
        elif intervals[0] <= value_at_75_percentile < intervals[1]:
            ax.bar(angles[j], end_y_75, width=bar_width, bottom=start_y_75, facecolor=colors[1], alpha=1,
                   edgecolor='k')
        elif intervals[1] <= value_at_75_percentile < intervals[2]:
            ax.bar(angles[j], end_y_75, width=bar_width, bottom=start_y_75, facecolor=colors[2], alpha=1,
                   edgecolor='k')
        elif intervals[2] <= value_at_75_percentile < intervals[3]:
            ax.bar(angles[j], end_y_75, width=bar_width, bottom=start_y_75, facecolor=colors[3], alpha=1,
                   edgecolor='k')
        elif value_at_75_percentile >= intervals[3]:
            ax.bar(angles[j], end_y_75, width=bar_width, bottom=start_y_75, facecolor=colors[4], alpha=1,
                   edgecolor='k')

            # 50percentile 
    start_y_50 = yticks[3]
    end_y_50 = yticks[4]
    for j, column in enumerate(stats.columns):
        value_at_50_percentile = stats.loc['50%', column]
        if value_at_50_percentile < intervals[0]:
            ax.bar(angles[j], end_y_50, width=bar_width, bottom=start_y_50, facecolor=colors[0], alpha=1,
                   edgecolor='k')
        elif intervals[0] <= value_at_50_percentile < intervals[1]:
            ax.bar(angles[j], end_y_50, width=bar_width, bottom=start_y_50, facecolor=colors[1], alpha=1,
                   edgecolor='k')
        elif intervals[1] <= value_at_50_percentile < intervals[2]:
            ax.bar(angles[j], end_y_50, width=bar_width, bottom=start_y_50, facecolor=colors[2], alpha=1,
                   edgecolor='k')
        elif intervals[2] <= value_at_50_percentile < intervals[3]:
            ax.bar(angles[j], end_y_50, width=bar_width, bottom=start_y_50, facecolor=colors[3], alpha=1,
                   edgecolor='k')
        elif value_at_50_percentile >= intervals[3]:
            ax.bar(angles[j], end_y_50, width=bar_width, bottom=start_y_50, facecolor=colors[4], alpha=1,
                   edgecolor='k')

    fig.text(0.5, 0.98, title, fontsize=12, weight="bold", ha="center", va="center")
    if draw_legend:
        legend_elements = [
            mpatches.Patch(color=colors[0], label='<= 0.1'),
            mpatches.Patch(color=colors[1], label='0.1 < and <= 1'),
            mpatches.Patch(color=colors[2], label='1 < and <= 5'),
            mpatches.Patch(color=colors[3], label='5 < and <= 10'),
            mpatches.Patch(color=colors[4], label='> 10'),
        ]

        legend = ax.legend(handles=legend_elements, title='RQ ranges', bbox_to_anchor=(0.05, 1.), loc='upper right',
                           fontsize=12, title_fontsize=12, frameon=False)
        legend.get_title().set_fontweight('bold')
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    if save_as is not None:
        plt.savefig(save_as, dpi=300, bbox_inches="tight")
        plt.close()