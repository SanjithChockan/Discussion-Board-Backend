from flask import jsonify, request, Blueprint
from ..models import *
from util import related_post_and_search
from datetime import datetime
read_bp = Blueprint('read', __name__)
from app import db


# Get all posts from db
@read_bp.route('/get_all_posts', methods=['GET'])
def get_all_posts():
    data = request.json()
    n = data['n']

    cur = db.cursor()
    query = f"SELECT * FROM posts LIMIT {n};"
    cur.execute(query)
    posts = cur.fetchall()
    return jsonify(posts), 200

# Get specific post
@read_bp.route('/get_specific_post', methods=['GET'])
def get_specific_post():
    data = request.get_json()
    post_id = data['post_id']

    cur = db.cursor()
    cur.execute("SELECT * FROM posts WHERE post_id = %s", (post_id,))
    post = cur.fetchone()
    return jsonify(post), 200

# Get related post(s):
@read_bp.route('/get_related_posts', methods=['GET'])
def get_related_posts():
    data = request.get_json()
    post_id = data['post_id']
    n = data['n']

    cur = db.cursor()
    related_post_ids = related_post_and_search.find_most_related_posts(post_id, n, db)
    # Format query and execute
    query = "SELECT * FROM posts WHERE post_id IN (" + ','.join(map(str, related_post_ids)) + ")"
    cur.execute(query)
    posts = cur.fetchall()
    return jsonify(posts), 200

# Lookup n related posts:
@read_bp.route('/search/', methods=['GET'])
def search():
    data = request.get_json()
    sentence = data['sentence']
    n = data['n']

    cur = db.cursor()
    lookup_post_ids = related_post_and_search.lookup_related_posts(sentence, n, db)
    
    # Format query and execute
    query = "SELECT * FROM posts WHERE post_id IN (" + ','.join(map(str, lookup_post_ids)) + ")"
    cur.execute(query)
    posts = cur.fetchall()
    return jsonify(posts), 200

# Get user posts (My posts)
@read_bp.route('/get_user_posts', methods=['GET'])
def get_user_posts():
    # implement current_user.id later when we actually have users
    data = request.get_json()
    user_id = data['user_id']
    n = data['n']

    cur = db.cursor()
    query = f'SELECT * FROM posts WHERE user_id = {user_id} LIMIT {n}'
    cur.execute(query)
    posts = cur.fetchall()
    return jsonify(posts), 200

# Get recommended posts
@read_bp.route('/get_recommended_posts', methods=['GET'])
def get_recommended_posts():
    # data = request.get_json()
    cur = db.cursor()
    query = "SELECT * FROM posts WHERE user_id = ? ()"
    cur.execute(query)
    posts = cur.fetchall()
    return jsonify(posts), 200

# Get professor posts
@read_bp.route('/get_professor_posts', methods=['GET'])
def get_professor_posts():
    data = request.get_json()
    professor_id = data['professor_id']
    n = data['n']

    cur = db.cursor()
    query = f'SELECT * FROM posts WHERE user_id = {professor_id} LIMIT {n}'
    cur.execute(query)
    posts = cur.fetchall()
    return jsonify(posts), 200

# Get recent posts
@read_bp.route('/get_recent_posts', methods=['GET'])
def get_recent_posts():
    # data = request.get_json()
    cur = db.cursor()
    query = "SELECT * FROM posts WHERE user_id = ? ()"
    cur.execute(query)
    posts = cur.fetchall()
    return jsonify(posts), 200


# Get answers for specific post
@read_bp.route('/get_answers_for_post', methods=['GET'])
def get_answers_for_post():
    data = request.get_json()
    post_id = data['post_id']

    cur = db.cursor()
    cur.execute("SELECT * FROM answers WHERE post_id = %s", (post_id,))
    sql_answers = cur.fetchall()
    answers = {}
    for i, row in enumerate(sql_answers):
        answer = Answer(row[1], row[2], row[3], row[4])
        answer.answer_id = row[0]
        answers[i] = answer.__dict__
    return jsonify(answers), 200