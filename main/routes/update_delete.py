from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models import *

update_delete_bp = Blueprint("update_delete", __name__)


# Edit post
@jwt_required()
@update_delete_bp.route("/edit_post", methods=["PUT"])
def update_post():
    data = request.get_json()

    # Check if user is authorized to edit post
    user_id = get_jwt_identity()
    post = Post.query.filter_by(post_id=data["post_id"]).first()
    if post.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 401

    post_id = data["post_id"]
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
@jwt_required()
@update_delete_bp.route("/edit_answer", methods=["PUT"])
def update_answer(id):
    data = request.get_json()

    # Check if user is authorized to edit answer
    user_id = get_jwt_identity()
    answer = Answer.query.filter_by(answer_id=data["answer_id"]).first()
    if answer.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 401

    answer_id = data["answer_id"]
    new_content = data["content"]

    # Fetch answer and update
    answer = Answer.query.filter_by(answer_id=answer_id).first()
    answer.answer_content = new_content
    db.session.commit()

    # Return JSON
    return jsonify(answer.serialize()), 200


# Delete post
@jwt_required()
@update_delete_bp.route("/delete_post", methods=["DELETE"])
def delete_post():
    data = request.get_json()
    post_id = data["post_id"]

    post = Post.query.filter_by(post_id=post_id).first()
    if post is None:
        return jsonify({"error": "Post not found."}), 404

    db.session.delete(post)
    db.session.commit()

    return "Post deleted successfully", 204


# Delete answer
@jwt_required()
@update_delete_bp.route("/delete_answer", methods=["DELETE"])
def delete_answer():
    data = request.get_json()
    answer_id = data["answer_id"]

    answer = Answer.query.filter_by(answer_id=answer_id).first()
    if answer is None:
        return jsonify({"error": "Answer not found."}), 404

    db.session.delete(answer)
    db.session.commit()

    return "Answer deleted successfully", 204
