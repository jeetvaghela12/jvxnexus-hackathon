from typing import Optional

SANCTIONED_TEST_NAMES = {"sanctioned_test", "sanctioned test"}

def calculate_risk(client_name, domain_age_days, registry_match_found, mx_valid, disposable_email) -> dict:
    sanctions_hit = client_name.lower().strip() in SANCTIONED_TEST_NAMES
    if sanctions_hit:
        return {
            "risk_score": "HIGH", "risk_points": 999, "sanctions_hit": True,
            "reasoning": ["This name matches a sanctions watchlist entry \u2014 automatic HIGH risk, overriding every other signal."]
        }

    points = 0
    reasoning = []

    if domain_age_days is not None:
        if domain_age_days < 180:
            points += 2
            reasoning.append(f"Domain is only {domain_age_days} days old (under 6 months) \u2014 +2 risk points.")
        else:
            reasoning.append(f"Domain is {domain_age_days} days old, well established \u2014 no risk added.")
    else:
        reasoning.append("Domain age could not be determined \u2014 treated as neutral, no points added.")

    if mx_valid is False:
        points += 2
        reasoning.append("No valid email server found for this domain \u2014 +2 risk points.")
    elif mx_valid is True:
        reasoning.append("Domain has a valid, working email server \u2014 no risk added.")
    else:
        reasoning.append("Email server check could not be completed \u2014 treated as neutral.")

    if disposable_email:
        points += 2
        reasoning.append("This is a known disposable/temporary email domain \u2014 +2 risk points.")
    else:
        reasoning.append("Email domain is not on the disposable-email list \u2014 no risk added.")

    risk_score = "HIGH" if points >= 5 else "MEDIUM" if points >= 2 else "LOW"
    return {"risk_score": risk_score, "risk_points": points, "sanctions_hit": False, "reasoning": reasoning}