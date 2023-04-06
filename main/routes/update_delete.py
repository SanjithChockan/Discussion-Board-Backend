import json
from flask import jsonify, request, Blueprint
from ..models import *
from datetime import datetime
update_delete_bp = Blueprint('update_delete', __name__)
from app import db

# Edit post
@update_delete_bp.route('/edit_post', methods=['PUT'])
def update_post():
    data = request.get_json()
    post_id = data['post_id']
    new_title = data['title']
    new_content = data['content']

    cur = db.cursor()
    update_query = """
    UPDATE posts
    SET title = %s, content = %s
    WHERE post_id = %s;
    """
    cur.execute(update_query, (new_title, new_content, post_id))
    db.session.commit()

    # Define the select query
    cur.execute("SELECT * FROM posts WHERE post_id = %s", (post_id,))
    post = cur.fetchone()

    # Return JSON
    return jsonify(post), 200

# Edit answer
@update_delete_bp.route('/edit_answer', methods=['PUT'])
def update_answer(id):
    data = request.get_json()
    answer_id = data['answer_id']
    new_content = data['content']

    cur = db.cursor()
    update_query = """
    UPDATE answers
    SET content = %s
    WHERE answer_id = %s;
    """
    cur.execute(update_query, (new_content, answer_id))
    db.session.commit()

    # Define the select query
    cur.execute("SELECT * FROM answer WHERE answer_id = %s", (answer_id,))
    answer = cur.fetchone()

    # Return JSON
    return jsonify(answer), 200


# Delete post
@update_delete_bp.route('/delete_post', methods=['DELETE'])
def delete_post():
    data = request.get_json()
    post_id = data['post_id']
    
    cur = db.cursor()
    delete_query = "DELETE FROM posts WHERE post_id = %s"
    cur.execute(delete_query, (post_id,))
    db.commit()

    return "Deleted successfully", 204

# Delete answer
@update_delete_bp.route('/delete_answer', methods=['DELETE'])
def delete_answer():
    data = request.get_json()
    answer_id = data['answer_id']
    
    cur = db.cursor()
    delete_query = "DELETE FROM answers WHERE answer_id = %s"
    cur.execute(delete_query, (answer_id,))
    db.commit()
    
    return "Deleted successfully", 204