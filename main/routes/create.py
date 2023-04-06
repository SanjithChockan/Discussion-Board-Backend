from flask import jsonify, request, Blueprint
from ..models import *
from util import rule_based, gpt_api
from datetime import datetime
create_bp = Blueprint('create', __name__)
from app import db

# Create post and generate AI answer
# !!! Need to change to 'POST' only after testing
@create_bp.route('/create_post', methods=['POST'])
def create_post():
    data = request.get_json()
    user_id = data['user_id']
    course_id = data['course_id']
    title = data['title']
    content = data['content']

    post = Post(user_id, course_id, title, content, time_created=datetime.now(), answer_count=1) #Adding to the database
    insert_query = "INSERT INTO posts (user_id, course_id, title, content, time_created, answer_count) VALUES (%s, %s, %s, %s, %s, %s)"
    insert_values = (post.user_id, post.course_id, post.title, post.content, post.time_created, post.answer_count)
    cur = db.cursor()
    cur.execute(insert_query, insert_values)
    post_id = cur.lastrowid
    db.commit()

    # Generate automatic answer after post is created
    ai_answer = rule_based.generate(post.content, post.course_id, db)
    print(ai_answer)
    if ai_answer == "N/A":
        ai_answer = gpt_api.generate("What is O(n)?")
    
    answer = Answer(post_id, 13, content=ai_answer, time_created=datetime.now())
    insert_query = "INSERT INTO answers (post_id, user_id, content, time_created) VALUES (%s, %s, %s, %s)"
    insert_values = (answer.post_id, answer.user_id, answer.content, answer.time_created)
    cur.execute(insert_query, insert_values)
    db.commit()

    return jsonify(ai_answer), 201

# Create answer (from user)
# !!! Need to change to 'POST' only after testing
@create_bp.route('/create_answer', methods=['POST'])
def create_answer():
    data = request.get_json()
    post_id = data['post_id']
    user_id = data['user_id']
    content = data['content']

    answer = Answer(post_id=post_id, user_id=user_id, content=content, time_created=datetime.now())
    insert_query = "INSERT INTO answers (post_id, user_id, content, time_created) VALUES (%s, %s, %s, %s)"
    insert_values = (answer.post_id, answer.user_id, answer.content, answer.time_created)
    cur = db.cursor()
    cur.execute(insert_query, insert_values)
    db.commit()

    return
