from flask import jsonify, request, Blueprint
from ..models import *
from util import related_post_and_search

read_bp = Blueprint("read", __name__)
from app import db

DEFAULT_N = 50


# Get all posts from db
@read_bp.route("/get_all_posts", methods=["GET"])
@read_bp.route("/get_all_posts/<int:n>", methods=["GET"])
def get_all_posts(n=DEFAULT_N):
    query = f"SELECT * FROM posts LIMIT {n};"

    cur = db.cursor()
    cur.execute(query)
    posts = format_return(cur.fetchall())

    return jsonify(posts), 200


# Get specific post
@read_bp.route("/get_specific_post", methods=["GET"])
@read_bp.route("/get_specific_post/<int:post_id>", methods=["GET"])
def get_specific_post(post_id, n=DEFAULT_N):
    query = f"SELECT * FROM posts WHERE post_id = {post_id} LIMIT {n}"

    cur = db.cursor()
    cur.execute(query)
    posts = format_return(cur.fetchone())

    return jsonify(posts[0].__dict__), 200


# Get related post(s):
@read_bp.route("/get_related_posts/<int:post_id>", methods=["GET"])
@read_bp.route("/get_related_posts/<int:post_id>/<int:n>", methods=["GET"])
def get_related_posts(post_id, n=DEFAULT_N):
    related_post_ids = related_post_and_search.find_most_related_posts(post_id, n, db)

    query = (
        "SELECT * FROM posts WHERE post_id IN ("
        + ",".join(map(str, related_post_ids))
        + f") LIMIT {n}"
    )

    cur = db.cursor()
    cur.execute(query)
    posts = format_return(cur.fetchall())

    return jsonify(posts), 200


# Lookup n related posts:
@read_bp.route("/search/<string:query>", methods=["GET"])
@read_bp.route("/search/<string:query>/<int:n>", methods=["GET"])
def search(query, n=DEFAULT_N):
    lookup_post_ids = related_post_and_search.lookup_related_posts(query, n, db)

    query = (
        "SELECT * FROM posts WHERE post_id IN ("
        + ",".join(map(str, lookup_post_ids))
        + ")"
    )

    cur = db.cursor()
    cur.execute(query)
    posts = format_return(cur.fetchall())

    return jsonify(posts), 200


# Get user posts (My posts)
@read_bp.route("/get_user_posts", methods=["GET"])
@read_bp.route("/get_user_posts/<int:n>", methods=["GET"])
def get_user_posts(n=DEFAULT_N):
    user_id = 3  # implement current_user.id later when we actually have users

    query = f"SELECT * FROM posts WHERE user_id = {user_id} LIMIT {n}"

    cur = db.cursor()
    cur.execute(query)
    posts = format_return(cur.fetchall())

    return jsonify(posts), 200


# Get recommended posts
@read_bp.route("/get_recommended_posts", methods=["GET"])
def get_recommended_posts():
    query = "SELECT * FROM posts WHERE user_id = ? ()"

    cur = db.cursor()
    cur.execute(query)
    posts = format_return(cur.fetchall())

    return jsonify(posts), 200


# Get professor posts
@read_bp.route("/get_professor_posts/<int:professor_id>", methods=["GET"])
@read_bp.route("/get_professor_posts/<int:professor_id>/<int:n>", methods=["GET"])
def get_professor_posts(professor_id, n=DEFAULT_N):
    query = f"SELECT * FROM posts WHERE user_id = {professor_id} LIMIT {n}"

    cur = db.cursor()
    cur.execute(query)
    posts = format_return(cur.fetchall())

    return jsonify(posts), 200


# Get recent posts
@read_bp.route("/get_recent_posts", methods=["GET"])
def get_recent_posts():
    # data = request.get_json()
    cur = db.cursor()
    query = "SELECT * FROM posts WHERE user_id = ? ()"
    cur.execute(query)
    posts = format_return(cur.fetchall())
    return jsonify(posts), 200


# Get answers for specific post
@read_bp.route("/get_answers_for_post/<int:post_id>", methods=["GET"])
@read_bp.route("/get_answers_for_post/<int:post_id>/<int:n>", methods=["GET"])
def get_answers_for_post(post_id, n=DEFAULT_N):
    query = f"SELECT * FROM answers WHERE post_id = {post_id} LIMIT {n}"

    cur = db.cursor()
    cur.execute(query)
    sql_answers = cur.fetchall()

    answers = []
    for row in sql_answers:
        answer = Answer(row[1], row[2], row[3], row[4], row[0])
        answers.append(answer.__dict__)

    return jsonify(answers), 200


def format_return(sql_posts):
    posts = []
    for row in sql_posts:
        post = Post(row[1], row[2], row[3], row[4], row[5], row[6], row[0])
        posts.append(post.__dict__)

    return posts
