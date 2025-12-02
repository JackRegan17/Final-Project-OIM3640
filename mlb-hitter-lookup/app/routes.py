from flask import Blueprint, render_template, request
from .services import fetch_player_stats
import pandas as pd

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@main.route("/player", methods=["POST"])
def player():
    player_name = request.form.get("player_name")

    # Fetch data from services
    result = fetch_player_stats(player_name)

    if result is None:
        return render_template("player.html", error="Player not found.")

    # Convert stats dict → DataFrame so we can use to_html()
    df = pd.DataFrame([result["stats"]])
    html_table = df.to_html(classes="table table-striped table-bordered", border=0)

    return render_template(
        "player.html",
        player=result["player_name"],
        table=html_table,
    )


