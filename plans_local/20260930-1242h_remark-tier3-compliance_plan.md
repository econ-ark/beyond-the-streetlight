# Plan: make econ-ark/beyond-the-streetlight a compliant Tier 3 REMARK

**Status (2026-10-02): EXECUTED through step 8.** PR #1 was merged into `main` (7a83335)
with all four CI jobs green and `cli.py lint --tier 3` reporting no errors. Steps 9-10
(Zenodo DOI, releases v1.1.0/v1.1.1, catalog and website PRs) wait on the owner; they
are tracked in `TODO.md`. Two departures from the plan:
- Actions did not need enabling on the fork.
- PR #2 (8c484e5) replaced the paper drafts with a citation of the published version,
  FEDS 2025-019, which `REMARK.md` links via `identifiers-paper`.

## Context

The repo was last touched on 2025-06-26/27. It was then made "strictly REMARK compliant" (tags v1.0.4, v1.0.5) against the **pre-tier** standard. Since then the standard has changed:

- **Three tiers.** `econ-ark/REMARK` `STANDARD.md` on `main` was rewritten 2025-12-08 → 2025-12-27 (PR #171) into three tiers.
- **New required files at every tier:** `Dockerfile`, `reproduce.sh`, `README.md`, `LICENSE`, `binder/environment.yml`.
- **Tier 2 adds:** `REMARK.md`, `CITATION.cff`, and a README with at least 100 non-empty lines.
- **Tier 3 adds:** `tier: 3` in `REMARK.md`, a Zenodo DOI, and a git tag matching the archive.
- **A `binder/environment.yml` "adapter" is allowed.** It only has to install uv, poetry or pip-tools, which then install from a pinned lockfile.
- **Pending PR #176 (not yet in force)** would require a committed lockfile. We comply anyway.
- **The only checker is `cli.py lint`.** It tests files and line counts, and always exits 0.

An audit of `main` (b84d162) found problems beyond missing files:

- **No `LICENSE`.** The repo fails lint at every tier.
- **`reproduce.sh` does not reproduce.**
  - `code/main/reproduce.py` ignores subprocess failures.
  - No figure is saved (`plt.savefig` is commented out in `code/main/abse_reg.py`).
  - 11 of 12 `results/*.txt` and `data/output/errors.csv` are made only by `code/other/*`, which never runs.
  - The output checks test files that are committed, so they always pass.
- **Conda and Poetry disagree.** They coexist with different pins, and Python 3.9 is past end of life.
- **The Docker image is broken.** It deletes its own Poetry venv during the build.
- **Neither CI workflow has ever run.** Actions stay off on a fork until enabled. `remark-validation.yml` is broken regardless.
- **A FRED API key is hard-coded** in `code/main/scrape_FRED_data.py` line 6. This is a public repo, with the key in history since 2023.
- **The published description is wrong.** The `REMARK.md` body (AI-generated June 2025) describes Google-Ngram web scraping that does not exist. That text is published verbatim on econ-ark.org. `AI_REPOSITORY_DESCRIPTION.md` claims "Apache 2.0" and "Python 3.8+".

**Goal:** an honest Tier 3 REMARK.
- `reproduce.sh` regenerates every computed result and fails loudly on error.
- One pinned environment.
- Accurate metadata.
- Passes `cli.py lint --tier 3` with zero errors.
- A Zenodo DOI tied to a tag, and the catalog and website updated to match.

## Decisions (user, 2026-09-30)

- **Target:** Tier 3, including the Zenodo DOI.
- **Environment:** uv with Python 3.12. `uv.lock` is the single source of truth. `binder/environment.yml` becomes a thin uv adapter, following the `econ-ark/method-of-moderation` pattern. The Dockerfile is uv-based, following the `econ-ark/econ-scenarios` pattern.
- **License:** Apache-2.0, the same as HARK. This makes the repo's existing public claim true.
- **Downstream:** also open PRs to `econ-ark/REMARK` (catalog `tag:`) and `econ-ark/econ-ark.org` (materials page).
- **Branch workflow:** do the work on `remarkification`, then open a PR into `main`. `remarkification` is currently `main` minus 2 commits with 0 unique commits, so updating it is a pure fast-forward.

## Steps

All work is in `/Volumes/Sync/GitHub/econ-ark/beyond-the-streetlight`, one logical change per commit on `remarkification`.

### 0. Branch and plan record
- Check out the branch and bring it up to date:
  ```
  git switch -c remarkification --track origin/remarkification
  git merge --ff-only main
  ```
- Copy this plan to `plans_local/20260930-HHMMh_remark-tier3-compliance_plan.md`, matching the `plans_local/` convention in `HAFiscal-Latest`, and commit it. It contains no secrets.

### 1. FRED key and an offline default
- `code/main/scrape_FRED_data.py`:
  - Read the key from `FRED_API_KEY` and remove the literal.
  - Snapshot the data the published results used: `git mv`-copy today's `data/output/FRED.csv` to `data/raw/FRED_snapshot.csv`.
- Default pipeline: use the snapshot, so it runs offline and without a key, as REMARK tooling and CI require. `./reproduce.sh --refresh-fred` (with `FRED_API_KEY` set) pulls live data instead.
- **User action:** have the key's owner (probably Decory Edwards) revoke it at fred.stlouisfed.org. There will be no history rewrite, since four forks already carry the key.

### 2. uv environment
- **`pyproject.toml`:** convert to PEP 621 `[project]` with `requires-python = ">=3.12,<3.13"` and `[tool.uv] package = false`.
  - A `code/` package would shadow the stdlib `code` module.
  - Drop the broken `[tool.poetry.scripts]` entry.
- **Dependencies:** keep only what the code imports. Check with `grep -rh '^import\|^from' code/`: expected pandas, numpy, matplotlib, openpyxl, statsmodels, fredpy, plus nbconvert and jupyter for the slides.
  - Drop `fredapi` (never imported).
  - Drop `pandas-datareader` and `pyarrow` if unused.
- **Lock:** add `.python-version` (`3.12`), run `uv lock`, and commit `uv.lock`.
- **`binder/environment.yml`:** make it an adapter: `python=3.12`, `pip`, and `pip: [uv==<pinned>]`.
- **`binder/postBuild`:** add it, running `uv export --frozen --no-dev --no-hashes -o /tmp/req.txt && uv pip install --system -r /tmp/req.txt`, then an import check. This copies `econ-ark/method-of-moderation` `binder/`.
- **Delete:** `poetry.lock`, `install.sh`, `run_analysis.sh`, `reproduce_requirements.md` (its content moves to the README), `docker-compose.yml`, `docker-run.sh`.

### 3. A pipeline that actually reproduces
- **`code/main/reproduce.py`:**
  - Run each step with `subprocess.run([sys.executable, f], check=True)`.
  - Set `MPLBACKEND=Agg`.
  - Run from the repo root no matter where it is invoked.
- **`code/main/abse_reg.py`:** replace `plt.show()` with saves of the figures the slides use, `figures/abse_reg_1983_GB_cons_only.png` and `figures/abse_reg_1983_SPF_cons_only.png`.
  - Reconcile it with `code/other/useless.py`, the copy that still has working `savefig` calls.
  - Retire `useless.py` once `abse_reg.py` reproduces its outputs.
- **Supplementary step** (full run only): run `code/other/compute_errors.py`, `sqe_reg.py`, `diff_*`, `xGR_*` and `produce_graphs.py`, which make `errors.csv` and the other `results/*.txt` and figures.
  - Fix any that fail.
  - Anything that cannot be regenerated gets listed in the README as legacy.
- **Static images:** `figures/ev_uncertainty.png` and `figures/ngram-new-economy.png` come from outside the analysis. Document them as such.
- **Slides:** render with `uv run jupyter nbconvert --to slides RS100_Discussion_Slides.ipynb` and copy the result to `index.html`, which GitHub Pages serves from `main`.
  - Stop using `--execute --inplace`: the notebook has 0 code cells, and that flag rewrites a committed file.
- **`reproduce.sh`**, a bash script modelled on econ-scenarios:
  - If not already running under bash, re-exec: `[ -n "$BASH_VERSION" ] || exec bash "$0" "$@"`. `cli.py execute` runs scripts with `$SHELL`, which is zsh on macOS.
  - `set -euo pipefail`, then `cd` to the script's directory.
  - `uv sync --frozen`.
  - **Delete the generated outputs first**, so the existence checks mean something.
  - Run the main pipeline, then the supplementary step, then the slides.
  - Finally run `code/verify_outputs.py` (see below).
- **`reproduce_min.sh`:** the same, but the main pipeline only.
- **`code/verify_outputs.py` (new):** compares regenerated CSVs, and the numeric content of `results/*.txt` with statsmodels' Date/Time lines ignored, against the committed versions (`git show HEAD:<path>`), within a tolerance. It exits non-zero on any mismatch. This proves the committed results reproduce.

### 4. Docker, devcontainer, binder
- **`Dockerfile`**, in the econ-scenarios style:
  - `FROM python:3.12-slim`.
  - `COPY --from=ghcr.io/astral-sh/uv:<pinned> /uv /uvx /bin/` (pinned, not `latest`).
  - `WORKDIR /remark`, `COPY . .`, `RUN uv sync --frozen`.
  - `CMD ["./reproduce.sh"]`.
- **`.dockerignore`:** update to match.
- **`.devcontainer/devcontainer.json`:** fix `workspaceFolder`/`workspaceMount` and the interpreter path (`/remark/.venv/bin/python`). Trim `.devcontainer/README.md`.
- **Note:** `cli.py build docker` uses repo2docker, which reads `binder/` and ignores the root Dockerfile. Both paths are tested in step 8.

### 5. Metadata and docs
- **`LICENSE`:** full Apache-2.0 text, "Copyright 2023–2026 Decory Edwards and Christopher Carroll". Give Decory a courtesy heads-up.
- **`CITATION.cff`** (CFF 1.2.0):
  - Add `license: Apache-2.0`, `url` (the Pages site), and `version: 1.1.0` with the matching `date-released`.
  - Remove the non-CFF `tags:` key.
  - Keep the `references:` entry for Corrado & Kennickell.
  - Validate with `uvx cffconvert --validate`.
- **`REMARK.md`:** replace everything.
  - Front matter:
    - `remark-name: beyond-the-streetlight`
    - `title`
    - `tier: 3`
    - `tags: [REMARK, Reproduction, Notebook]`
    - `keywords`
    - `notebooks: [RS100_Discussion_Slides.ipynb]`
    - `title-original-paper`
    - `authors-original-paper`
    - `summary`
  - Body: an accurate abstract and description of what is reproduced. **Remove all Ngram/web-scraping text.**
  - Keys follow what `econ-ark.org/scripts/populate_remarks.py` and `_layouts/material.html` read.
- **`README.md`:** rewrite following REMARK `main` `README-TEMPLATE-TIER3.md`, with at least 100 non-empty lines. Sections:
  - overview and data sources;
  - the pipeline, and which outputs are regenerated versus static;
  - how to reproduce (uv, Docker, Binder/conda);
  - the FRED snapshot and refresh option;
  - runtime;
  - license and citation.
  - Also fix the existing typos ("Philidelphia", "forcasters", `<repository-url>`).
- **`AI_REPOSITORY_DESCRIPTION.md`:** rewrite briefly so every claim is true (license, Python version, no scraping, current tag).
- **Hygiene:**
  - `git rm data/.DS_Store`.
  - `chmod -x` the `data/raw/*.xlsx` files and `.github/workflows/ci.yml`.

### 6. CI (replace both workflows)
- **Delete `remark-validation.yml`.** It is broken: `cli.py build` without a type, `lint` without `pull`, and `version:` where the catalog uses `tag:`.
- **New `ci.yml`** runs on push to main and on PRs, with three jobs:
  - **`reproduce`:** `astral-sh/setup-uv` (pinned), then `./reproduce.sh`. This includes `verify_outputs.py`.
  - **`container`:** `docker build -t remark .`, then `docker run --rm remark ./reproduce_min.sh`.
  - **`remark-lint`:** check out `econ-ark/REMARK` at `main`, write `REMARKs/beyond-the-streetlight.yml`, and symlink the workspace to `_REMARK/repos/beyond-the-streetlight`.
    - Then run `python cli.py lint REMARKs/beyond-the-streetlight.yml --tier 3 --include-optional`.
    - Fail the job if the output reports any error. Lint itself always exits 0, so read its output format from `cli.py` first.
- If artifacts are uploaded, use `actions/upload-artifact@v4`.

### 7. Local verification before the PR (see Verification)

### 8. PR and merge
- `git push origin remarkification` (a fast-forward on the remote).
- **User action:** enable Actions on the fork (repo → Actions tab → enable workflows). The API reports Actions enabled, but no workflow has ever run.
- Open a PR `remarkification → main`. The body ends with the Claude Code attribution line.
- Merge when CI is green, with a rebase or merge commit to keep the per-change history.

### 9. Tier 3 release (DOI goes last)
- **User action:** in Zenodo → GitHub, switch on `econ-ark/beyond-the-streetlight`. The econ-ark org must have granted the Zenodo app access.
- **Release v1.1.0:** tag it and create a GitHub Release with notes. Zenodo then mints a concept DOI and a version DOI.
- **Record the DOI:**
  - Commit the **concept** DOI to `CITATION.cff` (`doi:`), `REMARK.md` (`DOI:`) and a README badge.
  - Tag **v1.1.1** and create a Release. Zenodo archives it, so the archived copy contains its own DOI.
- Follow `econ-ark/REMARK` `ZENODO-GUIDE.md`. `HAFiscal-dev/REMARK-make/setup-zenodo.sh` is HAFiscal-specific; use it for reference only.

### 10. Downstream PRs
- **`econ-ark/REMARK`:** in `REMARKs/beyond-the-streetlight.yml`, add `tag: v1.1.1` (today there is no `tag:`).
- **`econ-ark/econ-ark.org`:** in `_materials/beyond-the-streetlight.md`, rebuild the front matter from the new `CITATION.cff` and `REMARK.md` front matter, and replace the inaccurate body with the new `REMARK.md` body.

## Verification

- **Clean-clone run:** clone into the scratchpad with `git clone --branch remarkification`, then run `./reproduce.sh` and `./reproduce_min.sh`.
  - Both exit 0.
  - `verify_outputs.py` passes.
  - After deleting and regenerating, `git status` shows only expected changes (PNG bytes, statsmodels timestamps).
  - `--refresh-fred` without a key fails with a clear message.
- **REMARK tooling at `main`:** a fresh scratch clone of `econ-ark/REMARK`, not the local clone, which is on the unmerged PR #176 branch.
  - `python cli.py lint REMARKs/beyond-the-streetlight.yml --tier 3 --include-optional` gives zero errors. The only warning allowed is the DOI, and only until step 9.
  - `python cli.py build conda …` then `execute conda …` exercises the binder adapter and `reproduce_min.sh` under `$SHELL`.
- **Docker:** `docker build -t bts . && docker run --rm bts` (full) and `… ./reproduce_min.sh`. If Docker is unavailable locally, rely on the CI `container` job.
- **Metadata:**
  - `uvx cffconvert --validate`.
  - A YAML parse of the `REMARK.md` front matter.
  - `grep -c . README.md` is at least 100.
  - `grep -ri 'ngram\|scrap\|beautifulsoup\|3\.8' REMARK.md README.md AI_REPOSITORY_DESCRIPTION.md` finds only true mentions (the static Ngram figure).
- **CI:** all three jobs green on the PR.
- **After step 9:** the Zenodo record shows the v1.1.1 archive, and lint gives zero warnings.

## Needs the user (cannot be done by the assistant)

- Enable GitHub Actions on the fork (step 8).
- Enable the Zenodo GitHub integration for the repo (step 9).
- Get the leaked FRED key revoked (step 1).
- Optionally, tell Decory Edwards about the Apache-2.0 license.

## Out of scope

- Rewriting git history to purge the key.
- The upstream `dedwar65/beyond-the-streetlight` repo and its 2023 open PR #1.
- Scientific changes to the analysis beyond making it regenerate its own outputs.
