from flask import Blueprint, render_template, request
from .services import lookup_player_basic

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@main_bp.route("/player", methods=["POST"])
def player_lookup():
    name = request.form.get("player_name")
    result = lookup_player_basic(name)
    return {"searched_for": name, "raw_result": result}
