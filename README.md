# crude-oil-analysis

Python tools for crude oil market analysis. Built to develop 
quantitative skills in the energy field.


## Projects

### Crude Oil Supply & Demand Balance
`crude_balance.py` — Pulls five weekly EIA series (production, imports, 
exports, refinery inputs, ending stocks), merges them into one balance 
sheet, and calculates the implied vs actual weekly stock change.

**What it shows:** Whether the US crude market is drawing or building, 
plus the "adjustment factor" — the gap between what the balance equation 
implies and what EIA actually reports. This is the same unaccounted-for 
crude metric EIA itself tracks internally.

**Concepts covered:** multi-series API pulls, DataFrame merges, unit 
conversion (rate vs level), custom functions, dictionaries, string 
formatting
