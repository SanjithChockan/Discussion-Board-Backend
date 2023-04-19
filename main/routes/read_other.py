from flask import jsonify, request, Blueprint
from ..models import *
from util import related_post_and_search

read_other_bp = Blueprint("read_other", __name__)
from app import db

DEFAULT_N = 50


# Get answers for specific post
@read_other_bp.route("/get_answers_for_post/<int:post_id>", methods=["GET"])
@read_other_bp.route("/get_answers_for_post/<int:post_id>/<int:n>", methods=["GET"])
def get_answers_for_post(post_id, n=DEFAULT_N):
    query = f"SELECT * FROM answers WHERE post_id = {post_id} LIMIT {n}"

    cur = db.cursor()
    cur.execute(query)
    sql_answers = cur.fetchall()

    answers = []
    for row in sql_answers:
        answer = Answers(row[1], row[2], row[3], row[4], row[0])
        answers.append(answer.__dict__)

    return jsonify(answers), 200


# Get course
@read_other_bp.route("/get_course/<int:course_id>", methods=["GET"])
def get_course(course_id):
    query = f"SELECT * FROM courses WHERE course_id = {course_id}"

    cur = db.cursor()
    cur.execute(query)
    courses = format_course_return(cur.fetchall())

    return jsonify(courses[0]), 200
