from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from config import Config
from db import get_db_connection
from auth import auth_bp
from partners import partners_bp
from requests import requests_bp
from supplies import supplies_bp
from products import products_bp
from materials import materials_bp
from upload import upload_bp
from calc import calc_bp
from users import users_bp
from models import User
import logging

app = Flask(__name__)
app.config.from_object(Config)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    conn, db_status = get_db_connection()
    if not conn:
        logger.error(f"Ошибка загрузки пользователя: {db_status['message']}")
        return None
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT UserID, Username, Email, Role, PartnerID FROM Users WHERE UserID = %s", (user_id,))
        user = cursor.fetchone()
        if user:
            return User(user[0], user[1], user[2], user[3], user[4])
        return None
    finally:
        cursor.close()
        conn.close()

# Регистрация Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(partners_bp)
app.register_blueprint(requests_bp)
app.register_blueprint(supplies_bp)
app.register_blueprint(products_bp)
app.register_blueprint(materials_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(calc_bp)
app.register_blueprint(users_bp)

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    conn, db_status = get_db_connection()
    partners = []
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT PartnerID, Name FROM Partners")
            partners = cursor.fetchall()
        except Exception as e:
            logger.error(f"Ошибка при получении списка партнёров: {str(e)}")
            db_status = {'status': 'error', 'message': str(e)}
        finally:
            cursor.close()
            conn.close()
    return render_template('index.html', db_status=db_status, partners=partners)

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

if __name__ == '__main__':
    app.run(debug=True)