from flask import jsonify, request, Blueprint
from ..models import *
from util import related_post_and_search
from app import db
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from util.gpt_api import generate_answer
import re

read_other_bp = Blueprint("read_other", __name__)

DEFAULT_N = 50


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

        SELECT * FROM nested_answers ORDER BY path, time_created DESC;
        """
    )

    answers = session.query(Answer).from_statement(query).params(post_id=post_id).all()
    count = len(answers)
    post = Post.query.filter_by(post_id=post_id).first()
    post.answer_count = count
    db.session.commit()

    def build_nested_dict(answers, parent_id=None):
        nested_answers = []

        for answer in answers:
            if answer.parent_answer == parent_id:
                answer_dict = answer.serialize()
                answer_dict["replies"] = build_nested_dict(answers, answer.answer_id)
                nested_answers.append(answer_dict)

        return nested_answers

    nested_answers = build_nested_dict(answers)
    # return result
    return jsonify(nested_answers), 200


@read_other_bp.route("/get_quick_answer", methods=["POST"])
def quick_help():
    data = request.get_json()
    course_id = data["course_id"]
    content = data["content"]
    answer = generate_answer(content, course_id)
    answer = re.search("[a-zA-Z0-9].*", answer)
    if answer:
        answer = answer.group(0)
    else:
        answer = ""
    answer = answer.strip().replace("\n", "")
    return jsonify(answer), 200
