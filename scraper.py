import os
import json
import csv
import re
from serpapi import GoogleSearch

LEADERS_FILE = 'leaders.json'
SEED_FILE = 'seed_leaders.csv'

# --- Using the new, more direct search queries as you suggested ---
SEARCH_QUERIES = [
    "list of top 100 generative AI leaders",
    "most influential generative AI researchers 2025",
    "founders and CEOs of top AI startups list"
]

def load_existing_leaders():
    """Loads leaders from the JSON file and returns the list and a set of IDs for fast lookups."""
    try:
        with open(LEADERS_FILE, 'r', encoding='utf-8') as f:
            existing_leaders = json.load(f)
        existing_ids = {leader.get('id', '') for leader in existing_leaders}
        print(f"Loaded {len(existing_leaders)} existing leaders.")
        return existing_leaders, existing_ids
    except FileNotFoundError:
        print("leaders.json not found. Starting with an empty list.")
        return [], set()

def process_seed_file(existing_ids):
    """Reads the seed_leaders.csv file and returns a list of new leaders to be added."""
    new_leaders_from_seed = []
    try:
        with open(SEED_FILE, 'r', encoding='utf-8') as f:
            # Using DictReader to easily access columns by name ('name', 'company')
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get('name', '').strip()
                company = row.get('company', '').strip()
                if not name: # Skip empty rows
                    continue
                
                leader_id = name.lower().replace(' ', '-')
                if leader_id not in existing_ids:
                    print(f"[Seed] Found new leader from CSV: {name}")
                    new_leaders_from_seed.append({
                        "id": leader_id,
                        "name": name,
                        "current_role": {"company": company or "Unknown"}
                    })
                    existing_ids.add(leader_id) # Add to set to avoid duplicates in the same run
        
        # Optional: Clear the seed file after processing so it doesn't run every time
        # with open(SEED_FILE, 'w', newline='') as f:
        #     writer = csv.writer(f)
        #     writer.writerow(['name', 'company'])
        # print("Seed file has been processed and cleared.")

    except FileNotFoundError:
        print("No seed_leaders.csv file found. Skipping manual input.")
    return new_leaders_from_seed

def search_for_new_leaders(existing_ids):
    """Performs Google searches using smarter queries and parsing to find new leaders."""
    print("\nStarting automated search for new leaders...")
    potential_leaders = []
    api_key = os.getenv("SERPAPI_API_KEY")

    if not api_key:
        print("Error: SERPAPI_API_KEY not found. Stopping automated search.")
        return []

    for query in SEARCH_QUERIES:
        print(f"Running search query: '{query}'")
        try:
            search = GoogleSearch({"q": query, "api_key": api_key, "num": "20"}) # Ask for more results
            results = search.get_dict().get('organic_results', [])

            for result in results:
                text_to_search = f"{result.get('title', '')} {result.get('snippet', '')}"
                
                # Smarter pattern matching for names
                found_names = re.findall(r'([A-Z][a-z]+(?:\s[A-Z][a-z\'-]+)+)', text_to_search)

                if found_names:
                    for name in found_names:
                        # Filter out things that are clearly not names
                        if len(name.split()) > 1 and len(name.split()) < 5 and " " in name:
                            leader_id = name.strip().lower().replace(' ', '-')
                            if leader_id not in existing_ids:
                                print(f"[Search] Found potential new leader: {name}")
                                potential_leaders.append({"id": leader_id, "name": name, "current_role": {"company": "Unknown"}})
                                existing_ids.add(leader_id)
        except Exception as e:
            print(f"An error occurred during search: {e}")
    
    return potential_leaders

def update_leader_list():
    """Main function to orchestrate the entire update process."""
    all_leaders, existing_ids = load_existing_leaders()
    
    # 1. Process the manual seed file first
    new_leaders = process_seed_file(existing_ids)
    
    # 2. Run the automated search for more leaders
    new_leaders.extend(search_for_new_leaders(existing_ids))

    if not new_leaders:
        print("\nProcess finished. No new leaders were added.")
        return

    print(f"\nFound a total of {len(new_leaders)} new leaders to add.")
    
    # 3. Enrich and format the new leader data
    for leader in new_leaders:
        leader['region'] = 'Unknown'
        leader.setdefault('current_role', {}).setdefault('title', 'Unknown')
        leader['skills'] = ['GenAI']
        leader['latest_activity'] = []
        leader['profile_image_url'] = "https://via.placeholder.com/100"

    # 4. Combine and save the final list
    final_leader_list = all_leaders + new_leaders
    with open(LEADERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_leader_list, f, indent=4, ensure_ascii=False)

    print(f"Successfully updated leaders.json. Total leaders: {len(final_leader_list)}.")


if __name__ == "__main__":
    update_leader_list()
