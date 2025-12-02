# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for

from .services import (
    search_players_by_name,
    fetch_player_stats,
    get_player_metadata,
    construct_team_logo_url
)

main = Blueprint("main", __name__)

# ----------------------------------------------------
# HOME PAGE
# ----------------------------------------------------
@main.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# ----------------------------------------------------
# SEARCH HANDLER
# ----------------------------------------------------
@main.route("/player", methods=["POST"])
def player_search():
    player_name = request.form.get("player_name", "").strip()
    scope = request.form.get("scope", "career")
    season = request.form.get("season")
    season_int = int(season) if season and season.isdigit() else None

    if not player_name:
        return render_template("index.html", error="Please enter a player name.")

    matches = search_players_by_name(player_name)
    if not matches:
        return render_template("index.html", error="No matching players found.")

    # MULTIPLE MATCHES → let user choose
    if len(matches) > 1:
        return render_template(
            "select_player.html",
            matches=matches,
            original_query=player_name,
            scope=scope,
            season=season_int
        )

    # EXACT MATCH → redirect to stats page
    player_id = matches[0]["id"]
    return redirect(url_for(
        "main.player_by_id",
        player_id=player_id,
        scope=scope,
        season=season_int if season_int else ""
    ))


# ----------------------------------------------------
# MULTIPLE MATCH SELECTION FORM
# ----------------------------------------------------
@main.route("/player/select", methods=["POST"])
def player_selected():
    player_id = request.form.get("player_id")
    scope = request.form.get("scope", "career")
    season = request.form.get("season")

    if not player_id:
        return render_template("index.html", error="No player selected.")

    return redirect(url_for(
        "main.player_by_id",
        player_id=int(player_id),
        scope=scope,
        season=season if season else ""
    ))


# ----------------------------------------------------
# SINGLE PLAYER PAGE
# ----------------------------------------------------
@main.route("/player/<int:player_id>", methods=["GET"])
def player_by_id(player_id):
    scope = request.args.get("scope", "career")
    season = request.args.get("season")
    season_int = int(season) if season and season.isdigit() else None

    # Fetch hitting stats
    try:
        df = fetch_player_stats(player_id=player_id, scope=scope, season=season_int)
    except Exception as e:
        return render_template("player.html", error=f"Error fetching stats: {e}")

    if df is None or df.empty:
        return render_template("player.html", error="No stats available for this player/scope/season.")

    # Get player metadata
    meta = get_player_metadata(player_id)

    # TEAM LOGO
    team_logo = None
    team_id = meta.get("teamId")
    if team_id:
        team_logo = construct_team_logo_url(team_id)

    # Convert stats DF → dictionary
    stats_dict = df.iloc[0].to_dict()

    return render_template(
        "player.html",
        player=meta.get("fullName", f"Player {player_id}"),
        meta=meta,
        team_logo=team_logo,
        stats=stats_dict,
        scope=scope,
        season=season_int
    )



