# crude-sd-model

Bottom-up monthly US crude oil supply & demand balance, built entirely from
free public data (EIA, state agencies, FERC, CER) and reconciled against
EIA's published balance. Publishes an automated markdown report per month.

See **SPEC.md** for the full four-phase design. Phase 1 (PADD-level balance
from EIA alone) is implemented here.

## Quickstart

```bash
pip install -r requirements.txt
cp .env.example .env          # paste your free EIA API key into .env

# 1. one-time: verify series IDs in config/series_map.yaml against the
#    EIA browser (https://www.eia.gov/opendata/browser/petroleum), then:
python -m model refresh --start 2021-01

# 2. inspect
python -m model status
python -m model balance --month 2026-05

# 3. publish reports/2026-05/report.md + charts
python -m model publish --month 2026-05
```

No API key yet? Prove the pipeline with synthetic data:

```bash
PYTHONPATH=. python tests/demo_synthetic.py   # loads fake data, publishes a report
PYTHONPATH=. python tests/test_balance.py     # unit tests on the balance engine
```

## The identity

```
production + imports + net_receipts + stock_draw
  = refinery_inputs + exports + residual
```

The **residual** is the diagnostic: nationally it should track EIA's own
adjustment line (see the reconciliation section of each report); regionally
it flags data gaps and, in Phase 3, misallocated pipeline flows.

## Layout

```
config/series_map.yaml   EIA series IDs -> (region, metric, units) — data, not code
config/style.mplstyle    one chart style everywhere
model/ingest/            one loader per source (EIA live; NDIC/RRC/CER/FERC stubbed)
model/db.py              DuckDB, vintage-versioned (every revision kept)
model/balance.py         the identity
model/reconcile.py       model residual vs EIA adjustment
model/publish.py         markdown + PNG report writer
reports/YYYY-MM/         committed output — the repo is the archive
```

## Phase status

| Phase | What | Status | Entry point |
|---|---|---|---|
| 1 | PADD balance from EIA | **Built + tested** | `python -m model refresh / balance / publish` |
| 2 | Basin production (NDIC, RRC, NM OCD) + revision tracker | **Built** (loaders take downloaded CSVs) | loaders in `model/ingest/`; `python -m model revisions --source RRC` |
| 3 | Pipeline network + allocation engine + FERC/CER calibration | **Built + tested** | `config/network.yaml`; `python -m model network` |
| 4 | WPSR weekly nowcast, refined products, automation | **Built + tested** | `python -m model nowcast / products`; `.github/workflows/monthly.yml`; `_quarto.yml` |

Phase 2/3 loaders parse locally downloaded exports (NDIC/RRC/OCD/CER/FERC
formats drift and some need form-driven downloads); each module's docstring
gives the source URL and expected columns, and `COLUMN_ALIASES` absorbs
header renames without code changes.

## Before first real run (one-time checklist)

1. Verify EIA series IDs in `config/series_map.yaml` (monthly, weekly, product
   sections) against https://www.eia.gov/opendata/browser/petroleum
2. Fill in the inter-PADD `movements:` matrix (currently `VERIFY_*` placeholders)
3. Sanity-check nameplate capacities in `config/network.yaml`
4. Add `EIA_API_KEY` as a GitHub Actions secret for the monthly cron
