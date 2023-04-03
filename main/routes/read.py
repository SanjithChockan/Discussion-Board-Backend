from flask import jsonify, request, Blueprint
from ..models import *
from util import related_post_and_search
from datetime import datetime
read_bp = Blueprint('read', __name__)
from app import db


# Get all posts from db
@read_bp.route('/get_all_posts', methods=['GET'])
def get_all_posts():
    cur = db.cursor()
    query = "SELECT * FROM posts"
    cur.execute(query)
    posts = cur.fetchall()
    return jsonify(posts), 200

# Get related post(s):
@read_bp.route('/get_related_posts/<int:post_id>', methods=['GET'])
def get_related_posts(post_id):
    cur = db.cursor()
    n = 1
    related_post_ids = related_post_and_search.find_most_related_posts(post_id, n, db)
    # Format query and execute
    query = "SELECT * FROM posts WHERE post_id IN (" + ','.join(map(str, related_post_ids)) + ")"
    cur.execute(query)
    posts = cur.fetchall()
    return jsonify(posts), 200

# Lookup n related posts:
@read_bp.route('/search/<string:sentence>', methods=['GET'])
def search(sentence):
    cur = db.cursor()
    n = 1
    lookup_post_ids = related_post_and_search.lookup_related_posts(sentence, n, db)
    
    # Format query and execute
    query = "SELECT * FROM posts WHERE post_id IN (" + ','.join(map(str, lookup_post_ids)) + ")"
    cur.execute(query)
    posts = cur.fetchall()
    return jsonify(posts), 200

# Get user posts (My posts)
@read_bp.route('/get_user_posts', methods=['GET'])
def get_user_posts():
    # data = request.get_json()
    cur = db.cursor()
    query = "SELECT * FROM posts WHERE user_id = ? ()"
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
    # data = request.get_json()
    cur = db.cursor()
    query = "SELECT * FROM posts WHERE user_id = ? ()"
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