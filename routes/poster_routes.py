from flask import Blueprint, render_template, request, redirect, url_for, flash
import json, os
from datetime import datetime
from werkzeug.utils import secure_filename

poster_bp = Blueprint("poster_bp", __name__)
POST_DB = "data/exports/scheduled_posts.json"
UPLOAD_DIR = "static/uploads"

@poster_bp.route("/", methods=["GET", "POST"])
def auto_poster():
    if request.method == "POST":
        content = request.form["content"]
        platform = request.form["platform"]
        schedule_time = request.form["schedule_time"]

        image_file = request.files["image"]
        image_path = None

        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            image_path = os.path.join(UPLOAD_DIR, filename)
            image_file.save(image_path)
            image_name = filename
        else:
            image_name = ""

        post = {
            "content": content,
            "platform": platform,
            "schedule_time": schedule_time,
            "image": image_name
        }

        posts = []
        if os.path.exists(POST_DB):
            with open(POST_DB, "r") as f:
                posts = json.load(f)

        posts.append(post)

        with open(POST_DB, "w") as f:
            json.dump(posts, f, indent=4)

        flash("Post scheduled successfully!", "success")
        return redirect(url_for("poster_bp.auto_poster"))

    # Show existing scheduled posts
    if os.path.exists(POST_DB):
        with open(POST_DB, "r") as f:
            posts = json.load(f)
    else:
        posts = []

    return render_template("auto_poster.html", posts=posts)
