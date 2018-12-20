from flask import Flask
from flask_cors import CORS

from src.common.database import Database
<<<<<<< HEAD
from src.models.Inspection.inspection_views import inspection_bp
=======
>>>>>>> 2c6c81573d291e45e059fc6c4a871787a23ebd60
from src.models.item.item_view import item_bp

from src.models.views import view_bp
from src.models.user.user_views import user_bp

app = Flask(__name__)
CORS(app)
app.secret_key = "Jimmy"

@app.before_first_request
def init():
  Database.go()


app.register_blueprint(view_bp)
app.register_blueprint(user_bp, url_prefix='/auth')
app.register_blueprint(item_bp, url_prefix="/lostAndFound")
<<<<<<< HEAD
app.register_blueprint(inspection_bp, url_prefix="/inspection")
=======
>>>>>>> 2c6c81573d291e45e059fc6c4a871787a23ebd60

if __name__ == '__main__':
    app.run(debug=True)
