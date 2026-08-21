from typing import Optional

SANCTIONED_TEST_NAMES = {"sanctioned_test", "sanctioned test"}

def calculate_risk(client_name, domain_age_days, registry_match_found, mx_valid, disposable_email) -> dict:
    sanctions_hit = client_name.lower().strip() in SANCTIONED_TEST_NAMES
    if sanctions_hit:
        return {"risk_score": "HIGH", "risk_points": 999, "sanctions_hit": True}
    points = 0
    if domain_age_days is not None and domain_age_days < 180:
        points += 2
    if mx_valid is False:
        points += 2
    if disposable_email:
        points += 2
    if registry_match_found is False:
        points += 1
    risk_score = "HIGH" if points >= 5 else "MEDIUM" if points >= 2 else "LOW"
    return {"risk_score": risk_score, "risk_points": points, "sanctions_hit": False}