# Beyond the Streetlight

**Authors**: Decory Edwards and Christopher D. Carroll (Johns Hopkins University)
**Keywords**: forecast errors, Greenbook, Survey of Professional Forecasters, economic measurement
**Status**: Published REMARK (Tier 3) under the [Econ-ARK REMARK standard](https://github.com/econ-ark/REMARK/blob/main/STANDARD.md)
**Repository**: <https://github.com/econ-ark/beyond-the-streetlight>
**Slides**: <https://econ-ark.github.io/beyond-the-streetlight/>

This repository contains Christopher Carroll's discussion of Carol Corrado and
Arthur Kennickell, "100 years of Economic Measurement in the Division of
Research & Statistics: Beyond the Streetlight", presented at the Federal
Reserve Board's [R&S Centennial Conference](https://www.federalreserve.gov/conferences/rs-centennial-conference.htm)
on November 6-8, 2023, together with the data and code behind the
discussion's figures.

## Overview

### Research question

Has forecasting improved over time? The discussion treats the Fed's staff
forecasts as "tertiary" information produced by measurement, and asks whether
the Greenspan Fed's call of a "new economy" in the 1990s was luck, or part of
a long improvement in forecasting at the Fed and elsewhere.

### Methods

- Year-ahead forecasts of the change in the unemployment rate and of real
  personal consumption expenditures (PCE) growth are taken from the
  Greenbook/Tealbook (GB) and from the mean of the Survey of Professional
  Forecasters (SPF), both published by the Federal Reserve Bank of Philadelphia.
- Realized values come from FRED: `UNRATE` and `DPCERA3Q086SBEA`.
- The absolute error of each forecast is regressed on a linear time trend, with
  heteroskedasticity-robust (HC3) standard errors, for the full sample (144
  quarters, labeled 1983Q1-2018Q4) and for 1995 onward.
- Supplementary analyses repeat this for squared errors, for the difference
  between GB and SPF errors, and for samples that exclude 2008-2011.

### Key findings

- Errors in forecasts of real consumption growth trend down for both
  forecasters: -0.039 percentage points a year for the Greenbook and -0.031
  for the SPF over the full sample (both p < 0.001), and they remain negative
  from 1995 on.
- Errors in forecasts of the change in unemployment show no significant trend.
- The two slides "Tertiary Data from Philly Fed and FRED" show the
  consumption-error results (`figures/abse_reg_1983_GB_cons_only.png` and
  `figures/abse_reg_1983_SPF_cons_only.png`).

## Quick start

```bash
git clone https://github.com/econ-ark/beyond-the-streetlight
cd beyond-the-streetlight
./reproduce.sh          # needs uv; or use Docker, below
```

**Expected runtime**: about 30 seconds after the environment is installed.

## Software requirements

- [uv](https://docs.astral.sh/uv/), which installs Python 3.12 and the exact
  package versions pinned in `uv.lock` (pandas, NumPy, statsmodels, matplotlib,
  openpyxl, fredpy, nbconvert). `pyproject.toml` lists the direct dependencies.
- Or [Docker](https://www.docker.com/get-started), with nothing else installed.
- Or conda, using `binder/environment.yml`, which provides Python and uv.

The code runs on Linux and macOS, and in the Docker image on any platform.
No network access or API key is needed to reproduce the results.

## Installation

### With uv (recommended)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # if uv is not installed
uv sync --frozen                                  # creates .venv from uv.lock
```

`reproduce.sh` runs `uv sync --frozen` itself, so this step is optional.

### With Docker

```bash
docker build -t beyond-the-streetlight .
docker run --rm beyond-the-streetlight                      # ./reproduce.sh
docker run --rm beyond-the-streetlight ./reproduce_min.sh   # main pipeline only
```

The repository also contains a VS Code / Cursor dev container built from the
same `Dockerfile`; see `.devcontainer/README.md`.

### With conda or Binder

```bash
conda env create -f binder/environment.yml --prefix ./condaenv
conda activate ./condaenv
./reproduce.sh
```

`binder/environment.yml` only provides Python and uv, as the REMARK standard
allows; the packages come from `uv.lock`. On
[Binder](https://mybinder.org/v2/gh/econ-ark/beyond-the-streetlight/HEAD),
`binder/postBuild` also installs them into the notebook's environment.

## Reproduction instructions

### Full reproduction

```bash
./reproduce.sh
```

**What it does**: installs the environment, runs the 19 steps of the analysis
(`code/main/reproduce.py --all`), and renders the slides. Every output is
deleted before the step that makes it runs, and the run fails unless each
regenerated CSV and regression summary matches the committed version (to
within floating-point rounding; statsmodels' date stamps are ignored).

**Expected runtime**: about 30 seconds.
**Output location**: `data/output/`, `results/`, `figures/`, and the slides in
`RS100_Discussion_Slides.slides.html` and `index.html`.

### Quick verification

```bash
./reproduce_min.sh
```

Runs only the main pipeline, from the raw data to the regression and the two
figures in the slides (6 steps, 9 outputs), with the same checks.
**Runtime**: a few seconds.

## Outputs

| Output | Made by | Notes |
|---|---|---|
| `data/output/GB.csv`, `SPF.csv` | `code/main/parse_*_raw_data.py` | forecasts parsed from `data/raw/*.xlsx` |
| `data/output/FRED.csv` | `code/main/scrape_FRED_data.py` | copy of `data/raw/FRED_snapshot.csv` |
| `data/output/forecast.csv` | `code/main/annual_forecasts.py` | year-ahead forecasts and outcomes |
| `data/output/abs_errors.csv` | `code/main/compute_abs_error.py` | absolute forecast errors |
| `results/abse_reg_{1983,1995}.txt` | `code/main/abse_reg.py` | trend regressions; the main results |
| `figures/abse_reg_1983_{GB,SPF}_cons_only.png` | `code/main/abse_reg.py` | the figures in the slides |
| `figures/abse_reg_{1983,1995}.png` | `code/main/abse_reg.py` | all four error series |
| `data/output/errors.csv` | `code/other/compute_errors.py` | squared forecast errors |
| `results/`, `figures/` `sqe_reg_*` | `code/other/sqe_reg.py` | trends in squared errors |
| `results/`, `figures/` `diff_*_reg_*` | `code/other/diff_*_reg.py` | GB error minus SPF error |
| `results/`, `figures/` `xGR_*` | `code/other/xGR_*.py` | excluding 2008-2011 |
| `figures/{unemp,cons}_forecast.png` | `code/other/produce_graphs.py` | forecasts against outcomes |

These files are not produced by the code:

- `figures/ev_uncertainty.png` (a result from Will Du's HANK-and-SAM model) and
  `figures/ngram-new-economy.png` (a Google Books Ngram chart of "new economy")
  are images from outside this analysis, shown in the slides.
- `figures/abse_reg_1995_cons_only.png` is a legacy figure that no current
  script makes.
- `RS100_Discussion_Slides.pdf` is a static export of the slides.

## Data availability

### Included data

- `data/raw/GBweb_Row_Format.xlsx`: the Greenbook data set, and
  `data/raw/meanLevel.xlsx`, `meanGrowth.xlsx`: SPF mean forecasts, all from
  the [Federal Reserve Bank of Philadelphia](https://www.philadelphiafed.org/surveys-and-data/real-time-data-research).
- `data/raw/FRED_snapshot.csv`: the FRED data used for the published results,
  retrieved on 2023-11-03.

### External data

To use current FRED data instead of the snapshot, get a free
[FRED API key](https://fred.stlouisfed.org/docs/api/api_key.html) and run:

```bash
FRED_API_KEY=... ./reproduce.sh --refresh-fred
```

FRED revises these series, so results then differ somewhat from the committed
ones, and the comparison with them is skipped.

## Code organization

```text
code/main/        the main pipeline; reproduce.py runs every step in order
code/other/       supplementary analyses (run by reproduce.sh, not reproduce_min.sh)
data/raw/         inputs: Philadelphia Fed spreadsheets and the FRED snapshot
data/output/      intermediate data sets
results/          regression summaries
figures/          figures
RS100_Discussion_Slides.ipynb   the slides (reveal.js, via nbconvert)
paper/            drafts of the Corrado and Kennickell paper under discussion
references/       the 1997 Economic Report of the President (cited in the slides)
about/            the conference agenda and invitation
```

## Parameter modification guide

- **Sample start**: the regression scripts take `1983` (default) or `1995`,
  e.g. `uv run python code/main/abse_reg.py 1995`; run them from the
  repository root.
- **Excluded period**: `code/other/xGR_*.py` drop 2008-01-01 to 2011-12-31;
  edit `start_date_to_exclude` and `end_date_to_exclude` to change it.
- **Data vintage**: `--refresh-fred`, above.

After changing parameters, `code/main/reproduce.py --no-verify` reruns the
pipeline without comparing against the committed outputs.

## Known issues

`code/other/diff_abse_reg.py` reads `data/output/errors.csv`, which holds
squared errors, so its results duplicate those of `diff_sqe_reg.py`. The
committed `results/diff_abse_reg_*.txt` were produced this way, so the script
is kept as it is.

## License and citation

The code is licensed under the Apache License 2.0 (`LICENSE`); `NOTICE` lists
the third-party material in the repository that the license does not cover.
To cite this work, use the metadata in `CITATION.cff` (GitHub's "Cite this
repository" button).
