from flask import Flask, render_template
from dotenv import load_dotenv
from automarketpro.routes.email_routes import email_bp
from automarketpro.routes.analytics_routes import analytics_bp
from automarketpro.routes.content_routes import content_bp
from automarketpro.routes.lead_routes import lead_bp
from automarketpro.routes.poster_routes import poster_bp
from automarketpro.routes.persona_routes import persona_bp
from automarketpro.routes.repurpose_routes import repurposer_bp
from automarketpro.routes.coach_routes import coach_bp
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev")

# Register Blueprints
app.register_blueprint(email_bp, url_prefix="/email")
app.register_blueprint(analytics_bp, url_prefix="/analytics")
app.register_blueprint(content_bp, url_prefix="/content")
app.register_blueprint(lead_bp, url_prefix="/leads")
app.register_blueprint(poster_bp, url_prefix="/poster")
app.register_blueprint(persona_bp, url_prefix="/persona")
app.register_blueprint(repurposer_bp, url_prefix="/repurpose")

app.register_blueprint(coach_bp, url_prefix="/coach")

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
