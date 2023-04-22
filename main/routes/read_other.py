from flask import jsonify, request, Blueprint
from ..models import Answer, Course, User
from util import related_post_and_search
from app import db
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

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

        SELECT * FROM nested_answers ORDER BY path;
        """
    )

    answers = session.query(Answer).from_statement(query).params(post_id=post_id).all()
    nested_answers = answers.copy()

    for na in nested_answers:
        for a in answers:
            if a.parent_answer == na.answer_id:
                na.replies.append(a)

    result = []

    for na in nested_answers:
        if na.parent_answer == None:
            result.append(a)
    # return result
    return jsonify([res.serialize() for res in nested_answers]), 200
