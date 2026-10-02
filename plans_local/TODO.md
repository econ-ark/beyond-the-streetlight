# TODO (owner-sequenced)

Items here are tracked, not auto-run: when an item's trigger fires, SURFACE it to
the owner (Christopher Carroll); don't execute it unasked.

- [ ] **Zenodo DOI and the Tier 3 release** (owner, 2026-10-02: "add to todo").
  Steps 9-10 of `20260930-1242h_remark-tier3-compliance_plan.md`.
  **Trigger:** the owner says the Zenodo GitHub integration is switched on for
  `econ-ark/beyond-the-streetlight`. Releasing before that leaves the release unarchived.
  1. Owner: Zenodo → GitHub → enable the repository. The econ-ark org must have granted
     the Zenodo app access.
  2. Tag `v1.1.0` on `main` and publish a GitHub Release. Zenodo then mints a concept DOI
     and a version DOI.
  3. Commit the **concept** DOI to `CITATION.cff` (`doi:`), `REMARK.md` (`DOI:`) and a
     README badge. Set `date-released` in `CITATION.cff` to the real release date (it now
     says 2026-09-30). Tag `v1.1.1` and release, so the archive contains its own DOI.
     Don't use `cli.py lint` to confirm this. Its DOI test passes on any `doi:` or `10.`
     in `CITATION.cff`, and since 2026-10-02 the file already holds the cited paper's DOI
     (FEDS 2025-019). So the warning is gone while this REMARK still has no DOI of its
     own. Check for a top-level `doi:` instead.
  4. PR to `econ-ark/REMARK`: add `tag: v1.1.1` to `REMARKs/beyond-the-streetlight.yml`.
  5. PR to `econ-ark/econ-ark.org`: rebuild `_materials/beyond-the-streetlight.md` from
     `CITATION.cff` plus the `REMARK.md` front matter and body.
     - Its current body is the inaccurate Ngram/web-scraping text.
     - Its front matter lacks `github_repo_url`, so the page shows no GitHub or Binder
       buttons.

## Deferred: revisit

- [ ] **`code/other/diff_abse_reg.py` regresses squared errors, not absolute ones**
  (owner, 2026-10-02: "remember this to revisit in the future").
  - **The problem:** the script reads `data/output/errors.csv` (squared errors, from
    `compute_errors.py`) instead of `abs_errors.csv`. So
    `results/diff_abse_reg_{1983,1995}.txt` and `figures/diff_abse_reg_*.png` duplicate
    the `diff_sqe_reg_*` outputs; they are identical apart from timestamps (checked
    2026-09-30).
  - **Why it was left:** the committed results were produced this way, so the script was
    left unchanged and the problem is documented under "Known issues" in `README.md`.
    No slide uses these outputs.
  - **The fix:** read `abs_errors.csv`, regenerate both years, and commit the new results
    together with the code. `reproduce.py` flags the outputs as not reproducing until
    then. Then drop the README "Known issues" entry.
  - **Trigger:** any work on the supplementary analyses, or the next release after v1.1.1.

## Decided, no action

- **The FRED API key committed in `code/main/scrape_FRED_data.py` from 2023 to 2026-09-30.**
  It was removed from the code then and stays in git history. Owner, 2026-10-02: "ignore".
  Don't raise it again.
- **The `paper/` drafts.** Owner, 2026-10-02: "you can delete them, but you should see if
  you can find a final public version to replace the draft". The final version is
  FEDS 2025-019, by Corrado, Kennickell and Cajner, https://doi.org/10.17016/FEDS.2025.019.
  It is cited in place of the drafts, and `paper/` was deleted in PR #2 (merged as 8c484e5).
  The drafts remain in git history.
