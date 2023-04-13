from flask import jsonify, request, Blueprint
from ..models import *
from util import related_post_and_search
from util.format import *

read_posts_bp = Blueprint("read_posts", __name__)
from app import db

DEFAULT_N = 50


# Get all posts from db
@read_posts_bp.route("/get_all_posts", methods=["GET"])
@read_posts_bp.route("/get_all_posts/<int:n>", methods=["GET"])
def get_all_posts(n=DEFAULT_N):
    query = f"SELECT * FROM posts LIMIT {n};"

    cur = db.cursor()
    cur.execute(query)
    posts = format_post_return(cur.fetchall())

    return jsonify(posts), 200


# Get specific post
@read_posts_bp.route("/get_specific_post", methods=["GET"])
@read_posts_bp.route("/get_specific_post/<int:post_id>", methods=["GET"])
def get_specific_post(post_id):
    query = f"SELECT * FROM posts WHERE post_id = {post_id}"

    cur = db.cursor()
    cur.execute(query)
    posts = format_post_return(cur.fetchall())

    return jsonify(posts[0]), 200


# Get related post(s):
@read_posts_bp.route("/get_related_posts/<int:post_id>", methods=["GET"])
@read_posts_bp.route("/get_related_posts/<int:post_id>/<int:n>", methods=["GET"])
def get_related_posts(post_id, n=DEFAULT_N):
    related_post_ids = related_post_and_search.find_most_related_posts(post_id, n, db)
    posts = {}
    if not related_post_ids:
        pass
    else:
        query = (
            "SELECT * FROM posts WHERE post_id IN ("
            + ",".join(map(str, related_post_ids))
            + f") LIMIT {n}"
        )

        cur = db.cursor()
        cur.execute(query)
        posts = format_post_return(cur.fetchall())

    return jsonify(posts), 200


# Lookup n related posts:
@read_posts_bp.route("/search/<string:query>", methods=["GET"])
@read_posts_bp.route("/search/<string:query>/<int:n>", methods=["GET"])
def search(query, n=DEFAULT_N):
    lookup_post_ids = related_post_and_search.lookup_related_posts(query, n, db)
    posts = {}
    if not lookup_post_ids:
        pass
    else:
        query = (
            "SELECT * FROM posts WHERE post_id IN ("
            + ",".join(map(str, lookup_post_ids))
            + ")"
        )

        cur = db.cursor()
        cur.execute(query)
        posts = format_post_return(cur.fetchall())

    return jsonify(posts), 200


# Get user posts (My posts)
@read_posts_bp.route("/get_user_posts/<int:user_id>", methods=["GET"])
@read_posts_bp.route("/get_user_posts/<int:user_id>/<int:n>", methods=["GET"])
def get_user_posts(user_id, n=DEFAULT_N):
    # implement current_user.id later when we actually have users
    query = f"SELECT * FROM posts WHERE user_id = {user_id} LIMIT {n}"

    cur = db.cursor()
    cur.execute(query)
    posts = format_post_return(cur.fetchall())

    return jsonify(posts), 200


# Get recommended posts
@read_posts_bp.route("/get_recommended_posts", methods=["GET"])
@read_posts_bp.route("/get_recommended_posts/<int:n>", methods=["GET"])
def get_recommended_posts(n=DEFAULT_N):
    query = f"SELECT * FROM posts LIMIT {n}"

    cur = db.cursor()
    cur.execute(query)
    posts = format_post_return(cur.fetchall())

    return jsonify(posts), 200


# Get professor posts
@read_posts_bp.route("/get_professor_posts/<int:professor_id>", methods=["GET"])
@read_posts_bp.route("/get_professor_posts/<int:professor_id>/<int:n>", methods=["GET"])
def get_professor_posts(professor_id, n=DEFAULT_N):
    query = f"SELECT * FROM posts WHERE user_id = {professor_id} LIMIT {n}"

    cur = db.cursor()
    cur.execute(query)
    posts = format_post_return(cur.fetchall())

    return jsonify(posts), 200


# Get recent posts
@read_posts_bp.route("/get_recent_posts", methods=["GET"])
@read_posts_bp.route("/get_recent_posts/<int:n>", methods=["GET"])
def get_recent_posts(n=DEFAULT_N):
    query = f"SELECT * FROM posts LIMIT {n}"

    cur = db.cursor()
    cur.execute(query)
    posts = format_post_return(cur.fetchall())

    return jsonify(posts), 200
