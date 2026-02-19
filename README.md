# EC530 REST API Exercise

Uses the [FDA openFDA Drug Adverse Event API](https://open.fda.gov/apis/drug/event/) to fetch adverse effects for a given drug, with report counts.

## Usage

```bash
pip install -r requirements.txt
python3 drug_adverse_effects.py ASPIRIN
python3 drug_adverse_effects.py LIPITOR --limit 20
```

## Concept
User stories:
- As a patient, I want to be able to check my medication list for any adverse effects.
- As a doctor, I want to be able to check the number of reports of adverse effects for each medication.
