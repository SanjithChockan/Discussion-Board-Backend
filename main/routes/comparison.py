from flask import jsonify, request, Blueprint
from ..models import *
from util import related_post_and_search

comparison_bp = Blueprint("comparison", __name__)

DEFAULT_N = 50


# Get related posts based on course_id and post id
@comparison_bp.route(
    "/get_related_course_posts/<int:post_id>/<int:course_id>", methods=["GET"]
)
def get_related_course_post(post_id, course_id):
    related_post_ids = related_post_and_search.find_most_related_posts(
        post_id, course_id
    )
    posts = []
    if related_post_ids:
        posts = Post.query.filter(Post.post_id.in_(related_post_ids)).all()

    return jsonify([post.serialize() for post in posts]), 200


# Get related posts based on content and post title
@comparison_bp.route(
    "/search_with_title_content/<string:content>/<string:title>/<int:n>",
    methods=["GET"],
)
def get_related_content_post(content, title, n=DEFAULT_N):
    related_post_ids = related_post_and_search.search_content_title(content, title, n)
    posts = []
    if related_post_ids:
        posts = Post.query.filter(Post.post_id.in_(related_post_ids)).all()

    return jsonify([post.serialize() for post in posts]), 200


# Search:
@comparison_bp.route("/search/<string:query>", methods=["GET"])
@comparison_bp.route("/search/<string:query>/<int:n>", methods=["GET"])
def search(query, n=DEFAULT_N):
    lookup_post_ids = related_post_and_search.search_sentence(query, n)
    posts = []
    if lookup_post_ids:
        posts = Post.query.filter(Post.post_id.in_(lookup_post_ids)).all()

    return jsonify([post.serialize() for post in posts]), 200
