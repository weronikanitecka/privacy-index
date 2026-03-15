# Guardatum Privacy Index

**The ethical eye on your digital life.**

An AI-powered, enforcement-informed privacy policy risk index for Europe's most-visited websites — scored against the 7 core GDPR principles and cross-referenced with public DPA enforcement records.

🌐 **Live index:** [guardatum.github.io/privacy-index](https://weronikanitecka.github.io/privacy-index/)

---

## What it is

The Guardatum Privacy Index scores privacy policies as written documents against GDPR principles. It is the first index to:

- Score at scale using AI-assisted analysis (NLP + GDPR fine-tuning)
- Cross-reference policy scores with documented DPA enforcement history
- Surface the gap between what companies *say* in their policies and what regulators have *found* them to actually do

**Data asset principle:** Guardatum's intelligence is about companies, not users. No user data is collected or stored.

---

## Repository structure

```
guardatum-index/
├── index.html              # The full interactive index
├── data/
│   ├── privacy_scores.json # GDPR principle scores for all 98 websites
│   └── dpa_fines.json      # Documented DPA fines from enforcementtracker.com
├── scripts/
│   └── update_fines.py     
└── README.md
```

---

## Data sources

| Source | What it provides | Update frequency |
|--------|-----------------|------------------|
| Guardatum AI analysis | GDPR principle scores (0–10) per policy | Quarterly |
| CMS GDPR Enforcement Tracker (enforcementtracker.com) | Documented DPA fines across the EU | Manual quarterly refresh |
| EDPB public register | Binding decisions and cross-border cases | Manual as needed |

---

## About Guardatum

Guardatum is a privacy intelligence company building tools that make data rights transparent and actionable — in real time, at the moment of consent, not after your data has already been shared.

- **CEO:** Weronika Nitecka — [weronika@guardatum.org](mailto:weronika@guardatum.org)
- **CTO:** Estera Kot, PhD
- **Website:** [guardatum.org](https://guardatum.org)

---

## License & attribution

The index and underlying scores are published under **CC BY 4.0** — you may use, share, and adapt this data with attribution.

DPA enforcement data is sourced from [CMS GDPR Enforcement Tracker](https://www.enforcementtracker.com/) and is used for informational purposes. All fines are publicly documented.

This index scores policies as written documents and does not constitute legal advice.
