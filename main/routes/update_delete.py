from flask import jsonify, request, Blueprint
from ..models import *

update_delete_bp = Blueprint("update_delete", __name__)


# Edit post
@update_delete_bp.route("/edit_post", methods=["PUT"])
def update_post():
    data = request.get_json()
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
@update_delete_bp.route("/edit_answer", methods=["PUT"])
def update_answer(id):
    data = request.get_json()
    answer_id = data["answer_id"]
    new_content = data["content"]

    # Fetch answer and update
    answer = Answer.query.filter_by(answer_id=answer_id).first()
    answer.answer_content = new_content
    db.session.commit()

    # Return JSON
    return jsonify(answer.serialize()), 200


# Delete post
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
