import json # A built-in Python library for working with JSON data

# The name of our data file
FILE_NAME = 'leaders.json'

def update_leaders():
    """
    This is the main function of our scraper.
    For now, it just adds a new, hardcoded leader to our list.
    """
    print("Starting the leader update process...")

    # --- 1. Read existing data ---
    # We open the leaders.json file and load its contents into a Python list.
    try:
        with open(FILE_NAME, 'r') as f:
            leaders_list = json.load(f)
        print(f"Successfully loaded {len(leaders_list)} leaders from {FILE_NAME}.")
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty list
        leaders_list = []
        print(f"{FILE_NAME} not found. Starting with an empty list.")

    # --- 2. Add a new leader (our "scraping" for now) ---
    # In the future, this section will contain the code to find new leaders online.
    # For now, we'll add Sam Altman as an example.
    new_leader = {
        "id": "sam-altman",
        "name": "Sam Altman",
        "region": "USA",
        "current_role": {
          "title": "CEO",
          "company": "OpenAI"
        },
        "skills": ["GenAI", "Startups", "Investment"],
        "latest_activity": [],
        "profile_image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Sam_Altman_Official_Portrait.jpg/640px-Sam_Altman_Official_Portrait.jpg"
    }

    # Let's check if this leader already exists before adding them
    is_already_added = any(leader['id'] == new_leader['id'] for leader in leaders_list)

    if not is_already_added:
        print(f"Adding a new leader: {new_leader['name']}.")
        leaders_list.append(new_leader)
    else:
        print(f"Leader {new_leader['name']} is already in the list. No changes made.")


    # --- 3. Write the updated data back to the file ---
    # We open the file in "write" mode ('w') and save our updated list back to it.
    # The 'indent=4' makes the file nicely formatted and easy to read.
    with open(FILE_NAME, 'w') as f:
        json.dump(leaders_list, f, indent=4)

    print(f"Process finished. Total leaders in file: {len(leaders_list)}.")

# This is the standard Python way to make a script runnable
if __name__ == "__main__":
    update_leaders()
