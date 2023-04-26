from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models import *
from util import rule_based, gpt_api
from datetime import datetime
from ..errors import *

courses_bp = Blueprint("courses", __name__)

# Register for list of courses
# @courses_bp.route("/register", methods=["POST"])
# @jwt_required()
# def register():
#     return


# Get list of courses for user
@courses_bp.route("/user_courses", methods=["GET"])
@jwt_required()
def user_courses():
    user_id = get_jwt_identity()
    student = Student.query.get(user_id)
    if not student:
        raise BadRequestError("User is not a student")

    registrations = Registration.query.filter_by(student_id=user_id).all()
    courses = [registration.course.serialize() for registration in registrations]
    return jsonify(courses), 200
