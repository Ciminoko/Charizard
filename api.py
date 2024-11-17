from flask import Blueprint, request, jsonify, send_from_directory, render_template
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
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
        data = request.form  # Здесь используем request.form
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"error": "User already exists"}), 400

        new_user = User(username=username, password=password)  # Добавьте хэширование паролей
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201

    # Для метода GET рендерим страницу регистрации
    return render_template('register.html')



# Авторизация
@api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("POST request received for login")
        data = request.form
        print("Form data received:", data)
        username = data.get('username')
        password = data.get('password')
        print("Username:", username, "Password:", password)
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            access_token = create_access_token(identity=user.id)
            print("User authenticated. Access token created.")
            return jsonify(access_token=access_token), 200
        print("Invalid username or password")
        return jsonify({"error": "Invalid username or password"}), 401
    return render_template('login.html')



# CRUD операции для машин
@api.route('/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    cars_list = [{"id": car.id, "make": car.make, "model": car.model, "year": car.year} for car in cars]
    return jsonify(cars_list)


@api.route('/cars', methods=['POST'])
@jwt_required()
def add_car():
    data = request.json
    new_car = Car(make=data.get('make'), model=data.get('model'), year=data.get('year'))
    db.session.add(new_car)
    db.session.commit()
    return jsonify({"id": new_car.id, "make": new_car.make, "model": new_car.model, "year": new_car.year}), 201

@api.route('/cars/<string:car_id>', methods=['PUT'])
@jwt_required()
def update_car(car_id):
    data = request.json
    car = Car.query.filter_by(id=car_id).first()
    if not car:
        return jsonify({"error": "Car not found"}), 404
    car.make = data.get('make', car.make)
    car.model = data.get('model', car.model)
    car.year = data.get('year', car.year)
    db.session.commit()
    return jsonify({"id": car.id, "make": car.make, "model": car.model, "year": car.year})

@api.route('/cars/<string:car_id>', methods=['DELETE'])
@jwt_required()
def delete_car(car_id):
    car = Car.query.filter_by(id=car_id).first()
    if not car:
        return jsonify({"error": "Car not found"}), 404
    db.session.delete(car)
    db.session.commit()
    return '', 204
