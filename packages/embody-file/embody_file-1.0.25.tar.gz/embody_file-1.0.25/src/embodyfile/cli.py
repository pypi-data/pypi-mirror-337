"""cli entry point for embodyfile.

Parse command line arguments, invoke methods based on arguments.
"""

import argparse
import logging
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from . import __version__
from . import embodyfile


def main(args=None):
    """Entry point for embody-file cli.

    The .toml entry_point wraps this in sys.exit already so this effectively
    becomes sys.exit(main()).
    The __main__ entry point similarly wraps sys.exit().
    """
    if args is None:
        args = sys.argv[1:]

    parsed_args = __get_args(args)
    logging.basicConfig(
        level=getattr(logging, parsed_args.log_level.upper(), logging.INFO),
        format="%(asctime)s:%(levelname)s:%(message)s",
        datefmt="%H:%M:%S",
    )

    if not parsed_args.src_file.exists():
        logging.error(f"Source file not found: {parsed_args.src_file}. Exiting.")
        exit(-1)

    dst_file = parsed_args.src_file.with_suffix(f".{parsed_args.output_format.lower()}")
    if dst_file.exists() and not parsed_args.force:
        logging.error(
            f"Destination exists: {dst_file}. Use --force to force parsing to destination anyway."
        )
        exit(-1)

    with open(parsed_args.src_file, "rb") as f:
        try:
            data = embodyfile.read_data(
                f, parsed_args.strict, samplerate=parsed_args.samplerate
            )
            logging.info(f"Loaded data from: {parsed_args.src_file}")
        except Exception as e:
            logging.info(f"Reading file failed: {e}", exc_info=True)
            exit(0)

    if parsed_args.print_stats:
        logging.info(f"Stats printed for file: {parsed_args.src_file}")
        exit(0)

    if parsed_args.analyse_ppg:
        embodyfile.analyse_ppg(data)
        exit(0)

    if parsed_args.plot:
        __plot_data(data)
        exit(0)

    if parsed_args.output_format == "CSV":
        embodyfile.data2csv(data, dst_file)
    elif parsed_args.output_format == "HDF":
        embodyfile.data2hdf(data, dst_file)
    else:
        logging.error(f"Unknown output format: {parsed_args.output_format}")
        exit(-1)


def __plot_data(data):
    sensor_data_available = data.sensor and len(data.sensor) > 0
    multi_sensor_data_avilable = (
        data.multi_ecg_ppg_data and len(data.multi_ecg_ppg_data) > 0
    )
    if not sensor_data_available and not multi_sensor_data_avilable:
        logging.warn("No ecg/ppg data in file")
        exit(-1)
    pd_data = (
        embodyfile._to_pandas(data.sensor)
        if sensor_data_available
        else embodyfile._multi_data2pandas(data.multi_ecg_ppg_data)
    )
    if not sensor_data_available:
        logging.info(f"Plotting all columns. Columns: {pd_data.columns}")

    num_columns = len(pd_data.columns)
    fig, axes = plt.subplots(num_columns, 1, sharex=True)

    # Generate a unique color for each plot using a colormap
    cmap = plt.get_cmap("viridis")
    colors = cmap(np.linspace(0, 1, num_columns))

    for i, col in enumerate(pd_data.columns):
        axes[i].plot(pd_data[col], label=col, color=colors[i])
        axes[i].legend()

    plt.show()


def __get_args(args):
    """Parse arguments passed in from shell."""
    return __get_parser().parse_args(args)


def __get_parser():
    """Return ArgumentParser for pypyr cli."""
    parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description="EmBody CLI application",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "src_file", help="Location of the binary source file", type=Path
    )
    log_levels = ["CRITICAL", "WARNING", "INFO", "DEBUG"]
    parser.add_argument(
        "--log-level",
        help=f"Log level ({log_levels})",
        choices=log_levels,
        default="INFO",
    )
    parser.add_argument(
        "--version",
        action="version",
        help="Echo version number.",
        version=f"{__version__}",
    )
    parser.add_argument(
        "--force",
        help="Force decoding if CSV file exists",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--strict",
        help="Fail on any parse errors",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--output-format",
        help="Output format for decoded data (CSV, HDF)",
        choices=["CSV", "HDF"],
        default="HDF",
    )

    parser.add_argument(
        "--print-stats",
        help="Print stats (without outputting anything)",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--analyse-ppg",
        help="Analyse PPG data",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--plot",
        help="Plot in graph in stead of convert",
        action="store_true",
        default=False,
    )

    samplerates = ["1000", "500", "250", "125"]
    parser.add_argument(
        "--samplerate",
        help=f"Samplerate ({samplerates})",
        choices=samplerates,
        default="1000",
    )

    return parser


if __name__ == "__main__":
    main()
