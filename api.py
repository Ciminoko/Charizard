from flask import Blueprint, request, jsonify, send_from_directory, render_template, session
from werkzeug.utils import secure_filename
import os
from models import db, User, Car

api = Blueprint('api', __name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Регистрация
@api.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"error": "User already exists"}), 400

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201

    return render_template('register.html')

# Авторизация
@api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id  # Сохраняем ID пользователя в сессии
            return jsonify({"message": "Login successful", "user_id": user.id}), 200
        return jsonify({"error": "Invalid username or password"}), 401
    return render_template('login.html')

# Выход из аккаунта
@api.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"}), 200

# Получение всех машин
@api.route('/cars', methods=['GET'])
def get_all_cars():
    cars = Car.query.all()
    cars_list = [
        {"id": car.id, "make": car.make, "model": car.model, "year": car.year, "price": car.price, "image": car.image}
        for car in cars
    ]
    return jsonify(cars_list)

# Получение машин текущего пользователя
@api.route('/user/cars', methods=['GET'])
def get_user_cars():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 403

    user_id = session['user_id']
    cars = Car.query.filter_by(user_id=user_id).all()
    cars_list = [
        {"id": car.id, "make": car.make, "model": car.model, "year": car.year, "price": car.price, "image": car.image}
        for car in cars
    ]
    return jsonify(cars_list)

# Добавление новой машины
@api.route('/cars', methods=['POST'])
def add_car():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 403

    make = request.form.get('make')
    model = request.form.get('model')
    year = request.form.get('year')
    price = request.form.get('price')
    image = request.files.get('image')

    filename = None
    if image:
        filename = secure_filename(image.filename)
        image.save(os.path.join(UPLOAD_FOLDER, filename))

    new_car = Car(make=make, model=model, year=year, price=price, image=filename, user_id=session['user_id'])
    db.session.add(new_car)
    db.session.commit()
    return jsonify({"message": "Car added successfully"}), 201

# Получение изображения
@api.route('/uploads/<string:filename>', methods=['GET'])
def get_uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Удаление машины
@api.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 403

    car = Car.query.filter_by(id=car_id, user_id=session['user_id']).first()
    if not car:
        return jsonify({"error": "Car not found or unauthorized"}), 404

    db.session.delete(car)
    db.session.commit()
    return jsonify({"message": "Car deleted successfully"}), 200

# Обновление машины
@api.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 403

    car = Car.query.filter_by(id=car_id, user_id=session['user_id']).first()
    if not car:
        return jsonify({"error": "Car not found or unauthorized"}), 404

    data = request.form
    car.make = data.get('make', car.make)
    car.model = data.get('model', car.model)
    car.year = data.get('year', car.year)
    car.price = data.get('price', car.price)
    db.session.commit()
    return jsonify({"message": "Car updated successfully"}), 200
