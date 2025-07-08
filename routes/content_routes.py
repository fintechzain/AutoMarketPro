from flask import Blueprint, render_template, request, flash
from utils.gpt_utils import generate_content

content_bp = Blueprint("content_bp", __name__)

@content_bp.route("/", methods=["GET", "POST"])
def content_generator():
    generated = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        tone = request.form["tone"]
        audience = request.form["audience"]
        platform = request.form["platform"]

        final_prompt = f"Write a {tone} {platform} post for {audience} about: {prompt}"
        generated = generate_content(final_prompt)

        if not generated:
            flash("Something went wrong with GPT!", "danger")
        else:
            flash("Content generated successfully!", "success")

    return render_template("content_generator.html", result=generated)
