import requests
import dns.resolver
from datetime import datetime, timezone
from typing import Optional

DISPOSABLE_EMAIL_DOMAINS = {
    "mailinator.com", "tempmail.com", "guerrillamail.com",
    "10minutemail.com", "throwawaymail.com", "yopmail.com",
    "trashmail.com", "fakeinbox.com"
}

def check_domain_age(domain: str) -> Optional[int]:
    try:
        response = requests.get(f"https://rdap.org/domain/{domain}", timeout=5)
        if response.status_code != 200:
            return None
        data = response.json()
        for event in data.get("events", []):
            if event.get("eventAction") == "registration":
                reg_date = datetime.fromisoformat(event["eventDate"].replace("Z", "+00:00"))
                return (datetime.now(timezone.utc) - reg_date).days
        return None
    except Exception:
        return None

def check_mx_record(domain: str) -> Optional[bool]:
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return len(records) > 0
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return False
    except Exception:
        return None

def check_disposable_email(email_domain: str) -> bool:
    return email_domain.lower().strip() in DISPOSABLE_EMAIL_DOMAINS