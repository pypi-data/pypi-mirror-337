# -*- coding: utf-8 -*-

"""Main functions for garytale package."""

import logging
from pathlib import Path
from typing import Sequence

from itertools import batched
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 14})
import pandas as pd

_log = logging.getLogger(__package__)

def plot_uvvis(
    filename: str,
    lambdas: Sequence,
    *,
    to_plot=None,
    plot_lambda_title: str = "",
    plot_time_title: str = "",
    write_time_data_into_csv=False,
    time_data_path="time_data",
    show_plots=True,
    save_pictures=True,
    picture_path="pictures",
    linewidth=1.2,
    drop_over=None,
    y_label="Attenuance",
    y_lim=None,
    lambda_plot_options: dict = {},
    lambda_legend_options: dict = {},
    time_plot_options: dict = {},
    time_legend_options: dict = {},
):
    """Generate an attenuance vs. wavelength and attenauance vs. time plot from Aglient Cary 60 spectrophotometer data.
    The measurement should stem from a kinetics scan measurement (repeated measurements over a wavelength range).
    The file name (parsed as a relative path from the current working directory) and a sequence (list, tuple, etc.)
    containing the wavelengths the attenunance vs. time plot should use need to be provided.

    Parameters:
        filename: str
            Path to the .csv file generated from the spectrophotometer
        lambdas: Sequence
            All wavelengths that the attenuance vs. time plot should contain
        to_plot: Sequence, default: None
            Sequence of indices that are used to select the scans in the attenuance vs. wavelength plot
        plot_lambda_title: str, default: ""
            Title of the attenuance vs. wavelength plot
        plot_time_title: str, default: ""
            Title of the attenuance vs. time plot
        write_time_data_into_csv: bool, default: False
            Generate a nicer .csv file from the input data containing the attenuances and times in seconds, without
            additional device data.
        time_data_path: str, default: "time_data"
            The relative **folder** path the .csv file should be saved to.
        show_plots: bool, default: True
            Call plt.show() after generation
        save_pictures: bool, default: True
            Save the plots to .png files
        picture_path: str, default "pictures"
            The relative **folder** path the images should be saved to.
        linewidth: float, default: 1.2
            The line width used in attenuance vs. wavelength plots.
        drop_over: float, default: None
            Attenuances over drop_over will not be plotted.
        y_label: str, default: "Attenuance"
            y label used in plots
        y_lim: float, default: None
            ylim used for attenuance vs. time plots
        lambda_plot_opts: dict
            Any additional keyword arguments to be passed to the plot function for the attenuance vs. wavelength plots.
            Fore more information see https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
        lambda_legend_opts: dict
            Any additional keyword arguments to be passed to the legend function for the attenuance vs. wavelength plots.
            Fore more information see https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html
        time_plot_opts: dict
            Any additional keyword arguments to be passed to the plot function for the attenuance vs. time plots.
            Fore more information see https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
        time_legend_opts: dict
            Any additional keyword arguments to be passed to the legend function for the attenuance vs. time plots.
            Fore more information see https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html

    Notes:
        - The attenuance vs. wavelength plot lists the scan start time in the legend. As a scan is not instantaneous,
            this seems like the best option.
        - The attenuance vs. time plot calculates the exact time the wavelength was measured from the scan start time
            and the scan rate.

    """

    lambda_plot_opts = {"lw": linewidth}
    lambda_plot_opts.update(lambda_plot_options)
    lambda_legend_opts = {"prop": {"size": 10}}
    lambda_legend_opts.update(lambda_legend_options)
    time_plot_opts = {}
    time_plot_opts.update(time_plot_options)
    time_legend_opts = {"prop": {"size": 10}}
    time_legend_opts.update(time_legend_options)

    csv_dataframe = pd.read_csv(filename, low_memory=False, skiprows=0)
    # remove last column from view
    df = csv_dataframe.iloc[:, :-1]

    # NOTE: in min
    start_times = (
        df[df.iloc[:, 0].str.contains("[Time]", regex=False)]
        .iloc[:, 1]
        .to_numpy()
        .astype(float)
    )
    _log.debug(f"Found {len(start_times)} scan start times")
    # NOTE: in nm/min
    scan_rate = float(
        df[df.iloc[:, 0].str.contains("Scan rate", regex=False)].iat[0, 0].split()[-1]
    )
    _log.info(f"Found a scan rate of {scan_rate} nm/min")
    # NOTE: in nm
    start_lambda = float(
        df[df.iloc[:, 0].str.contains("Start Wavelength", regex=False)]
        .iat[0, 0]
        .split()[-1]
    )
    _log.info(f"Found a wavelength at measurement start of {start_lambda} nm")

    # drop any rows containing NaN values, so everything below the data points
    df = df[~df.isna().any(axis=1)]
    graphs = []
    for i, j in batched(range(len(df.columns)), 2):
        graph = df.iloc[1:, [i, j]].apply(pd.to_numeric)
        # drop any rows over value
        if drop_over:
            graph = graph[graph.iloc[:, 1] <= drop_over]
        graphs.append(graph)

    # NOTE: make some default selection for nicer plotting
    if to_plot is None:
        selected_idxs = [0, 2, 4]
        if len(graphs) <= 100:
            selected_idxs += [i for i in range(9, len(graphs), 15)]
        else:
            selected_idxs += [i for i in range(9, 99, 15)] + [
                i for i in range(99, len(graphs), 50)
            ]
        selected_scans = [graphs[i] for i in selected_idxs]
        _log.debug(f"Selection is {selected_idxs}")
        if _log.getEffectiveLevel() == logging.DEBUG:
            _log.debug(f"Respective start times of selection: {[start_times[i] for i in selected_idxs]}")
    else:
        selected_scans = [graphs[i] for i in to_plot]
        selected_idxs = to_plot
    # NOTE: build 2-tuple of selected scans and respective selected start times
    selected = (selected_scans, [start_times[i] for i in selected_idxs])
    _log.debug(f"First 10 selected start times: {selected[1][:10]}")

    # NOTE: plot first element to get ax object
    ax = selected[0][0].plot(x=0, y=1, label=f"{selected[1][0] * 60:.0f} s", **lambda_plot_opts)
    for graph, time in zip(selected[0][1:], selected[1][1:]):
        graph.plot(x=0, y=1, ax=ax, label=f"{time * 60:.0f} s", **lambda_plot_opts)
    plt.xlabel(r"$\lambda$ (nm)", labelpad=2.0)
    plt.ylabel(y_label, labelpad=2.0)
    if plot_lambda_title:
        plt.title(plot_lambda_title)
    if save_pictures:
        picture_path = Path(picture_path)
        picture_path.mkdir(exist_ok=True)
        plt.savefig(
            picture_path / f"wavelen_{filename[:-4]}",
            bbox_inches="tight",
            dpi=300,
        )
    plt.legend(**lambda_legend_opts)
    if show_plots:
        plt.show()

    times = []
    vals = []
    for lmbd in lambdas:
        t = []
        v = []
        assert len(graphs) > 0 and len(start_times) > 0
        for graph, time in zip(graphs, start_times):
            # NOTE: convert to seconds after calculating appropriate time
            t.append((time + (start_lambda - lmbd) / scan_rate) * 60)
            xs_ys = graph.iloc[:, [0, 1]]
            closest_wavelen_val = xs_ys[
                xs_ys.iloc[:, 0]
                == min(xs_ys.iloc[:, 0], key=lambda x: abs(float(x) - lmbd))
            ].iat[0, 1]
            v.append(closest_wavelen_val)
        # NOTE: ignore IDE warning that closest_wavelen_val might be unbound
        _log.debug(
            f"Closest wavelength found at last iteration for {lmbd} nm is {closest_wavelen_val} nm"
        )
        _log.debug(f"First 10 time elements for {lmbd} nm: {t[:10]}")
        _log.debug(f"First 10 attenuances for {lmbd} nm: {v[:10]}")
        times.append(t)
        vals.append(v)

    for t, v, lmbd in zip(times, vals, lambdas):
        plt.plot(t, v, label=rf"${lmbd}\,$nm", **time_plot_opts)
    plt.xlabel(r"$t$ (s)", labelpad=2.0)
    plt.ylabel(y_label, labelpad=2.0)
    if y_lim is not None:
        plt.ylim(y_lim)
    plt.legend(**time_legend_opts)
    if plot_time_title:
        plt.title(plot_time_title)
    if write_time_data_into_csv:
        export = []
        for z in zip(times, vals):
            export.extend(z)
        export = pd.DataFrame(export).T
        time_label = [f"Times for {lmbd} nm in s" for lmbd in lambdas]
        att = ["Attenuance"] * len(lambdas)
        cols = []
        for z in zip(time_label, att):
            cols.extend(z)
        export.columns = cols
        _log.debug(f"Export dataframe head: {export.head()}")
        time_data_path = Path(time_data_path)
        time_data_path.mkdir(exist_ok=True)
        export.to_csv(time_data_path / f"data_{filename}", index=False)
    if save_pictures:
        plt.savefig(
            picture_path / f"time_{filename[:-4]}", bbox_inches="tight", dpi=300
        )
    if show_plots:
        plt.show()
