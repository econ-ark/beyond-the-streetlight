# AI Repository Description: Beyond the Streetlight

A short, factual summary for AI assistants and indexers. `README.md` is the
full documentation; `CITATION.cff` and `REMARK.md` hold the formal metadata.

## What this is

- Christopher Carroll's discussion (slides) of Carol Corrado and Arthur
  Kennickell, "100 years of Economic Measurement in the Division of Research &
  Statistics: Beyond the Streetlight", Federal Reserve Board R&S Centennial
  Conference, November 6-8, 2023.
- The code and data behind the discussion's figures, by Decory Edwards and
  Christopher Carroll (Johns Hopkins University).
- An Econ-ARK REMARK, targeting Tier 3 of the REMARK standard.

## The analysis

- Forecasts: Greenbook/Tealbook (Federal Reserve Board staff) and the Survey of
  Professional Forecasters mean, from the Federal Reserve Bank of Philadelphia
  (committed spreadsheets in `data/raw/`).
- Outcomes: FRED series `UNRATE` and `DPCERA3Q086SBEA`, from a committed
  snapshot retrieved on 2023-11-03 (optionally refreshed through the FRED API).
- Method: absolute (and, in supplementary analyses, squared) year-ahead
  forecast errors for the change in unemployment and for real PCE growth,
  regressed on a linear time trend with HC3 standard errors; full sample of
  144 quarters labeled 1983Q1-2018Q4, and 1995 onward.
- Finding: consumption-growth forecast errors fall significantly over time for
  both forecasters (about -0.04 and -0.03 percentage points a year); errors in
  unemployment forecasts show no significant trend.

There is no web scraping and no text analysis. The Google Books Ngram chart in
the slides is a static image.

## Reproduction

- `./reproduce.sh` (all 36 outputs and the slides, about 30 seconds) and
  `./reproduce_min.sh` (main pipeline only); both verify the outputs against the
  committed versions and fail otherwise.
- Environment: Python 3.12 and packages pinned in `uv.lock`, installed by uv;
  also a `Dockerfile` and a conda/Binder adapter in `binder/`.
- No network access or credentials needed.

## License

Apache License 2.0 for the code; `NOTICE` lists third-party material (the
Philadelphia Fed and FRED data, drafts of the paper under discussion, and other
documents) that the license does not cover.
