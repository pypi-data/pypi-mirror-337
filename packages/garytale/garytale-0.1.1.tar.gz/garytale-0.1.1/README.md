# Garytale

Library for working with Aglient Cary 60 kinetics scan measurements with simultaneous irradiation, as seen in the working group under Prof. Wöll (IPC RWTH Aachen).

## Installation

Installing via pip:

```
pip install garytale
```

## Usage

```
import garytale

# uncomment this line if you want log output (i.e. when working in an interactive shell).
# garytale.enable_logging("info")

garytale.plot_uvvis("example_measurements/example_filename.csv", (265, 345))
```

For tuning the output:

```
garytale.plot_uvvis(
    "example_measurements/example_filename.csv",
    (265, 345),
    write_time_data_into_csv = True/False,     
    show_plots = True/False,
    save_pictures = True/False,
)
```

For all available options (csv output and picture saving path, keyword arguments for matplotlib functions, etc.), refer to the docstrings by opening up an interactive Python console:

```
python
>>> import garytale
>>> help(garytale)
>>> help(garytale.plot_uvvis)
```

## Development

Poetry is used as the project's build system. Install it with pipx:

```
pipx install poetry
```

or use another installation method (see https://python-poetry.org/docs/#installation for details).

When in a virtual environment, you can run `poetry install` to install all current dependencies specified in poetry.lock. It is recommended to use development versions in a virtual environment. Poetry can spawn and activate these by running `eval $(poetry env activate)` (Linux, etc.) or `Invoke-Expression (poetry env activate)` (Windows Powershell). Leave the virtual enviroment with `deactivate`. For more information see https://python-poetry.org/docs/basic-usage/#using-your-virtual-environment.
