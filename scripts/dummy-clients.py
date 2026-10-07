#!/usr/bin/env python3
"""
Sample client generator for CSVN.

Runs during GitHub Actions builds to populate the site with
SAMPLE vendors for demonstration purposes. Every sample has
"_dummy": true and "_sample": true, and its file name starts
with "DUMMY-".

These are OBVIOUSLY FICTIONAL placeholder profiles. They are:
  - Named "Sample Vendor — [Category]" so no real business is implied
  - Marked status = "Sample" so no buyer mistakes them for real vendors
  - Used only to demonstrate how the directory looks when populated

TO REMOVE ALL SAMPLE DATA PERMANENTLY:
  1. Delete this file from the repo
  2. Commit
That's it. The next build will skip sample generation.
"""
import json
import random
import re
from pathlib import Path

PER_CATEGORY = 10

# Categories that already have real vendors — skip sample generation for these
SKIP_CATEGORIES = {
    "chartered-accountants",
}

random.seed(20260101)

root = Path(__file__).resolve().parent.parent
cats_file = root / "data" / "categories.json"
out_dir = root / "data" / "clients"
out_dir.mkdir(parents=True, exist_ok=True)

CITIES = [
    ("Mumbai","Maharashtra"),("Pune","Maharashtra"),
    ("Bangalore","Karnataka"),("Chennai","Tamil Nadu"),
    ("Hyderabad","Telangana"),("Gurgaon","Haryana"),
    ("Noida","Uttar Pradesh"),("Ahmedabad","Gujarat"),
    ("Kolkata","West Bengal"),("Jaipur","Rajasthan"),
    ("Indore","Madhya Pradesh"),("Coimbatore","Tamil Nadu"),
]

REVIEWERS = [
    "Rahul S.","Priya P.","Amit K.","Sneha R.","Vikram S.",
    "Anita D.","Rohan M.","Kavita N.","Suresh I.","Meera J.",
]

REVIEW_TEXTS = [
    "Sample review — this is a placeholder to demonstrate how reviews will appear on CSVN.",
    "Sample review — real customer feedback will replace these once vendors are onboarded.",
    "Sample review — demonstration content only, not an actual customer testimonial.",
]

CLIENT_COMPANIES = [
    "Sample Client A","Sample Client B","Sample Client C",
    "Sample Client D","Sample Client E","Sample Client F",
]

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def gen_name(cat_name, idx):
    base = cat_name.split("&")[0].split("/")[0].strip()
    if idx == 0:
        return f"Sample Vendor — {base}"
    return f"Sample Vendor {idx + 1} — {base}"

def gen_client(cat, idx):
    name = gen_name(cat["name"], idx)
    city, state = random.choice(CITIES)
    slug = slugify(name)
    if not slug.endswith(str(idx + 1)) and idx > 0:
        slug = f"{slug}-{idx + 1}"

    return {
        "_dummy": True,
        "_sample": True,
        "id": slug,
        "name": name,
        "tagline": f"Sample listing for {cat['name']} — demonstration profile only.",
        "category": cat["slug"],
        "tier": "Standard",
        "order": idx + 1,
        "city": city,
        "area": state,
        "rating": 0,
        "reviewCount": 0,
        "since": 2026,
        "experience": "—",
        "status": "Sample",
        "phone": "+91 00000 00000",
        "whatsapp": "+91 00000 00000",
        "email": "sample@csvn.in",
        "website": "",
        "address": f"Sample Address, {city}",
        "hours": "—",
        "mapUrl": "",
        "about": [
            f"This is a SAMPLE profile for the {cat['name']} category. "
            f"It demonstrates how a real CSVN listing will appear once vendors "
            f"are onboarded. No real business is represented by this profile."
        ],
        "services": [
            f"{cat['name']} — Sample Service 1",
            f"{cat['name']} — Sample Service 2",
            f"{cat['name']} — Sample Service 3",
            "Sample Service 4",
            "Sample Service 5",
        ],
        "catalogues": [],
        "clients": random.sample(CLIENT_COMPANIES, 2),
        "reviews": [
            {"name": random.choice(REVIEWERS), "rating": 5, "text": random.choice(REVIEW_TEXTS)}
            for _ in range(2)
        ],
        "social": {"facebook": "", "instagram": "", "youtube": ""},
    }

def main():
    with open(cats_file, encoding="utf-8") as f:
        cats_data = json.load(f)

    total = 0
    skipped = 0

    for cat in cats_data["categories"]:
        slug = cat["slug"]

        # Skip categories that have real vendors
        if slug in SKIP_CATEGORIES:
            old_dummy = out_dir / f"DUMMY-{slug}.json"
            if old_dummy.exists():
                old_dummy.unlink()
                print(f"Skipped + removed sample data for {slug}")
            skipped += 1
            continue

        clients = [gen_client(cat, i) for i in range(PER_CATEGORY)]
        out_file = out_dir / f"DUMMY-{slug}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(clients, f, indent=2, ensure_ascii=False)
        total += len(clients)

    print(f"Generated {total} SAMPLE clients across {len(cats_data['categories']) - skipped} categories")
    print(f"Skipped {skipped} categories with real vendors")

    old = out_dir / "clients-01.json"
    if old.exists():
        old.unlink()
        print("Removed legacy clients-01.json sample")

if __name__ == "__main__":
    main()
