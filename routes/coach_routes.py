from flask import Blueprint, render_template, request, flash
from utils.gpt_utils import generate_content

coach_bp = Blueprint("coach_bp", __name__)

@coach_bp.route("/", methods=["GET", "POST"])
def coach_tool():
    answer = None
    if request.method == "POST":
        question = request.form["question"]
        prompt = f"As a marketing expert, answer this question in detail:\n{question}"
        answer = generate_content(prompt)
        flash("Response generated!", "success")

    return render_template("coach.html", answer=answer)
