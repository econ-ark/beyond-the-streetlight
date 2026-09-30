"""Run the analysis from the raw data to the results and figures.

Usage (normally via reproduce.sh or reproduce_min.sh):

    python code/main/reproduce.py [--all] [--refresh-fred] [--no-verify]

  --all           also run the supplementary analyses: the 1995-onward
                  subsample, squared errors, GB-minus-SPF differences, the
                  samples excluding 2008-2011 (xGR_*), and the forecast plots
  --refresh-fred  download current FRED data instead of using the 2023
                  snapshot (needs FRED_API_KEY; verification is then skipped,
                  because FRED revises the data)
  --no-verify     skip the comparison with the earlier outputs

Each step's outputs are deleted before it runs, a failing step stops the run,
and afterwards every output is compared with the version that was there
before (in a fresh clone, the committed one). A step that silently fails
therefore cannot pass for a successful reproduction.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time

from verify_outputs import verify

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def abse_reg(year):
    return (["code/main/abse_reg.py", year],
            [f"results/abse_reg_{year}.txt", f"figures/abse_reg_{year}.png",
             f"figures/abse_reg_{year}_GB_cons_only.png",
             f"figures/abse_reg_{year}_SPF_cons_only.png"])


# (command, outputs) in the order they must run
MAIN = [
    (["code/main/parse_GB_raw_data.py"], ["data/output/GB.csv"]),
    (["code/main/parse_SPF_raw_data.py"], ["data/output/SPF.csv"]),
    (["code/main/scrape_FRED_data.py"], ["data/output/FRED.csv"]),
    (["code/main/annual_forecasts.py"], ["data/output/forecast.csv"]),
    (["code/main/compute_abs_error.py"], ["data/output/abs_errors.csv"]),
    abse_reg("1983"),
]

SUPPLEMENTARY = [
    abse_reg("1995"),
    (["code/other/compute_errors.py"], ["data/output/errors.csv"]),
    *[([f"code/other/{name}.py", year], [f"results/{name}_{year}.txt", f"figures/{name}_{year}.png"])
      for name in ["sqe_reg", "diff_sqe_reg", "diff_abse_reg", "xGR_sqe_reg", "xGR_diff_sqe_reg"]
      for year in ["1983", "1995"]],
    (["code/other/produce_graphs.py"], ["figures/unemp_forecast.png", "figures/cons_forecast.png"]),
]


def main(args):
    steps = MAIN + (SUPPLEMENTARY if "--all" in args else [])
    refresh = "--refresh-fred" in args
    check = not refresh and "--no-verify" not in args
    outputs = [path for _, paths in steps for path in paths]
    env = dict(os.environ, MPLBACKEND="Agg")
    start_time = time.time()

    with tempfile.TemporaryDirectory() as expected:
        # Keep the current outputs to compare against, then remove them
        for rel in outputs:
            src = os.path.join(ROOT, rel)
            if os.path.isfile(src):
                os.makedirs(os.path.dirname(os.path.join(expected, rel)), exist_ok=True)
                shutil.copy2(src, os.path.join(expected, rel))
                os.remove(src)

        for command, _ in steps:
            if refresh and command[0].endswith("scrape_FRED_data.py"):
                command = command + ["--refresh"]
            print(f"==> {' '.join(command)}", flush=True)
            subprocess.run([sys.executable, *command], cwd=ROOT, env=env, check=True)

        print(f"Ran {len(steps)} steps in {time.time() - start_time:.1f} seconds")

        if not check:
            print("Skipping comparison with earlier outputs")
            return 0
        problems = verify(outputs, expected, ROOT)
        if problems:
            print("Outputs that did not reproduce:", *problems, sep="\n  ", file=sys.stderr)
            return 1
        print(f"All {len(outputs)} outputs reproduced")
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
