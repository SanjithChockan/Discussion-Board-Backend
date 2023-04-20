from flask import jsonify, request, Blueprint
from ..models import Answer, Course
from util import related_post_and_search
from app import db

read_other_bp = Blueprint("read_other", __name__)

DEFAULT_N = 50


# Get answers for specific post
@read_other_bp.route("/get_answers_for_post/<int:post_id>", methods=["GET"])
@read_other_bp.route("/get_answers_for_post/<int:post_id>/<int:n>", methods=["GET"])
def get_answers_for_post(post_id, n=DEFAULT_N):
    answers = Answer.query.filter_by(post_id=post_id).limit(n).all()
    return jsonify([answer.serialize() for answer in answers]), 200


# Get course
@read_other_bp.route("/get_course/<int:course_id>", methods=["GET"])
def get_course(course_id):
    course = Course.query.filter_by(course_id=course_id).first()
    if course:
        return jsonify(course.serialize()), 200
    else:
        return jsonify({"message": "Course not found"}), 404


# Get user
