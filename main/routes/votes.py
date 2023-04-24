from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models import *
from util import rule_based, gpt_api
from datetime import datetime

votes_bp = Blueprint("votes", __name__)


# Upvote answer
@votes_bp.route("/upvote_answer", methods=["POST"])
@jwt_required()
def upvote_post():
    data = request.get_json()
    answer_id = data["answer_id"]
    user_id = get_jwt_identity()

    existing_vote = Vote.query.filter_by(answer_id=answer_id, user_id=user_id).first()

    if existing_vote:
        if existing_vote.vote_type:
            return jsonify({"error": "already upvoted"}), 403
        else:
            existing_vote.vote_type = True
            db.session.commit()
            return jsonify({"message": "downvote changed to upvote"})
    else:
        new_upvote = Vote(answer_id=answer_id, user_id=user_id, vote_type=True)
        db.session.add(new_upvote)
        db.session.commit()
        return jsonify({"message": "upvote created"})


# Downvote answer
@votes_bp.route("/downvote_answer", methods=["POST"])
@jwt_required()
def downvote_post():
    data = request.get_json()
    user_id = get_jwt_identity()
    answer_id = data["answer_id"]

    existing_vote = Vote.query.filter_by(answer_id=answer_id, user_id=user_id).first()

    if existing_vote:
        if existing_vote.vote_type:
            existing_vote.vote_type = False
            db.session.commit()
            return jsonify({"message": "upvote changed to downvote"})
        else:
            return jsonify({"error": "already downvoted"}), 403
    else:
        new_downvote = Vote(answer_id=answer_id, user_id=user_id, vote_type=False)
        db.session.add(new_downvote)
        db.session.commit()
        return jsonify({"message": "downvote created"})


# Undo vote
@votes_bp.route("/undo_vote", methods=["POST"])
@jwt_required()
def undo_vote():
    data = request.get_json()
    user_id = get_jwt_identity()
    answer_id = data["answer_id"]

    existing_vote = Vote.query.filter_by(answer_id=answer_id, user_id=user_id).first()

    if existing_vote:
        db.session.delete(existing_vote)
        db.session.commit()
        return jsonify({"message": "vote deleted"})
    else:
        return jsonify({"error": "no vote found"}), 404
