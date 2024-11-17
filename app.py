from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from api import api  # Ваш файл api.py
from models import db  # Ваш файл models.py
from models import Car

# Создание приложения Flask
app = Flask(__name__)

# Настройки приложения
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = '12345678'  # Для безопасности сессии

# Инициализация расширений
db.init_app(app)  # Связываем SQLAlchemy с Flask
migrate = Migrate(app, db)  # Связываем Flask-Migrate
Session(app)  # Инициализируем Flask-Session

# Создаем все таблицы, если они не существуют
with app.app_context():
    db.create_all()


# Регистрация Blueprint для API
app.register_blueprint(api, url_prefix='/api')


# Маршруты для страниц
@app.route('/')
def home():
    cars = Car.query.all()  # Получение всех машин из базы данных
    cars_list = [{"make": car.make, "model": car.model, "year": car.year, "price": car.price, "image": car.image} for car in cars]
    return render_template('index.html', cars=cars_list)


@app.route('/view_cars')
def view_cars():
    return render_template('view_cars.html')

@app.route('/add_car_form')
def add_car_form():
    # Отображение формы добавления машины
    return render_template('add_car.html')

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
