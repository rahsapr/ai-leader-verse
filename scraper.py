import os
import json
from serpapi import GoogleSearch

FILE_NAME = 'leaders.json'
SEARCH_QUERIES = [
    "CEO of top Generative AI startups",
    "leading researchers in Agentic AI",
    "founders of major LLM companies"
]

def search_for_new_leaders():
    """
    Performs Google searches to discover potential new leaders.
    Returns a list of potential leaders with their name and company.
    """
    print("Searching for new leaders...")
    potential_leaders = []
    api_key = os.getenv("SERPAPI_API_KEY")

    if not api_key:
        print("Error: SERPAPI_API_KEY not found. Stopping scraper.")
        return []

    for query in SEARCH_QUERIES:
        print(f"Running search query: '{query}'")
        search = GoogleSearch({
            "q": query,
            "api_key": api_key
        })
        results = search.get_dict()

        # Try to extract names from "organic_results"
        if 'organic_results' in results:
            for result in results.get('organic_results', []):
                # Simple logic: if a title contains " - " or " | ", split it.
                # This is a basic way to find "Name - Company". It can be improved later.
                if 'title' in result:
                    parts = result['title'].replace(' | ', ' - ').split(' - ')
                    if len(parts) >= 2:
                        name = parts[0].strip()
                        company = parts[1].strip()
                        # Basic filter to avoid generic results
                        if len(name.split()) > 1 and len(name.split()) < 4:
                            potential_leaders.append({"name": name, "company": company})

    print(f"Found {len(potential_leaders)} potential new leaders from searches.")
    return potential_leaders

def get_latest_activity(leader_name):
    """
    Searches for the latest news about a leader.
    For now, returns a placeholder. We will build this out later.
    """
    # Placeholder - In a future step we could scrape news sites here.
    return [{
        "title": f"Recent news about {leader_name}",
        "url": "#",
        "source": "News Aggregator",
        "date": "2025-01-01"
    }]


def update_leaders():
    """
    Main function to orchestrate the update process.
    """
    print("Starting the leader update process...")

    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            existing_leaders = json.load(f)
    except FileNotFoundError:
        existing_leaders = []
    
    existing_ids = {leader.get('id', '') for leader in existing_leaders}
    print(f"Loaded {len(existing_leaders)} existing leaders.")

    newly_found_leaders = search_for_new_leaders()
    leaders_to_add = []

    for leader in newly_found_leaders:
        leader_id = leader['name'].lower().replace(' ', '-')
        if leader_id not in existing_ids:
            print(f"New unique leader found: {leader['name']}. Preparing to add.")
            leaders_to_add.append({
                "id": leader_id,
                "name": leader['name'],
                "region": "Unknown", # We can try to determine this later
                "current_role": {
                    "title": "Unknown",
                    "company": leader['company']
                },
                "skills": ["GenAI"], # Default skill
                "latest_activity": get_latest_activity(leader['name']),
                "profile_image_url": "https://via.placeholder.com/100" # Placeholder image
            })
            # Add to existing_ids immediately to prevent duplicates from the same run
            existing_ids.add(leader_id)

    if not leaders_to_add:
        print("No new leaders to add. The list is up to date.")
        return

    print(f"Adding {len(leaders_to_add)} new leaders to the list.")
    all_leaders = existing_leaders + leaders_to_add

    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(all_leaders, f, indent=4, ensure_ascii=False)

    print(f"Process finished. Total leaders in file: {len(all_leaders)}.")


if __name__ == "__main__":
    update_leaders()
