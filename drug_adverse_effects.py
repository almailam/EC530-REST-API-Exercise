#!/usr/bin/env python3
"""
Script to fetch all adverse effects associated with a particular drug from the FDA openFDA API.
Uses the Drug Adverse Event Reporting System (FAERS) data.
Returns adverse effects with report counts when available.
"""

import argparse
import sys

import requests

FDA_EVENT_API = "https://api.fda.gov/drug/event.json"


def fetch_adverse_effects(drug_name: str, limit: int = 1000) -> list[tuple[str, int]]:
    """
    Query the FDA Drug Adverse Event API for all adverse effects associated with a drug.
    Uses the count endpoint to get report counts per adverse effect (MedDRA term).

    Args:
        drug_name: The drug name to search for (e.g., "LIPITOR", "ASPIRIN").
        limit: Maximum number of adverse effects to return (default 1000, API max).

    Returns:
        List of (adverse_effect, report_count) tuples, sorted by count descending.
    """
    # Search for records where this drug appears; count by reaction (MedDRA preferred term)
    # Use patient.drug.medicinalproduct for drug search - FAERS often uses uppercase
    params = {
        "search": f'patient.drug.medicinalproduct:"{drug_name}"',
        "count": "patient.reaction.reactionmeddrapt.exact",
        "limit": limit,
    }

    try:
        response = requests.get(FDA_EVENT_API, params=params, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"API request failed: {e}", file=sys.stderr)
        return []

    data = response.json()
    results = data.get("results", [])

    # Count API returns [{"term": "REACTION_NAME", "count": N}, ...]
    adverse_effects = [(r["term"], r["count"]) for r in results if r.get("term")]

    return adverse_effects


def main():
    parser = argparse.ArgumentParser(
        description="Fetch adverse effects for a drug from the FDA openFDA API."
    )
    parser.add_argument(
        "drug",
        nargs="?",
        default=None,
        help="Drug name to search (e.g., LIPITOR, ASPIRIN, METFORMIN)",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=1000,
        help="Max number of adverse effects to return (default: 1000)",
    )
    args = parser.parse_args()

    limit = args.limit
    drug_name = args.drug

    while True:
        if not drug_name:
            drug_name = input("\nEnter drug name (or 'q' to quit): ").strip()
        if not drug_name or drug_name.lower() == "q":
            print("Quitting")
            break

        print(f"\nFetching adverse effects for '{drug_name}' from FDA API...")
        print("-" * 60)

        adverse_effects = fetch_adverse_effects(drug_name, limit=limit)

        if not adverse_effects:
            print(f"No adverse effects found for '{drug_name}'.")
            print(
                "Tip: Try the exact brand/generic name (e.g., LIPITOR, ASPIRIN). "
                "FAERS data often uses uppercase."
            )
            retry = input("Try another drug? (y/n): ").strip().lower()
            if retry != "y":
                break
            drug_name = None
            continue

        print(f"\n{'ADVERSE EFFECTS FOR: ' + drug_name.upper():^60}")
        print(f"{'Total unique adverse effects: ' + str(len(adverse_effects)):^60}")
        print("=" * 60)
        print(f"{'Adverse Effect':<45} {'Reports':>10}")
        print("-" * 60)

        for effect, count in adverse_effects:
            display_name = effect.title() if effect.isupper() else effect
            print(f"{display_name:<45} {count:>10,}")

        print("=" * 60)
        print(
            "\nNote: Data from FDA FAERS (2004–present). Reports may list multiple "
            "drugs per event; the specific drug causing each reaction is not identified."
        )

        again = input("\nSearch another drug? (y/n): ").strip().lower()
        if again != "y":
            break
        drug_name = None


if __name__ == "__main__":
    main()
