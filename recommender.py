"""
EE355 Phase 3 - Friend Recommendation System
Content-based filtering using person attributes from networkDB_phase3.txt
"""

import re
from datetime import datetime


# ─────────────────────────────────────────────
#  1. PARSE THE DATABASE
# ─────────────────────────────────────────────

def parse_database(filename):
    """
    Reads networkDB_phase3.txt and returns a list of person dictionaries.
    Each person has: fname, lname, birthdate, email, phone, and any
    extra key-value attributes (college, major, state, interest, ...).
    """
    people = []

    with open(filename, 'r') as f:
        content = f.read()

    # Split on separator lines (dashes)
    blocks = re.split(r'-{4,}', content)

    for block in blocks:
        lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
        if len(lines) < 5:
            continue  # skip incomplete blocks

        person = {}
        person['fname']     = lines[0]
        person['lname']     = lines[1]
        person['birthdate'] = lines[2]

        # Lines 3 and 4 are email and phone (order may vary)
        for line in lines[3:5]:
            if '@' in line:
                person['email'] = line
            else:
                person['phone'] = line

        # Lines 5+ are extra key: value attributes
        person['extra'] = {}
        for line in lines[5:]:
            if ':' in line:
                key, _, val = line.partition(':')
                person['extra'][key.strip().lower()] = val.strip().lower()

        people.append(person)

    return people


# ─────────────────────────────────────────────
#  2. FEATURE EXTRACTION HELPERS
# ─────────────────────────────────────────────

def get_birth_year(bdate_str):
    """Parse birth year from M/D/YYYY or MM/DD/YYYY string."""
    try:
        parts = bdate_str.split('/')
        return int(parts[2])
    except Exception:
        return None


def get_area_code(phone_str):
    """Extract the 3-digit area code from a phone contact string like '(Cell) 310-555-1234'."""
    digits = re.sub(r'\D', '', phone_str)  # keep only digits
    if len(digits) >= 3:
        return digits[:3]
    return None


def get_email_domain(email_str):
    """Extract domain from email contact string like '(Gmail) user@gmail.com'."""
    match = re.search(r'@([\w.]+)', email_str)
    if match:
        return match.group(1).lower()
    return None


def get_code_name(fname, lname):
    """Unique ID: concat fname+lname, lowercase, no spaces. (from misc.cpp logic)"""
    return (fname + lname).replace(' ', '').lower()


# ─────────────────────────────────────────────
#  3. SIMILARITY SCORING
# ─────────────────────────────────────────────

def compute_similarity(p1, p2):
    """
    Computes a similarity score (0.0 to 1.0) between two people
    based on shared attributes. Higher = more similar = better match.

    Scoring breakdown (total possible = 5 points, then normalized):
      - Same college            : +2.0  (strong signal)
      - Same major              : +2.0  (strong signal)
      - Same interest           : +1.5
      - Same state              : +1.0
      - Same area code          : +1.0
      - Same email domain       : +0.5
      - Age within 5 years      : +1.0
      - Age within 10 years     : +0.5
    """
    MAX_SCORE = 9.0  # sum of all possible points above
    score = 0.0
    reasons = []

    # --- College ---
    c1 = p1['extra'].get('college', '')
    c2 = p2['extra'].get('college', '')
    if c1 and c2 and c1 != 'none' and c1 == c2:
        score += 2.0
        reasons.append(f"Same college ({c1.title()})")

    # --- Major ---
    m1 = p1['extra'].get('major', '')
    m2 = p2['extra'].get('major', '')
    if m1 and m2 and m1 != 'none' and m1 == m2:
        score += 2.0
        reasons.append(f"Same major ({m1.title()})")

    # --- Interest ---
    i1 = p1['extra'].get('interest', '')
    i2 = p2['extra'].get('interest', '')
    if i1 and i2 and i1 == i2:
        score += 1.5
        reasons.append(f"Shared interest in {i1}")

    # --- State ---
    s1 = p1['extra'].get('state', '')
    s2 = p2['extra'].get('state', '')
    if s1 and s2 and s1 == s2:
        score += 1.0
        reasons.append(f"Same state ({s1.upper()})")

    # --- Area code ---
    ac1 = get_area_code(p1.get('phone', ''))
    ac2 = get_area_code(p2.get('phone', ''))
    if ac1 and ac2 and ac1 == ac2:
        score += 1.0
        reasons.append(f"Same area code ({ac1})")

    # --- Email domain ---
    ed1 = get_email_domain(p1.get('email', ''))
    ed2 = get_email_domain(p2.get('email', ''))
    if ed1 and ed2 and ed1 == ed2:
        score += 0.5
        reasons.append(f"Same email domain ({ed1})")

    # --- Age proximity ---
    y1 = get_birth_year(p1.get('birthdate', ''))
    y2 = get_birth_year(p2.get('birthdate', ''))
    if y1 and y2:
        age_diff = abs(y1 - y2)
        if age_diff <= 5:
            score += 1.0
            reasons.append(f"Close in age (within {age_diff} years)")
        elif age_diff <= 10:
            score += 0.5
            reasons.append(f"Somewhat close in age (within {age_diff} years)")

    normalized = round(score / MAX_SCORE, 4)
    return normalized, reasons


# ─────────────────────────────────────────────
#  4. RECOMMENDATION ENGINE
# ─────────────────────────────────────────────

def recommend(people, target_fname, target_lname, top_n=3):
    """
    Given a target person (by first+last name), returns the top_n
    most similar people from the network (excluding themselves).
    """
    # Find the target person
    target = None
    for p in people:
        if p['fname'].lower() == target_fname.lower() and \
           p['lname'].lower() == target_lname.lower():
            target = p
            break

    if target is None:
        return None, []

    # Score everyone else
    scored = []
    for p in people:
        if p is target:
            continue
        sim, reasons = compute_similarity(target, p)
        scored.append((sim, reasons, p))

    # Sort by similarity descending
    scored.sort(key=lambda x: x[0], reverse=True)

    return target, scored[:top_n]


# ─────────────────────────────────────────────
#  5. DISPLAY
# ─────────────────────────────────────────────

def print_person_summary(p):
    code = get_code_name(p['fname'], p['lname'])
    print(f"  {p['lname']}, {p['fname']}  [{code}]")
    print(f"  Birthdate : {p['birthdate']}")
    print(f"  Phone     : {p.get('phone', 'N/A')}")
    print(f"  Email     : {p.get('email', 'N/A')}")
    for k, v in p['extra'].items():
        print(f"  {k.capitalize():<10}: {v.title()}")


def print_recommendations(target, results):
    print("\n" + "=" * 50)
    print("  TARGET PERSON")
    print("=" * 50)
    print_person_summary(target)

    print("\n" + "=" * 50)
    print(f"  TOP {len(results)} RECOMMENDED CONNECTIONS")
    print("=" * 50)

    for rank, (sim, reasons, p) in enumerate(results, 1):
        print(f"\n  #{rank}  Similarity Score: {sim:.2%}")
        print_person_summary(p)
        print("  Why recommended:")
        for r in reasons:
            print(f"    - {r}")

    print("\n" + "=" * 50)


# ─────────────────────────────────────────────
#  6. MAIN MENU
# ─────────────────────────────────────────────

def main():
    DB_FILE = "networkDB_phase3.txt"

    print("\n" + "=" * 50)
    print("   EE355 TROJANBOOK - Phase 3 Recommender")
    print("=" * 50)

    # Load database
    try:
        people = parse_database(DB_FILE)
    except FileNotFoundError:
        print(f"Error: '{DB_FILE}' not found. Make sure it's in the same folder.")
        return

    print(f"\nLoaded {len(people)} people from {DB_FILE}\n")

    while True:
        print("\nOptions:")
        print("  1. Get friend recommendations for a person")
        print("  2. Show all people in database")
        print("  3. Show similarity between two people")
        print("  4. Quit")
        choice = input("\nSelect an option: ").strip()

        # ── Option 1: Recommend ──────────────────────────
        if choice == '1':
            print("\nEnter the person you want recommendations for:")
            fname = input("  First Name: ").strip()
            lname = input("  Last Name : ").strip()

            try:
                top_n = int(input("  How many recommendations? (default 3): ").strip() or "3")
            except ValueError:
                top_n = 3

            target, results = recommend(people, fname, lname, top_n)

            if target is None:
                print(f"\nPerson '{fname} {lname}' not found in database.")
            else:
                print_recommendations(target, results)

        # ── Option 2: List all people ────────────────────
        elif choice == '2':
            print("\n" + "-" * 40)
            for p in people:
                code = get_code_name(p['fname'], p['lname'])
                print(f"  {p['lname']}, {p['fname']}  [{code}]")
            print("-" * 40)

        # ── Option 3: Compare two people ─────────────────
        elif choice == '3':
            print("\nPerson 1:")
            fname1 = input("  First Name: ").strip()
            lname1 = input("  Last Name : ").strip()
            print("Person 2:")
            fname2 = input("  First Name: ").strip()
            lname2 = input("  Last Name : ").strip()

            p1 = next((p for p in people if p['fname'].lower() == fname1.lower()
                        and p['lname'].lower() == lname1.lower()), None)
            p2 = next((p for p in people if p['fname'].lower() == fname2.lower()
                        and p['lname'].lower() == lname2.lower()), None)

            if p1 is None:
                print(f"Person '{fname1} {lname1}' not found.")
            elif p2 is None:
                print(f"Person '{fname2} {lname2}' not found.")
            else:
                sim, reasons = compute_similarity(p1, p2)
                print(f"\nSimilarity between {p1['fname']} {p1['lname']} "
                      f"and {p2['fname']} {p2['lname']}: {sim:.2%}")
                if reasons:
                    print("Shared attributes:")
                    for r in reasons:
                        print(f"  - {r}")
                else:
                    print("  No significant shared attributes found.")

        # ── Option 4: Quit ───────────────────────────────
        elif choice == '4':
            print("\nGoodbye!\n")
            break

        else:
            print("Invalid option. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
