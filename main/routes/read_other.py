from flask import jsonify, request, Blueprint
from ..models import Answer, Course, User
from util import related_post_and_search
from app import db
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

read_other_bp = Blueprint("read_other", __name__)

DEFAULT_N = 50


# Get replies from of an answer
@read_other_bp.route("/get_replies_from_answer/<int:post_id>/<int:answer_id>", methods=["GET"])
def get_replies_from_answer(post_id, answer_id):
    Session = sessionmaker(bind=db.engine)
    session = Session()

    query = text(
        """
        WITH RECURSIVE nested_answers AS (
        SELECT *, 1 as depth, CAST(answer_id AS CHAR(255)) as path
        FROM answers
        WHERE post_id = :post_id AND parent_answer IS NULL

        UNION ALL

        SELECT a.*, depth + 1, CONCAT(path, ',', a.answer_id)
        FROM answers AS a
        INNER JOIN nested_answers AS na ON a.parent_answer = na.answer_id
        WHERE a.post_id = :post_id
        )

        SELECT * FROM nested_answers ORDER BY path;
        """
    )

    answers = session.query(Answer).from_statement(query).params(post_id=post_id, answer_id=answer_id).all()
    result = []
    for a in answers:
        if a.parent_answer == answer_id:
            result.append(a)
    return jsonify([res.serialize() for res in result]), 200

    #return jsonify([answer.serialize() for answer in answers]), 200

# Get answers for specific post
@read_other_bp.route("/get_answers_for_post/<int:post_id>", methods=["GET"])
@read_other_bp.route("/get_answers_for_post/<int:post_id>/<int:n>", methods=["GET"])
def get_answers_for_post(post_id, n=DEFAULT_N):
    Session = sessionmaker(bind=db.engine)
    session = Session()

    query = text(
        """
        WITH RECURSIVE nested_answers AS (
        SELECT *, 1 as depth, CAST(answer_id AS CHAR(255)) as path
        FROM answers
        WHERE post_id = :post_id AND parent_answer IS NULL

        UNION ALL

        SELECT a.*, depth + 1, CONCAT(path, ',', a.answer_id)
        FROM answers AS a
        INNER JOIN nested_answers AS na ON a.parent_answer = na.answer_id
        WHERE a.post_id = :post_id
        )

        SELECT * FROM nested_answers ORDER BY path;
        """
    )

    answers = session.query(Answer).from_statement(query).params(post_id=post_id).all()

    def fill_nested_replies(answer):
        answer.replies = []
        for a in answers:
            if a.parent_answer == answer.answer_id:
                answer.replies.append(fill_nested_replies(a))
        return answer

    result = []

    for a in answers:
        if a.parent_answer == None:
            a.replies = fill_nested_replies(a).copy()
            result.append(a)
            
    return jsonify([res.serialize() for res in result]), 200

# Get answers for a specific answer
@read_other_bp.route("/get_answers_for_answer/<int:answer_id>", methods=["GET"])
@read_other_bp.route("/get_answers_for_answer/<int:answer_id>/<int:n>", methods=["GET"])
def get_answers_for_answer(answer_id, n=DEFAULT_N):
    Session = sessionmaker(bind=db.engine)
    session = Session()

    query = text(
        """
        WITH RECURSIVE answer_tree AS (
        SELECT answer_id, post_id, user_id, answer_content, time_created, parent_answer
        FROM answers
        WHERE answer_id = :answer_id
        UNION ALL
        SELECT a.answer_id, a.post_id, a.user_id, a.answer_content, a.time_created, a.parent_answer
        FROM answers a
        JOIN answer_tree t ON a.parent_answer = t.answer_id
        )
        SELECT answer_id, post_id, user_id, answer_content, time_created, parent_answer
        FROM answer_tree;

        """
    )

    answers = session.query(Answer).from_statement(query).params(answer_id = answer_id).all()

    return jsonify([answer.serialize() for answer in answers]), 200


# Get course
@read_other_bp.route("/get_course/<int:course_id>", methods=["GET"])
def get_course(course_id):
    course = Course.query.filter_by(course_id=course_id).first()
    if course:
        return jsonify(course.serialize()), 200
    else:
        return jsonify({"message": "Course not found"}), 404


# Get user id based off of username and password
@read_other_bp.route("/get_user_id/<string:username>/<string:password>", methods=["GET"])
def get_user_id(username, password):
    user = User.query.filter_by(username= username, password= password).first()
    if user and user.password == password:
        return jsonify(user.user_id.serialize()), 200
    else:
        return jsonify({"message": "User not found"}), 404
