from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from api import api
# app.py
from models import db  # Убедитесь, что models.py содержит определение db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Замените на ваш собственный ключ

db.init_app(app)  # Используем существующий экземпляр
migrate = Migrate(app, db)
jwt = JWTManager(app)  # Инициализация JWTManager с вашим приложением

with app.app_context():
    db.create_all()  # Создание всех таблиц


# Регистрация Blueprint для API
app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/view_cars')
def view_cars():
    return render_template('view_cars.html')


if __name__ == '__main__':
    app.run(debug=True)
