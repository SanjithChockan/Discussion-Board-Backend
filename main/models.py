from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
    id = db.Column('PostID', db.Integer, primary_key=True)
    user_id = db.Column('UserID', db.ForeignKey('UserID'), nullable=False)
    course_id = db.Column('CourseID', db.ForeignKey('CourseID'), nullable=False)
    title = db.Column('PostTitle', db.String(255), nullable=False)
    content = db.Column('PostContent', db.Text, nullable=False)
    time_created = db.Column('TimeCreated', db.TIMESTAMP, nullable=False)
    answer_count = db.Column('AnswerCount', db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Post {self.id}: {self.title}>'