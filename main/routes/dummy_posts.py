#Code to just fill in databases
from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models import *
from util import rule_based, gpt_api
from datetime import datetime
from ..errors import BadRequestError
import random

create_fake_bp = Blueprint("dummy_posts", __name__)

@create_fake_bp.route("/create_fake", methods=["POST"])
#@jwt_required()
def create_post():
    data = request.get_json()

    user_id = data['id']
    student_id = data['id']
    potential_title = ["Homework", 
                       "Office hours", 
                       "Quiz",
                       "Room number",
                       "Contanct information",
                       "Late policy",
                       "Exam percentage",
                       "Exam date",
                       "Time of class",
                       ]
    potential_content = [
        "What is the homework percentage?",
        "When are the office hours?",
        "What is the quiz percentage?",
        "What is the room number?",
        "What is the email of the professor",
        "What is the late policy?",
        "What is the exam percentage",
        "When is the exam?",
        "What is the class time?",
    ]

    # Get course IDs that the student is registered for
    course_ids = [registration.course_id for registration in Registration.query.filter_by(student_id=student_id).all()]

    # Create a new post for each course
    posts = []
    for course_id in course_ids:
        post_index = random.randint(0, len(potential_content)-1)
        title = potential_title[post_index]
        content = potential_content[post_index]
        post = Post(
            user_id=user_id,
            course_id=course_id,
            post_title=title,
            post_content=content,
            answer_count=1,
        )
        db.session.add(post)
        db.session.commit()

        # Generate automatic answer after post is created
        ai_answer = rule_based.generate(post.post_content, post.course_id, db)
        print(ai_answer)
        if ai_answer == "N/A":
            ai_answer = gpt_api.generate(post.post_content)

        answer = Answer(
            post_id=post.post_id,
            user_id=3,
            answer_content=ai_answer,
            parent_answer=None,
        )
        db.session.add(answer)
        db.session.commit()

        posts.append(post.serialize())

    # Return list of created posts
    return jsonify(posts), 201
