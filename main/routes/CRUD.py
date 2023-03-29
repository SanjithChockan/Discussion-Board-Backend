from flask import jsonify, request, Blueprint
import sys
from ..models import *
from intelligent_answering import rule_based, gpt_api
from datetime import datetime
bp = Blueprint('CRUD', __name__)
from app import db

# This is supposed to retrieve all the posts from the database
@bp.route('/getposts', methods=['GET'])
def get_posts():
    ## Add code to select posts from specific course, get courseID from request data
    # data = request.get_json()
    cur = db.cursor()
    query = "SELECT * FROM posts"
    cur.execute(query)
    posts = cur.fetchall()
    return jsonify(posts), 200

# This is supposed to add a new post to the database
@bp.route('/addpost', methods=['POST', 'GET'])
def add_post():
    # data = request.get_json()
    cur = db.cursor()
    post = Post(user_id=3, course_id=2, title='My First Post', content='Hello, world!', time_created=datetime.now(), answer_count=0) #Adding to the database
    insert_query = "INSERT INTO posts (user_id, course_id, post_title, post_content, time_created, answer_count) VALUES (%s, %s, %s, %s, %s, %s)"
    insert_values = (post.user_id, post.course_id, post.title, post.content, post.time_created, post.answer_count)
    cur.execute(insert_query, insert_values)
    post_id = cur.lastrowid
    db.commit()

    # Generate automatic answer after post is created
    ai_answer = rule_based.generate(post.content, post.course_id, db)
    if ai_answer == "N/A":
        ai_answer = gpt_api.generate("What is O(n)?")
    answer = Answer(post_id= post_id, user_id=3, content=ai_answer, time_created=datetime.now())
    insert_query = "INSERT INTO answers (post_id, user_id, answer_content, time_created) VALUES (%s, %s, %s, %s)"
    insert_values = (answer.post_id, answer.user_id, answer.content, answer.time_created)
    cur.execute(insert_query, insert_values)
    db.commit()

    return "Success!"#jsonify(post.to_dict()), 201

# This is supposed to retrieve a specific post based off of a unique identifier
@bp.route('/post/<int:id>', methods=['GET'])
def get_specific_post(id):
    post = Post.query.get_or_404(id) #Retrieving the specific post
    return jsonify(post.to_dict()), 200

# This is supposed to allow updating of posts given the posts unique identifier
@bp.route('/updatepost/<int:id>', methods=['PUT'])
def update_post(id):
    post = Post.query.get_or_404(id)#Queries to retrieve the specific post needed to be updated
    data = request.get_json()
    post.title = data['title']
    post.description = data['description']
    db.session.commit()
    return jsonify(post.to_dict()), 200

#Deleting the post given the unique identifier
@bp.route('/deletepost/<int:id>', methods=['DELETE'])
def delete_book(id):
    post = Post.query.get_or_404(id) #Querying and deleting post
    db.session.delete(post)
    db.session.commit()
    return '', 204