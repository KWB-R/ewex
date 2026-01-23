import math
from math import pi

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt, patches as mpatches
import seaborn as sns
from matplotlib.ticker import FixedLocator

from ewex.simulate_removal import SimulationResult


def er_profiles(
        sim_results: list[SimulationResult],
        case_study_name: str | None = None,
        save_as: str | None = None,
        no_mixture: bool = True,
        c_scale: str | None = None,
        color_palette: list = ["Grays"],
        font_size: int = 12,
        reference_value: float | None = True
):
    output_c_df = pd.concat([r.output_c_df.assign(scenario=r.scenario.name) for r in sim_results])
    output_c_df = pd.melt(output_c_df, id_vars="scenario")
    if reference_value is not None:
        reference_value = sim_results[0].scenario.reference.ref_value_ng_l
    substance_name = sim_results[0].scenario.substance.name
    # set the scale for concentration y axis
    max_c = output_c_df.max(numeric_only=True).max()
    if (reference_value is not None and c_scale is not None):
        if (max_c / reference_value) > 100:
            c_scale = "log"
    else:
        c_scale = "linear"

    if len(color_palette) == 1:
        color_palette = color_palette[0]

    fig = plt.figure(
        figsize=(4 + len(sim_results) * len(sim_results[0].scenario.treatment_train) / (1 + int(len(sim_results) > 1)),
                 4 + len(sim_results) * len(sim_results[0].scenario.treatment_train) / (1 + int(len(sim_results) > 1))))
    gs = fig.add_gridspec(2, height_ratios=[1, 2])
    axs = gs.subplots()

    # Negative removal should be displayed reverse (input concentration / output Concentration),
    # so that every process is between 0 and 100%
    # maybe displayed in another color
    # not implemented yet!!!!!
    sns.violinplot(
        x="variable", y="value",
        data=output_c_df,
        hue="scenario",
        # color=np.random.choice(["silver", "orange", "yellow", "blue"]),
        cut=0,
        density_norm="width",
        inner=None,
        saturation=1,
        palette=color_palette,
        ax=axs[0],
        legend="brief" if len(sim_results) > 1 else False
    )

    if len(sim_results) > 1:
        plt.setp(axs[0].get_legend().get_texts(), fontsize=font_size)
        plt.setp(axs[0].get_legend().get_title(), fontsize=font_size)
    plt.xticks(fontsize=font_size, rotation=0)
    plt.yticks(fontsize=font_size, rotation=0)

    axs[0].set_title(f"At CS: '{case_study_name}'" if case_study_name is not None else "")
    axs[0].set_ylabel(substance_name + " (ng/L)", fontsize=font_size)
    if reference_value is not None:
        axs[0].axhline(y=reference_value, color='black', linestyle='--')
    axs[0].set_xlabel('Treatment step outlet', fontsize=font_size)
    axs[0].set_yscale(c_scale)

    rmv_factor_df = pd.concat([r.rmv_factor_df.assign(scenario=r.scenario.name) for r in sim_results])
    if no_mixture:
        mixture_columns = [rmv_factor_df.columns.get_loc(col) for col in rmv_factor_df.columns if "dil" in col]
        rmv_factor_df = rmv_factor_df.drop(rmv_factor_df.columns[mixture_columns], axis=1)
    rmv_factor_df = pd.melt(rmv_factor_df, id_vars="scenario")

    sns.violinplot(
        x="value", y="variable",
        data=rmv_factor_df,
        hue="scenario",
        cut=0,
        density_norm="width",
        inner=None,
        saturation=1,
        palette=color_palette,
        orient="h",
        ax=axs[1],
        legend="brief" if len(sim_results) > 1 else False
    )

    if len(sim_results) > 1:
        plt.setp(axs[1].get_legend().get_texts(), fontsize = font_size)
        plt.setp(axs[1].get_legend().get_title(),fontsize = font_size)
    ## Legen above the plot
    # plt.setp(axs[1].legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left",
    #            mode="expand", borderaxespad=0, ncol=3, fontsize = font_size))
        plt.setp(axs[1].legend(loc="right", fontsize=font_size))


    axs[1].set_title(substance_name + f" at CS: '{case_study_name}'" if case_study_name is not None else "")
    axs[1].set_xlabel('Reduction of concentration (removal or dilution) in %', fontsize = font_size)
    axs[1].set_ylabel('Treatment step outlet', fontsize = font_size)
    plt.xticks(fontsize = font_size, rotation = 0)
    plt.yticks(fontsize = font_size, rotation = 0)

    left, right = plt.xlim()
    if left < -1000:
        axs[1].set_xlim(-1000, 150)
    if save_as is not None:
        plt.savefig(save_as, dpi=300)
    return fig


def spider_plot(
        sim_results: list[SimulationResult],
        case_study_name: str | None = None,
):

    rq = [r.final_concentration / r.scenario.reference.ref_value_ng_l for r in sim_results]

    output_c_df = pd.DataFrame(np.column_stack(rq),
                               columns=[
                                   f"{case_study_name if case_study_name is not None else f'result {i}'}  {r.scenario.name}"
                                   for i, r in enumerate(sim_results)]
                               )

    percentiles = [0.50, 0.75, 0.95, 0.99]
    stats = output_c_df.describe(percentiles)
    categories = stats.columns
    N = len(categories)
    angles = np.linspace(0, 2 * pi, N, endpoint=False)
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

    XTICKS = ax.xaxis.get_major_ticks()
    for tick in XTICKS:
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
    bar_width = 2 * np.pi / N

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

    title = "Reference quotient (RQ) percentiles in final media"
    fig.text(0.5, 0.98, title, fontsize=12, weight="bold", ha="center", va="center")
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
    return fig
