"""
kpi_definitions.py
==================
Central registry of all KPI definitions, formulas, targets, and descriptions.
Import this module to ensure consistent KPI computation across all dashboards.
"""

KPI_REGISTRY = {
    "delivery_accuracy_pct": {
        "name":        "Delivery Accuracy",
        "description": "% of deliveries where quantity delivered is within ±5% of quantity ordered",
        "formula":     "COUNT(within_tolerance=1) / COUNT(*) * 100",
        "target":      95.0,
        "unit":        "%",
        "higher_is_better": True,
    },
    "on_time_delivery_pct": {
        "name":        "On-Time Delivery Rate",
        "description": "% of deliveries arriving on or before scheduled date",
        "formula":     "COUNT(actual_date <= scheduled_date) / COUNT(*) * 100",
        "target":      90.0,
        "unit":        "%",
        "higher_is_better": True,
    },
    "site_availability_pct": {
        "name":        "Site Availability",
        "description": "% of time a site is operational (not in critical/major downtime)",
        "formula":     "(Total mins - Downtime mins) / Total mins * 100",
        "target":      99.5,
        "unit":        "%",
        "higher_is_better": True,
    },
    "mttr_hrs": {
        "name":        "Mean Time To Resolve (MTTR)",
        "description": "Average hours to resolve a network alarm from start to clear",
        "formula":     "AVG(clear_time - start_time) in hours",
        "target":      3.0,
        "unit":        "hours",
        "higher_is_better": False,
    },
    "supply_risk_events": {
        "name":        "Supply Risk Events",
        "description": "Count of sites with < 2 days of fuel autonomy after delivery",
        "formula":     "COUNT(days_of_autonomy < 2)",
        "target":      0,
        "unit":        "events",
        "higher_is_better": False,
    },
    "vendor_composite_score": {
        "name":        "Vendor Composite Score",
        "description": "Weighted score combining timeliness, accuracy, documentation, escalation rate",
        "formula":     "Timeliness*35 + Accuracy*30 + DocAccuracy*20 + (1-EscRate)*15",
        "target":      85.0,
        "unit":        "score",
        "higher_is_better": True,
    },
}

def get_kpi_status(kpi_key: str, value: float) -> str:
    """Returns GREEN / AMBER / RED status based on KPI target."""
    kpi = KPI_REGISTRY.get(kpi_key)
    if not kpi: return "UNKNOWN"
    target = kpi["target"]
    better = kpi["higher_is_better"]
    if better:
        if value >= target:          return "GREEN"
        elif value >= target * 0.95: return "AMBER"
        else:                        return "RED"
    else:
        if value <= target:           return "GREEN"
        elif value <= target * 1.10:  return "AMBER"
        else:                         return "RED"

if __name__ == "__main__":
    print("KPI Registry:")
    for key, kpi in KPI_REGISTRY.items():
        print(f"  {kpi['name']}: target={kpi['target']}{kpi['unit']} ({'↑' if kpi['higher_is_better'] else '↓'})")
    print("\nStatus examples:")
    print(f"  Delivery accuracy 96%: {get_kpi_status('delivery_accuracy_pct', 96)}")
    print(f"  Delivery accuracy 88%: {get_kpi_status('delivery_accuracy_pct', 88)}")
    print(f"  MTTR 2.5 hrs: {get_kpi_status('mttr_hrs', 2.5)}")
    print(f"  MTTR 5.0 hrs: {get_kpi_status('mttr_hrs', 5.0)}")
