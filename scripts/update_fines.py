"""
Guardatum — DPA Enforcement Data Updater
----------------------------------------
This script is a template for automating updates to dpa_fines.json
from public enforcement databases.

CURRENT STATUS: Manual curation (Edition 1)
FUTURE: Automated scraping of enforcementtracker.com + CNIL + ICO feeds

Usage:
    python scripts/update_fines.py

Requirements:
    pip install requests beautifulsoup4

Data sources:
    - CMS GDPR Enforcement Tracker: https://www.enforcementtracker.com/
    - CNIL decisions: https://www.cnil.fr/en/decisions
    - ICO decisions: https://ico.org.uk/action-weve-taken/
    - EDPB register: https://www.edpb.europa.eu/our-work-tools/consistency-findings/register-for-article-60-final-decisions_en
    - UODO (Poland): https://uodo.gov.pl/en/p/decisions
"""

import json
import os
from datetime import datetime

# Companies we track — add new ones as the index expands
TRACKED_COMPANIES = [
    "Google.com", "YouTube.com", "Facebook.com", "Instagram.com",
    "WhatsApp.com", "Netflix.com", "TikTok.com", "LinkedIn.com",
    "Spotify.com", "Twitter/X.com", "Uber.com", "Airbnb.com",
    "Booking.com", "Discord.com", "Snapchat.com", "Deliveroo.co.uk",
    "Bumble.com", "Badoo.com", "Amazon (EU domains)",
]

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'dpa_fines.json')


def load_current_fines():
    """Load existing fine records."""
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_fines(data):
    """Save updated fine records."""
    data['meta']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(data['fines'])} companies with fine records.")


def add_fine(data, company_name, fine_record):
    """
    Add a new fine record for a company.
    
    fine_record should be a dict with:
        amount (int): Fine amount in base currency
        currency (str): "EUR" or "GBP"
        dpa (str): Name of the Data Protection Authority
        country (str): Country of the DPA
        year (int): Year fine was issued
        article (str): GDPR article(s) violated
        summary (str): Plain English description of the violation
        url (str): Source URL
    """
    if company_name not in data['fines']:
        data['fines'][company_name] = []
    
    # Check for duplicates by year + dpa + amount
    existing = data['fines'][company_name]
    is_duplicate = any(
        e['year'] == fine_record['year'] and
        e['dpa'] == fine_record['dpa'] and
        e['amount'] == fine_record['amount']
        for e in existing
    )
    
    if is_duplicate:
        print(f"  Skipping duplicate: {company_name} — {fine_record['dpa']} {fine_record['year']}")
        return False
    
    data['fines'][company_name].append(fine_record)
    print(f"  Added: {company_name} — {fine_record['dpa']} {fine_record['year']} — €{fine_record['amount']:,}")
    return True


def get_total_fines(data):
    """Calculate total documented fines."""
    total = sum(
        f['amount'] for fines in data['fines'].values()
        for f in fines
    )
    count = sum(len(fines) for fines in data['fines'].values())
    return total, count


def print_summary(data):
    """Print a summary of current fine data."""
    total, count = get_total_fines(data)
    print(f"\n=== Guardatum DPA Fine Database ===")
    print(f"Last updated: {data['meta']['last_updated']}")
    print(f"Companies with fines: {len(data['fines'])}")
    print(f"Total fine records: {count}")
    print(f"Total documented value: €{total:,.0f}")
    print(f"\nTop 5 by total fine value:")
    
    sorted_companies = sorted(
        data['fines'].items(),
        key=lambda x: sum(f['amount'] for f in x[1]),
        reverse=True
    )
    
    for company, fines in sorted_companies[:5]:
        company_total = sum(f['amount'] for f in fines)
        print(f"  {company}: €{company_total:,.0f} ({len(fines)} fine{'s' if len(fines) > 1 else ''})")


# ── FUTURE IMPLEMENTATION NOTES ───────────────────────────────────────────────
#
# To implement automated scraping from enforcementtracker.com:
#
# 1. The site loads data via an internal API endpoint. Inspect the network
#    requests in browser devtools to find the JSON endpoint.
#
# 2. Filter results by company name to find relevant fines.
#
# 3. Check their terms of service before automating. For non-commercial
#    research/public interest use, reach out to fines@enforcementtracker.com
#    to ask about data access — they may provide it directly.
#
# 4. CNIL publishes decisions at https://www.cnil.fr/en/decisions in a 
#    structured format. RSS feed available.
#
# 5. The ICO publishes enforcement actions at https://ico.org.uk/action-weve-taken/
#    No API, but structured HTML scraping is feasible.
#
# ─────────────────────────────────────────────────────────────────────────────


if __name__ == '__main__':
    data = load_current_fines()
    print_summary(data)
    
    # Example: add a new fine manually
    # add_fine(data, "NewCompany.com", {
    #     "amount": 1000000,
    #     "currency": "EUR",
    #     "dpa": "CNIL",
    #     "country": "France",
    #     "year": 2025,
    #     "article": "Art. 6",
    #     "summary": "Description of the violation.",
    #     "url": "https://www.cnil.fr/en/decisions/..."
    # })
    # save_fines(data)
