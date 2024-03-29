from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models import *
from util import rule_based, gpt_api
from datetime import datetime
from ..errors import BadRequestError

create_bp = Blueprint("create", __name__)


# Create post and generate AI answer
@create_bp.route("/create_post", methods=["POST"])
@jwt_required()
def create_post():
    data = request.get_json()
    # Error Handling
    required_keys = ["post_title", "post_content", "course_id"]
    for key in required_keys:
        if key not in data:
            raise BadRequestError(f"Missing {key}")

    user_id = get_jwt_identity()
    course_id = data["course_id"]
    title = data["post_title"]
    content = data["post_content"]

    # Insert post
    post = Post(
        user_id=user_id,
        course_id=course_id,
        post_title=title,
        post_content=content,
        answer_count=1,
    )
    db.session.add(post)
    db.session.commit()

    # Generate automatic answer after post is created
    ai_answer = rule_based.generate(post.post_content, post.course_id, db)
    print(ai_answer)
    if ai_answer == "N/A":
        ai_answer = gpt_api.generate(post.post_content)

    answer = Answer(
        post_id=post.post_id,
        user_id=3,
        answer_content=ai_answer,
        parent_answer=None,
    )
    db.session.add(answer)
    db.session.commit()

    # Get post and return
    return jsonify(post.serialize()), 201


# Create answer (from user)
@create_bp.route("/create_answer", methods=["POST"])
@jwt_required()
def create_answer():
    data = request.get_json()
    # Error Handling
    required_keys = ["post_id", "answer_content", "parent_answer"]
    for key in required_keys:
        if key not in data:
            raise BadRequestError(f"Missing {key}")

    user_id = get_jwt_identity()
    post_id = data["post_id"]
    answer_content = data["answer_content"]
    parent_answer = data["parent_answer"]

    if parent_answer == -1:
        parent_answer = None

    post = Post.query.filter_by(post_id=post_id).first()
    post.answer_count += 1

    answer = Answer(
        post_id=post_id,
        user_id=user_id,
        answer_content=answer_content,
        parent_answer=parent_answer,
    )
    db.session.add(answer)
    db.session.commit()

    return jsonify(answer.serialize()), 201
