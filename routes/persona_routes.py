from flask import Blueprint, render_template, request, flash
from utils.gpt_utils import generate_persona

persona_bp = Blueprint("persona_bp", __name__)

@persona_bp.route("/", methods=["GET", "POST"])
def persona_tool():
    result = None
    if request.method == "POST":
        product = request.form["product"]
        industry = request.form["industry"]
        audience = request.form["audience"]

        prompt = (
            f"Create a detailed customer persona for a product like: '{product}', "
            f"in the industry: '{industry}', targeting: '{audience}'. "
            f"Include name, age, job, goals, challenges, buying triggers, and marketing tips."
        )

        result = generate_persona(prompt)
        flash("Persona generated!", "success")

    return render_template("persona_builder.html", result=result)
