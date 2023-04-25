from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models import *

update_delete_bp = Blueprint("update_delete", __name__)


# Edit post
@update_delete_bp.route("/edit_post", methods=["PUT"])
@jwt_required()
def update_post():
    data = request.get_json()
    user_id = get_jwt_identity()
    post_id = data["post_id"]

    # Check if user has professor role first
    professor = Professor.query.filter_by(user_id=user_id).first()
    if len(professor) == 0:
        # Check if this is the user's post
        post = Post.query.filter_by(post_id=post_id).first()
        if post.user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 401

    # Set updated content and title
    new_title = data["title"]
    new_content = data["content"]

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
def update_answer(id):
    data = request.get_json()
    user_id = get_jwt_identity()
    answer_id = data["answer_id"]

    # Check if user has professor role first
    professor = Professor.query.filter_by(user_id=user_id).first()
    if len(professor) == 0:
        # Check if this is the user's answer
        answer = Answer.query.filter_by(answer_id=answer_id).first()
        if answer.user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 401

    # Set updated content
    new_content = data["content"]

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
    post_id = data["post_id"]
    user_id = get_jwt_identity()

    # Check if post exists
    post = Post.query.filter_by(post_id=post_id).first()
    if post is None:
        return jsonify({"error": "Post not found."}), 404

    # Check if user has professor role first
    professor = Professor.query.filter_by(user_id=user_id).first()
    if not professor:
        # Check if this is the user's post
        if post.user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 401

    db.session.delete(post)
    db.session.commit()

    return "Post deleted successfully", 204


# Delete answer
@update_delete_bp.route("/delete_answer", methods=["DELETE"])
@jwt_required()
def delete_answer():
    data = request.get_json()
    answer_id = data["answer_id"]
    user_id = get_jwt_identity()

    # Check if answer exists
    answer = Answer.query.filter_by(answer_id=answer_id).first()
    if answer is None:
        return jsonify({"error": "Answer not found."}), 404

    # Check if user has professor role first
    professor = Professor.query.filter_by(user_id=user_id).first()
    if len(professor) == 0:
        # Check if this is the user's answer
        if answer.user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 401

    db.session.delete(answer)
    db.session.commit()

    return "Answer deleted successfully", 204
