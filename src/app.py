from src.main import app, socketio

from src.models.Inspection.inspection_views import inspection_bp
from src.models.inventoryItem.inventoryItem_view import inventory_bp
from src.models.item.item_view import item_bp
from src.models.user.user_views import user_bp
from src.models.views import view_bp

app.register_blueprint(view_bp)
app.register_blueprint(user_bp, url_prefix='/auth')
app.register_blueprint(item_bp, url_prefix="/lostAndFound")
app.register_blueprint(inspection_bp, url_prefix="/inspection")
app.register_blueprint(inventory_bp, url_prefix="/inventory")


@socketio.on('msg')
def handle_msg(msg):
    print('received msg: ' + msg)


if __name__ == '__main__':
    socketio.run(app)
