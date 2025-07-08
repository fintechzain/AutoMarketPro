from flask import Blueprint, render_template, request, flash, redirect, url_for
from utils.email_utils import send_bulk_emails
import os
import csv
from werkzeug.utils import secure_filename
import re


email_bp = Blueprint("email_bp", __name__)

UPLOAD_FOLDER = "data/uploads"
ALLOWED_EXTENSIONS = {"csv"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@email_bp.route("/", methods=["GET", "POST"])
def email_tool():
    if request.method == "POST":
        subject = request.form["subject"]
        message = request.form["message"]
        sender_email = request.form["sender_email"]
        sender_password = request.form["sender_password"]
        pasted_emails = request.form.get("pasted_emails")

        recipients = []

        manual_emails = request.form.get("manual_emails", "")
        if manual_emails.strip():
            recipients += [email.strip() for email in re.split(r'[,\n]', manual_emails) if email.strip()]

        file = request.files.get("csv_file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            with open(filepath, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                recipients += [row["email"].strip() for row in reader if "email" in row]

        if not recipients:
            flash("Please provide emails via textbox or upload a CSV file.", "danger")
            return redirect(url_for("email_bp.email_tool"))

        # Send emails
        success = send_bulk_emails(subject, message, sender_email, sender_password, recipients)
        if success:
            flash("Emails sent successfully!", "success")
        else:
            flash("Failed to send emails. Check credentials or file format.", "danger")
        return redirect(url_for("email_bp.email_tool"))

    return render_template("email_tool.html")
