from flask import Flask
from flask_cors import CORS
from src.common.database import Database
from src.models.home.home_view import home_bp
from src.models.trial.trial_view import trial_bp
from src.models.trial.trial_status_view import trial_status_bp
from src.models.item.item_view import item_bp
from src.models.user.user_views import user_bp
from src.models.inventoryItem.inventoryItem_view import inventory_bp

app = Flask(__name__)
CORS(app)
app.secret_key = "Jimmy"

@app.before_first_request
def init():
    Database.go()

app.register_blueprint(home_bp)
app.register_blueprint(trial_bp)
app.register_blueprint(trial_status_bp, url_prefix="/statusChange")
app.register_blueprint(item_bp, url_prefix="/lostAndFound")
app.register_blueprint(user_bp, url_prefix="/login")
app.register_blueprint(inventory_bp, url_prefix="/inventory")

if __name__ == '__main__':
    app.run()
