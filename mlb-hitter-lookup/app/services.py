import requests

def fetch_player_stats(player_name: str):
    """
    Fetches player stats from MLB Stats API by player name.
    Returns a dict or None if player not found.
    """

    # --- 1️⃣ Search for the player ID ---
    search_url = "https://statsapi.mlb.com/api/v1/people/search"
    search_params = {"names": player_name}

    search_response = requests.get(search_url, params=search_params)
    search_data = search_response.json()

    # No players found
    if "people" not in search_data or len(search_data["people"]) == 0:
        return None

    player_id = search_data["people"][0]["id"]

    # --- 2️⃣ Fetch stats for that player ---
    stats_url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats"
    stats_params = {
        "stats": "career",
        "group": "hitting"
    }

    stats_response = requests.get(stats_url, params=stats_params)
    stats_data = stats_response.json()

    # No stats available
    if "stats" not in stats_data or len(stats_data["stats"]) == 0:
        return None

    splits = stats_data["stats"][0].get("splits", [])
    if len(splits) == 0:
        return None

    # Return the FIRST split, which contains the numbers
    return {
        "player_name": player_name.title(),
        "id": player_id,
        "stats": splits[0]["stat"]
    }

