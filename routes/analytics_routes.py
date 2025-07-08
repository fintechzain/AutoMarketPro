from flask import Blueprint, render_template, request, flash
import pandas as pd
import os
import matplotlib.pyplot as plt
from utils.gpt_utils import generate_content


analytics_bp = Blueprint("analytics_bp", __name__)
UPLOAD_FOLDER = "data/uploads"
PLOT_PATH = "static/analytics_plot.png"

@analytics_bp.route("/", methods=["GET", "POST"])
def analytics_tool():
    summary = None
    plot_url = None
    ai_insights = None
    top_platform_stats = None

    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            df = pd.read_csv(filepath)

            # Get platform with highest likes, views, clicks
            top_likes_platform = df.loc[df['likes'].idxmax(), 'platform']
            top_likes_value = df['likes'].max()

            top_views_platform = df.loc[df['views'].idxmax(), 'platform']
            top_views_value = df['views'].max()

            top_clicks_platform = df.loc[df['clicks'].idxmax(), 'platform']
            top_clicks_value = df['clicks'].max()

            top_platform_stats = [
                {"metric": "Most Likes", "platform": top_likes_platform, "value": top_likes_value},
                {"metric": "Most Views", "platform": top_views_platform, "value": top_views_value},
                {"metric": "Most Clicks", "platform": top_clicks_platform, "value": top_clicks_value},
            ]

            # Basic Summary
            numeric_df = df.select_dtypes(include='number')
            summary = numeric_df.agg(['mean', 'min', 'max']).T
            summary.columns = ['Mean', 'Min', 'Max']
            summary = summary.round(2)

            # Plot - Example: likes per platform
            if "platform" in df.columns and "likes" in df.columns:
                plt.figure(figsize=(8, 4))
                df.groupby("platform")["likes"].sum().plot(kind="bar")
                plt.title("Total Likes by Platform")
                plt.ylabel("Likes")
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(PLOT_PATH)
                plot_url = PLOT_PATH

            # AI Summary
            insight_prompt = f"Analyze this data and give high-level marketing insights:\n{df.head(10).to_string()}"
            ai_insights = generate_content(insight_prompt)

            flash("Analytics generated!", "success")

    return render_template(
        "analytics_dashboard.html",
        summary=summary,
        plot_url=plot_url,
        ai_insights=ai_insights,
        top_platform_stats=top_platform_stats
    )

