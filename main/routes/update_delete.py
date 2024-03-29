from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models import *
from ..errors import BadRequestError

update_delete_bp = Blueprint("update_delete", __name__)


# Edit post
@update_delete_bp.route("/edit_post", methods=["PUT"])
@jwt_required()
def update_post():
    data = request.get_json()

    required_keys = ["post_id", "post_title", "post_content"]
    for key in required_keys:
        if key not in data:
            raise BadRequestError(f"Missing {key}")

    user_id = get_jwt_identity()
    post_id = data["post_id"]
    post = Post.query.filter_by(post_id=post_id).first()

    # Check if user has professor role first
    professor = Professor.query.filter_by(user_id=user_id).first()
    if not professor or professor.course_id != post.course_id:
        # Check if this is the user's post
        if post.user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 401

    # Set updated content and title
    new_title = data["post_title"]
    new_content = data["post_content"]

    # Fetch post and update
    post = Post.query.filter_by(post_id=post_id).first()
    post.post_title = new_title
    post.post_content = new_content
    db.session.commit()

    # Return JSON
    return jsonify(post.serialize()), 200


# Edit answer
@update_delete_bp.route("/edit_answer", methods=["PUT"])
@jwt_required()
def update_answer():
    data = request.get_json()
    # Error Handling
    required_keys = ["answer_id", "answer_content"]
    for key in required_keys:
        if key not in data:
            raise BadRequestError(f"Missing {key}")

    user_id = get_jwt_identity()
    answer_id = data["answer_id"]
    answer = Answer.query.filter_by(answer_id=answer_id).first()
    post = Post.query.filter_by(post_id=answer.post_id).first()

    # Check if user has professor role first
    professor = Professor.query.filter_by(user_id=user_id).first()
    if not professor or professor.course_id != post.course_id:
        # Check if this is the user's answer
        if answer.user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 401

    # Set updated content
    new_content = data["answer_content"]

    # Fetch answer and update
    answer = Answer.query.filter_by(answer_id=answer_id).first()
    answer.answer_content = new_content
    db.session.commit()

    # Return JSON
    return jsonify(answer.serialize()), 200


# Delete post
@update_delete_bp.route("/delete_post", methods=["DELETE"])
@jwt_required()
def delete_post():
    data = request.get_json()
    # Error Handling
    required_keys = ["post_id"]
    for key in required_keys:
        if key not in data:
            raise BadRequestError(f"Missing {key}")

    post_id = data["post_id"]
    user_id = get_jwt_identity()

    # Check if post exists
    post = Post.query.filter_by(post_id=post_id).first()
    if post is None:
        return jsonify({"error": "Post not found."}), 404

    # Check if user has professor role first
    professor = Professor.query.filter_by(user_id=user_id).first()
    if not professor or professor.course_id != post.course_id:
        # Check if this is the user's post
        if post.user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 401

    db.session.delete(post)
    db.session.commit()

    return jsonify({"message": "Post deleted successfully"}), 200


# Delete answer
@update_delete_bp.route("/delete_answer", methods=["DELETE"])
@jwt_required()
def delete_answer():
    data = request.get_json()
    # Error Handling
    required_keys = ["answer_id"]
    for key in required_keys:
        if key not in data:
            raise BadRequestError(f"Missing {key}")

    answer_id = data["answer_id"]
    user_id = get_jwt_identity()

    # Check if answer exists
    answer = Answer.query.filter_by(answer_id=answer_id).first()
    if answer is None:
        return jsonify({"error": "Answer not found."}), 404

    # Check if user has professor role first
    post = Post.query.filter_by(post_id=answer.post_id).first()
    professor = Professor.query.filter_by(user_id=user_id).first()
    if not professor or professor.course_id != post.course_id:
        # Check if this is the user's answer
        if answer.user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 401

    db.session.delete(answer)
    db.session.commit()

    return jsonify({"message": "Answer deleted successfully"}), 200
