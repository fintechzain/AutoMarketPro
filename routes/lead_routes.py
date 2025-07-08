from flask import Blueprint, render_template

lead_bp = Blueprint("lead_bp", __name__)

@lead_bp.route("/", methods=["GET"])
def lead_tool():
    return render_template("lead_manager.html")
