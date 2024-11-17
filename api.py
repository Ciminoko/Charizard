from flask import Blueprint, request, jsonify, send_from_directory, render_template
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
            return render_template('index.html', username=user.username)
        return jsonify({"error": "Invalid username or password"}), 401
    return render_template('login.html')

# Получение всех машин
@api.route('/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    cars_list = [{"id": car.id, "make": car.make, "model": car.model, "year": car.year} for car in cars]
    return render_template('view_cars.html', cars=cars_list)

# Добавление новой машины
@api.route('/cars', methods=['POST'])
def add_car():
    data = request.form
    username = data.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Unauthorized access"}), 403

    new_car = Car(make=data.get('make'), model=data.get('model'), year=data.get('year'))
    db.session.add(new_car)
    db.session.commit()
    return jsonify({"message": "Car added successfully", "car_id": new_car.id}), 201

# Обновление машины
@api.route('/cars/<string:car_id>', methods=['PUT'])
def update_car(car_id):
    data = request.form
    car = Car.query.filter_by(id=car_id).first()
    if not car:
        return jsonify({"error": "Car not found"}), 404

    car.make = data.get('make', car.make)
    car.model = data.get('model', car.model)
    car.year = data.get('year', car.year)
    db.session.commit()
    return jsonify({"message": "Car updated successfully", "car_id": car.id})

# Удаление машины
@api.route('/cars/<string:car_id>', methods=['DELETE'])
def delete_car(car_id):
    data = request.form
    username = data.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Unauthorized access"}), 403

    car = Car.query.filter_by(id=car_id).first()
    if not car:
        return jsonify({"error": "Car not found"}), 404

    db.session.delete(car)
    db.session.commit()
    return jsonify({"message": "Car deleted successfully"}), 200

# Получение детальной информации о машине
@api.route('/cars/<string:car_id>', methods=['GET'])
def get_car_details(car_id):
    car = Car.query.filter_by(id=car_id).first()
    if not car:
        return jsonify({"error": "Car not found"}), 404
    return jsonify({"id": car.id, "make": car.make, "model": car.model, "year": car.year})

# Загрузка изображения
@api.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return jsonify({"message": "File uploaded successfully", "filename": filename}), 201

# Получение изображения
@api.route('/uploads/<string:filename>', methods=['GET'])
def get_uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

