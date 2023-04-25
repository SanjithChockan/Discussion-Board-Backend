from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from ..models import User, Professor, Student, Registration, db
import random


auth_blueprint = Blueprint("auth", __name__)


# Register
@auth_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data["password"], method="sha256")
    new_user = User(
        username=data["username"], email=data["email"], password=hashed_password
    )
    db.session.add(new_user)
    try:
        db.session.commit()
    except:
        return jsonify({"message": "User already exists"}), 400

    if data["is_professor"]:
        professor = Professor(user_id=new_user.user_id, course_id=data["course_id"])
        db.session.add(professor)
        db.session.commit()
    else:
        student = Student(user_id=new_user.user_id)
        db.session.add(student)
        db.session.commit()

        # register for courses randomly 1-8, select 4
        items = random.sample(range(1, 9), 4)
        for i in range(4):
            registration = Registration(student_id=new_user.user_id, course_id=items[i])
            db.session.add(registration)
            db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# Login
@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()

    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid username or password"}), 401

    access_token = create_access_token(identity=user.user_id)
    user = user.serialize()
    user["access_token"] = access_token
    return jsonify(user), 200
