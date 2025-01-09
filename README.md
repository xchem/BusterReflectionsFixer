# BusterReflectionsFixer
Quick fix for Ryan's missing buster reflections values

## Usage at DLS

For use at DLS metagrate has been set up at `/dls/science/groups/i04-1/software/max/BusterReflectionsFixer`

To use it:

1. Load the python environment

```
source /dls/science/groups/i04-1/software/max/load_py310.sh
```

2. See the (barebones) help screen:

```
$FIXER --help
```

3. Get missing values for a specific key from the buster report

```
$FIXER SOURCE TEMPLATE
```

- `SOURCE` is the path to the directory containing MMCIF's with missing values

- `MODEL_BUILDING` is the path to the model building directory

The script will go through every file matching `--pattern` (default `*-x????.mmcif`) in the `SOURCE` directory and look for the `--key` entry (default `_refine_ls_shell.number_reflns_R_free`). It will then look for the corresponding buster report in the `MODEL_BUILDING` subdirectories (named `Refine_*-report` by default) and grab the value from there.

Outputs are written to a directory called `_fixed` in the same place as the `SOURCE` directory
