# 📓 Telecom KPI Dashboard — Guide

## Purpose
This project generates a multi-panel management dashboard from raw operational data,
mirroring the kind of weekly/monthly reporting done at IHS Towers.

## How to Run
```bash
pip install -r requirements.txt
python dashboard/kpi_definitions.py    # Test KPI registry
python dashboard/generate_dashboard.py # Generate full dashboard + Excel report
```

## Dashboard Panels
| Panel | What It Shows |
|-------|---------------|
| Availability by Region | Which regions have the best/worst site uptime |
| On-Time Delivery by Vendor | Vendor delivery punctuality comparison |
| Monthly Accuracy Trend | How delivery accuracy changes over 12 months |
| Supply Risk Events | Geographic breakdown of fuel risk events |
| Fuel Autonomy Distribution | Portfolio-wide fuel security histogram |
| Executive KPI Summary | Top-level numbers in a single view |

## KPI Definitions
See `dashboard/kpi_definitions.py` for:
- Full KPI registry with formulas and targets
- `get_kpi_status()` function for GREEN/AMBER/RED RAG status

## Excel Report
The script also generates `outputs/kpi_report.xlsx` with three sheets:
- **Summary** — top-level KPI values
- **By Region** — performance breakdown by geographic zone
- **By Vendor** — vendor-level performance metrics

## Customisation
- Change colour palette: edit `PRIMARY_COLOR`, `DANGER_COLOR` etc. in `generate_dashboard.py`
- Add new KPI: define in `kpi_definitions.py`, then add a panel in `generate_dashboard.py`
- Change targets: update `target` values in `KPI_REGISTRY` dict
