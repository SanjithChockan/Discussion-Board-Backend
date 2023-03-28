from flask_sqlalchemy import SQLAlchemy
from app import db

class Post:
    def __init__(self, id, user_id, course_id, title, content, time_created, answer_count):
        self.id = id
        self.user_id = user_id
        self.course_id = course_id
        self.title = title
        self.content = content
        self.time_created = time_created
        self.answer_count = answer_count
