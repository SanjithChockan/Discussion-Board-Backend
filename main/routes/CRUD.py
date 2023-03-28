from flask import jsonify, request, Blueprint
import sys
bp = Blueprint('CRUD', __name__)
from ..models import Post, db
from datetime import datetime

# This is supposed to retrieve all the posts from the database
@bp.route('/getposts', methods=['GET'])
def get_posts():
    ## Add code to select posts from specific course, get courseID from request data
    # data = request.get_json()
    cur = db.cursor()
    query = "SELECT * FROM Posts"
    cur.execute(query)
    posts = cur.fetchall()
    return jsonify(posts), 200

# This is supposed to add a new post to the database
@bp.route('/addpost', methods=['POST', 'GET'])
def add_post():
    # data = request.get_json()
    cur = db.cursor()
    post = Post(id = 0, user_id=1, course_id=2, title='My First Post', content='Hello, world!', time_created=datetime.now(), answer_count=0) #Adding to the database
    insert_query = "INSERT INTO Posts (PostID, UserID, CourseID, PostTitle, PostContent, TimeCreated, AnswerCount) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    insert_values = (post.id, post.user_id, post.course_id, post.title, post.content, post.time_created, post.answer_count)
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