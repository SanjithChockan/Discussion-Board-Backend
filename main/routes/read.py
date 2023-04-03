from flask import jsonify, request, Blueprint
from ..models import *
from util import related_post
from datetime import datetime
read_bp = Blueprint('read', __name__)
from app import db

# Get all posts from db
@read_bp.route('/get_all_posts', methods=['GET'])
def get_all_posts():
    # data = request.get_json()
    cur = db.cursor()
    query = "SELECT * FROM posts"
    cur.execute(query)
    posts = cur.fetchall()
    return jsonify(posts), 200

# Get related posts:
@read_bp.route('/get_related_posts', methods=['GET'])
def get_related_posts():
    # data = request.get_json()
    target_post_id = 7
    cur = db.cursor()
    related_post_ids = related_post.find_most_related_posts(target_post_id, 1, db)
    
    # Format query and execute
    query = "SELECT * FROM posts WHERE post_id IN (" + ','.join(map(str, related_post_ids)) + ")"
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