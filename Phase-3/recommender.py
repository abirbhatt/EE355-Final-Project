"""
EE355 Phase 3 - Friend Recommendation System
Content-based filtering using person attributes from networkDB_phase3.txt
"""

import re
from datetime import datetime


#first go through the data base

def search_database(filename):
    """
    read the database of people from networkDB_phase3.txt text file and then
    return back a list of dictionaries for each person. 
    includes: first name, last name, birth date, email, phone, and any other
    key-value attributes 
    """
    people = []

    with open(filename, 'r') as f:
        content = f.read()

    blocks = re.split(r'-{4,}', content)
    for block in blocks:
        lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
        if len(lines) < 5:
            continue  # skip the incomplete blocks

        person = {}
        person['first_name'] = lines[0]
        person['last_name']  = lines[1]
        person['birthday']   = lines[2]

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
                colon_index = line.index(':')
                key = line[:colon_index]
                val = line[colon_index + 1:]
                person['extra'][key.strip().lower()] = val.strip().lower()                

        people.append(person)

    return people


#helpful features to extract data from database 

def get_birth_year(bdate_str):
    """Parse birth year from M/D/YYYY or MM/DD/YYYY string."""
    try:
        parts = bdate_str.split('/')
        return int(parts[2])
    except Exception:
        return None


def get_area_code(phone_str):
    #extracting the 3 digit area code from phone numbers 
    digits = ""
    for ch in phone_str:
        if ch.isdigit():
            digits += ch
    if len(digits) >= 3:
        return digits[:3]
    return None


def get_email_domain(email_str):
    #extracting the domain by looking at email handles after the "@" symbol in emails 
    if '@' in email_str:
        return email_str.split('@')[1].lower()
    return None


def get_code_name(first_name, last_name):
    #create a unique id for each person
    return (first_name + last_name).replace(' ', '').lower()


#compute the similarity score 

def compute_similarity(p1, p2):
    """
    In this step we compute a similarity score from 0.0 to 1.0 between two people
    The more shared attributes there are between the two people the higher the score is
    and they are therefore recommended as a better match 

    Scoring breakdown (total possible = 9 points): 
      - Same college    = +2.0 pts
      - Same major      = +2.0 pts
      - Same interest   = +1.5 pts
      - Same state      = +1.0 pts
      - Same area code  = +1.0 pts   
      - Same email domain = +0.5 pts
      - Age within 5 years  = +1.0 pts 
      - Age within 10 years = +0.5 pts
    """
    max_score = 9.0  # sum of maximum possible points
    score = 0.0
    reasons = []

    # college
    c1 = p1['extra'].get('college', '')
    c2 = p2['extra'].get('college', '')
    if c1 and c2 and c1 != 'none' and c1 == c2:
        score += 2.0
        reasons.append(f"Same college ({c1.title()})")

    # major
    m1 = p1['extra'].get('major', '')
    m2 = p2['extra'].get('major', '')
    if m1 and m2 and m1 != 'none' and m1 == m2:
        score += 2.0
        reasons.append(f"Same major ({m1.title()})")

    # interest
    i1 = p1['extra'].get('interest', '')
    i2 = p2['extra'].get('interest', '')
    if i1 and i2 and i1 == i2:
        score += 1.5
        reasons.append(f"Shared interest in {i1}")

    # state
    s1 = p1['extra'].get('state', '')
    s2 = p2['extra'].get('state', '')
    if s1 and s2 and s1 == s2:
        score += 1.0
        reasons.append(f"Same state ({s1.upper()})")

    # area code
    ac1 = get_area_code(p1.get('phone', ''))
    ac2 = get_area_code(p2.get('phone', ''))
    if ac1 and ac2 and ac1 == ac2:
        score += 1.0
        reasons.append(f"Same area code ({ac1})")

    # email domain
    ed1 = get_email_domain(p1.get('email', ''))
    ed2 = get_email_domain(p2.get('email', ''))
    if ed1 and ed2 and ed1 == ed2:
        score += 0.5
        reasons.append(f"Same email domain ({ed1})")

    # age proximity
    y1 = get_birth_year(p1.get('birthday', ''))
    y2 = get_birth_year(p2.get('birthday', ''))
    if y1 and y2:
        age_diff = abs(y1 - y2)
        if age_diff <= 5:
            score += 1.0
            reasons.append(f"Close in age (within {age_diff} years)")
        elif age_diff <= 10:
            score += 0.5
            reasons.append(f"Somewhat close in age (within {age_diff} years)")

    normalized = score / max_score
    return normalized, reasons


# actually giving back the top recommended people 

def recommend(people, target_first_name, target_last_name, top_n=3):
    # take the target person and then return the top n most similar people from the database, not including themselves

    # find the target person
    target = None
    for p in people:
        if p['first_name'].lower() == target_first_name.lower() and \
           p['last_name'].lower() == target_last_name.lower():
            target = p
            break

    if target is None:
        return None, []

    # score everyone else
    scored = []
    for p in people:
        if p is target:
            continue
        sim, reasons = compute_similarity(target, p)
        scored.append((sim, reasons, p))

    # sort by similarity descending
    scored.sort(key=lambda x: x[0], reverse=True)
    for i in range (len(scored)):
        for j in range( i + 1, len(scored)):
            if scored[j][0] > scored[i][0]:
                scored[i], scored [j] = scored[j], scored[i]

    return target, scored[:top_n]


# find the shortest friendship path between two people using BFS

def find_path(people, start_first_name, start_last_name, end_first_name, end_last_name):
    """
    Finds the shortest friendship path between two people using BFS.
    Returns the start person, end person, and the path as a list of people.
    Returns an empty list if no path is found.
    """
    # find start and end person in the database
    start = None
    end = None
    for p in people:
        if p['first_name'].lower() == start_first_name.lower() and p['last_name'].lower() == start_last_name.lower():
            start = p
        if p['first_name'].lower() == end_first_name.lower() and p['last_name'].lower() == end_last_name.lower():
            end = p

    if start is None or end is None:
        return None, None, []

    # BFS - each item in the queue is a path (list of people) explored so far
    queue = [[start]]
    visited = set()
    visited.add(get_code_name(start['first_name'], start['last_name']))

    while queue:
        path = queue.pop(0)   # grab the next path to explore
        current = path[-1]    # look at the last person in the current path

        # get this person's friends as a list of code names
        friends_str = current['extra'].get('friends', '')
        if friends_str == '':
            continue
        friend_codes = [f.strip() for f in friends_str.split(',')]

        for code in friend_codes:
            # find the actual person object that matches this code name
            friend = None
            for p in people:
                if get_code_name(p['first_name'], p['last_name']) == code:
                    friend = p
                    break

            if friend is None:
                continue

            # check if we reached the end person
            if get_code_name(friend['first_name'], friend['last_name']) == get_code_name(end['first_name'], end['last_name']):
                return start, end, path + [friend]

            # otherwise add this friend to the queue to keep exploring
            if get_code_name(friend['first_name'], friend['last_name']) not in visited:
                visited.add(get_code_name(friend['first_name'], friend['last_name']))
                queue.append(path + [friend])

    return start, end, []  # no path found


# display results of the recommendation system 

def print_person_summary(p):
    code = get_code_name(p['first_name'], p['last_name'])
    print(f"  {p['last_name']}, {p['first_name']}  [{code}]")
    print(f"  Birthday  : {p['birthday']}")
    print(f"  Phone     : {p.get('phone', 'N/A')}")
    print(f"  Email     : {p.get('email', 'N/A')}")
    for k, v in p['extra'].items():
        if k != 'friends':  # don't print the raw friends line
            print(f"  {k.capitalize():}: {v.title()}")


def print_recommendations(target, results):
    print("\n" + "=" * 50)
    print("  TARGET PERSON")
    print("=" * 50)
    print_person_summary(target)

    print("\n" + "=" * 50)
    print(f"  TOP {len(results)} RECOMMENDED CONNECTIONS")
    print("=" * 50)

    for i in range(len(results)):
        sim = results[i][0]
        reasons = results[i][1]
        p = results[i][2]
        print(f"\n  #{i+1}  Similarity Score: {sim:.2%}")

        print_person_summary(p)
        print("  Why recommended:")
        for r in reasons:
            print(f"    - {r}")

    print("\n" + "=" * 50)


# main menu for user to navigate 

def main():
    DB_FILE = "networkDB_phase3.txt"

    print("\n" + "=" * 50)
    print("   EE355 TROJANBOOK - Phase 3 Recommender")
    print("=" * 50)

    # load database
    try:
        people = search_database(DB_FILE)
    except FileNotFoundError:
        print(f"Error: '{DB_FILE}' not found. Make sure it's in the same folder.")
        return

    print(f"\nLoaded {len(people)} people from {DB_FILE}\n")

    while True:
        print("\nOptions:")
        print("  1. Get friend recommendations for a person")
        print("  2. Display entire database list")
        print("  3. Show similarity score between two people")
        print("  4. Friendship Path Finder")
        print("  5. Quit")
        choice = input("\nSelect an option: ").strip()

        # recommend
        if choice == '1':
            print("\nWho do you want recommendations for?")
            first_name = input("  First Name: ").strip()
            last_name = input("  Last Name : ").strip()

            try:
                top_n = int(input("  How many recommendations do you want? (default 3): ").strip() or "3")
            except ValueError:
                top_n = 3

            target, results = recommend(people, first_name, last_name, top_n)

            if target is None:
                print(f"\nPerson '{first_name} {last_name}' not found in database.")
            else:
                print_recommendations(target, results)

        # list all people
        elif choice == '2':
            print("\n" + "-" * 40)
            for p in people:
                code = get_code_name(p['first_name'], p['last_name'])
                print(f"  {p['last_name']}, {p['first_name']}  [{code}]")
            print("-" * 40)

        # compare two people
        elif choice == '3':
            print("\nPerson 1:")
            first_name1 = input("  First Name: ").strip()
            last_name1 = input("  Last Name : ").strip()
            print("Person 2:")
            first_name2 = input("  First Name: ").strip()
            last_name2 = input("  Last Name : ").strip()

            p1 = None
            for p in people:
                if p['first_name'].lower() == first_name1.lower() and p['last_name'].lower() == last_name1.lower():
                    p1 = p
                    break

            p2 = None
            for p in people:
                if p['first_name'].lower() == first_name2.lower() and p['last_name'].lower() == last_name2.lower():
                    p2 = p
                    break

            if p1 is None:
                print(f"Person '{first_name1} {last_name1}' not found.")
            elif p2 is None:
                print(f"Person '{first_name2} {last_name2}' not found.")
            else:
                sim, reasons = compute_similarity(p1, p2)
                print(f"\nSimilarity between {p1['first_name']} {p1['last_name']} "
                      f"and {p2['first_name']} {p2['last_name']}: {sim:.2%}")
                if reasons:
                    print("Shared attributes:")
                    for r in reasons:
                        print(f"  - {r}")
                else:
                    print("  No significant shared attributes found.")

        # friendship path finder
        elif choice == '4':
            print("\nFriendship Path Finder")
            print("Find how two people are connected through friends.\n")
            print("Person 1:")
            first_name1 = input("  First Name: ").strip()
            last_name1 = input("  Last Name : ").strip()
            print("Person 2:")
            first_name2 = input("  First Name: ").strip()
            last_name2 = input("  Last Name : ").strip()

            start, end, path = find_path(people, first_name1, last_name1, first_name2, last_name2)

            if start is None:
                print(f"\nOne or both people not found in database.")
            elif len(path) == 0:
                print(f"\nNo connection found between {first_name1} {last_name1} and {first_name2} {last_name2}.")
            else:
                print(f"\nConnection found! Path length: {len(path) - 1} step(s)")
                print("\n  ", end="")
                for i, person in enumerate(path):
                    print(f"{person['first_name']} {person['last_name']}", end="")
                    if i < len(path) - 1:
                        print(" -> ", end="")
                print()

        # quit
        elif choice == '5':
            print("\nGoodbye!\n")
            break

        else:
            print("Invalid option. Please enter 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()

