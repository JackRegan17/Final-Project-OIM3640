# app/services.py
import requests
import pandas as pd
from typing import List, Optional, Dict

MLB_SEARCH_URL = "https://statsapi.mlb.com/api/v1/people/search"
MLB_STATS_URL = "https://statsapi.mlb.com/api/v1/people/{player_id}/stats"
MLB_PEOPLE_URL = "https://statsapi.mlb.com/api/v1/people/{player_id}"


# -----------------------------------------------------------
# SEARCH PLAYERS BY NAME
# -----------------------------------------------------------
def search_players_by_name(name: str) -> List[Dict]:
    """
    Search MLB players by name.
    Returns a list of dicts containing minimal metadata.
    """
    params = {"names": name}
    resp = requests.get(MLB_SEARCH_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    results = []
    for p in data.get("people", []):
        results.append({
            "id": p.get("id"),
            "fullName": p.get("fullName"),
            "currentTeam": p.get("currentTeam", {}).get("name") if p.get("currentTeam") else None
        })

    return results


# -----------------------------------------------------------
# FETCH STATS
# -----------------------------------------------------------
def fetch_player_stats(player_id: int, scope: str = "career", season: Optional[int] = None) -> Optional[pd.DataFrame]:
    """
    Fetch hitting stats for a player.
    """
    params = {
        "stats": scope,
        "group": "hitting"
    }
    if scope == "season" and season:
        params["season"] = season

    resp = requests.get(MLB_STATS_URL.format(player_id=player_id), params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    stats_list = data.get("stats", [])
    if not stats_list:
        return None

    splits = stats_list[0].get("splits", [])
    if not splits:
        return None

    stat_dict = splits[0].get("stat", {})
    if not stat_dict:
        return None

    df = pd.DataFrame([stat_dict])
    df.insert(0, "player_id", player_id)
    return df


# -----------------------------------------------------------
# PLAYER METADATA
# -----------------------------------------------------------
def get_player_metadata(player_id: int) -> Dict:
    """
    Returns base metadata: fullName, position, team name, teamId
    """
    resp = requests.get(MLB_PEOPLE_URL.format(player_id=player_id), timeout=10)
    resp.raise_for_status()
    data = resp.json()

    people = data.get("people", [])
    if not people:
        return {}

    p = people[0]

    return {
        "id": p.get("id"),
        "fullName": p.get("fullName"),
        "primaryPosition": p.get("primaryPosition", {}).get("abbreviation"),
        "currentTeam": p.get("currentTeam", {}).get("name") if p.get("currentTeam") else None,
        "teamId": p.get("currentTeam", {}).get("id") if p.get("currentTeam") else None,
    }


# -----------------------------------------------------------
# TEAM LOGO
# -----------------------------------------------------------

def construct_team_logo_url(team_id: int) -> str:
    """
    Returns the MLB team logo in SVG format.
    Uses MLB's team-cap-on-dark logo variant.
    """
    return f"https://www.mlbstatic.com/team-logos/team-cap-on-dark/{team_id}.svg"