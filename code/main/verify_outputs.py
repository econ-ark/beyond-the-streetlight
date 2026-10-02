"""Compare regenerated outputs with the versions that were there before the run.

Used by reproduce.py. CSV files and regression summaries (results/*.txt) must
match their earlier versions: text exactly, numbers to within a tolerance that
absorbs last-digit floating-point differences across platforms and library
versions. The Date/Time stamps in statsmodels summaries are ignored. Figures
are only checked for existence, because PNG bytes depend on the platform's
font rendering.
"""
import math
import re
from pathlib import Path

import pandas as pd

RTOL, ATOL = 1e-9, 1e-12
STAMPS = re.compile(r"(Date:\s+\w{3}, \d{2} \w{3} \d{4})|(Time:\s+\d{2}:\d{2}:\d{2})")
NUMBER = re.compile(r"-?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")


def _close(a, b):
    return math.isclose(a, b, rel_tol=RTOL, abs_tol=ATOL)


def compare_csv(new, old):
    a, b = pd.read_csv(new), pd.read_csv(old)
    if list(a.columns) != list(b.columns) or a.shape != b.shape:
        return f"columns/shape differ: {a.shape} vs {b.shape}"
    for col in a.columns:
        x, y = a[col], b[col]
        if pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y):
            both_nan = x.isna() & y.isna()
            diff = ~both_nan & ~pd.Series(
                [_close(p, q) for p, q in zip(x.fillna(0), y.fillna(0))], index=x.index)
            diff |= x.isna() ^ y.isna()
            if diff.any():
                return f"column {col!r} differs in {int(diff.sum())} row(s)"
        elif not x.astype(str).equals(y.astype(str)):
            return f"column {col!r} differs"
    return None


def compare_text(new, old):
    a = STAMPS.sub("", Path(new).read_text()).splitlines()
    b = STAMPS.sub("", Path(old).read_text()).splitlines()
    if len(a) != len(b):
        return f"{len(a)} lines vs {len(b)}"
    for n, (la, lb) in enumerate(zip(a, b), 1):
        if NUMBER.sub("#", la) != NUMBER.sub("#", lb):
            return f"line {n} text differs"
        na, nb = NUMBER.findall(la), NUMBER.findall(lb)
        if any(not _close(float(p), float(q)) for p, q in zip(na, nb)):
            return f"line {n} numbers differ"
    return None


def verify(outputs, expected_dir, root):
    """Return a list of problems; empty means every output reproduced."""
    problems = []
    for rel in outputs:
        new, old = Path(root, rel), Path(expected_dir, rel)
        if not new.is_file() or new.stat().st_size == 0:
            problems.append(f"{rel}: not produced")
        elif not old.is_file() or rel.endswith(".png"):
            continue
        elif rel.endswith(".csv"):
            if msg := compare_csv(new, old):
                problems.append(f"{rel}: {msg}")
        elif msg := compare_text(new, old):
            problems.append(f"{rel}: {msg}")
    return problems
