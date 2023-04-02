from flask import jsonify, request, Blueprint
from ..models import *
from intelligent_answering import rule_based, gpt_api
from datetime import datetime
create_bp = Blueprint('create', __name__)
from app import db

# Create post and generate AI answer
# !!! Need to change to 'POST' only after testing
@create_bp.route('/create_post', methods=['POST', 'GET'])
def create_post():
    # data = request.get_json()
    cur = db.cursor()
    post = Post(user_id=3, course_id=2, title='My First Post', content='When is the exam date?', time_created=datetime.now(), answer_count=0) #Adding to the database
    insert_query = "INSERT INTO posts (user_id, course_id, post_title, post_content, time_created, answer_count) VALUES (%s, %s, %s, %s, %s, %s)"
    insert_values = (post.user_id, post.course_id, post.title, post.content, post.time_created, post.answer_count)
    cur.execute(insert_query, insert_values)
    post_id = cur.lastrowid
    db.commit()

    # Generate automatic answer after post is created
    ai_answer = rule_based.generate(post.content, post.course_id, db)
    print(ai_answer)
    if ai_answer == "N/A":
        ai_answer = gpt_api.generate("What is O(n)?")
    answer = Answer(post_id=post_id, user_id=3, content=ai_answer, time_created=datetime.now())
    insert_query = "INSERT INTO answers (post_id, user_id, answer_content, time_created) VALUES (%s, %s, %s, %s)"
    insert_values = (answer.post_id, answer.user_id, answer.content, answer.time_created)
    cur.execute(insert_query, insert_values)
    db.commit()

    return jsonify(ai_answer), 201

# Create answer (from user)
# !!! Need to change to 'POST' only after testing
@create_bp.route('/create_answer', methods=['POST', 'GET'])
def create_answer():
    # data = request.get_json()

    return
