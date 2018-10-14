from flask import Flask
import os

from src.common.database import Database
from src.models.home.home_view import home_bp
from src.models.HK_Views.HK_Main_View import hk_bp
from src.models.HK_Views.HK_Status_View import trial_status_bp
from src.models.item.item_view import item_bp
from src.models.user.user_views import user_bp
from src.models.inventoryItem.inventoryItem_view import inventory_bp

application = Flask(__name__)
application.secret_key = "Jimmy"

@application.before_first_request
def init():
    Database.go()

application.register_blueprint(home_bp)
application.register_blueprint(hk_bp)
application.register_blueprint(trial_status_bp, url_prefix="/statusChange")
application.register_blueprint(item_bp, url_prefix="/lostAndFound")
application.register_blueprint(user_bp, url_prefix="/login")
application.register_blueprint(inventory_bp, url_prefix="/inventory")

if __name__ == '__main__':
    application.run(debug=True, port=9000)
