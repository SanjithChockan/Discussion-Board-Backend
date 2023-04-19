from app import db


class Answers(db.Model):
    answer_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    answer_content = db.Column(db.Text, nullable=False)
    time_created = db.Column(db.DateTime, nullable=False)

    post = db.relationship("Posts", backref=db.backref("answers", lazy=True))
    user = db.relationship("Users", backref=db.backref("answers", lazy=True))

    def serialize(self):
        return {
            "id": self.answer_id,
            "post_id": self.post_id,
            "answer_content": self.answer_content,
            "user_id": self.user_id,
            "created_at": self.time_created
        }


class Posts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.course_id"))
    post_title = db.Column(db.String(255), nullable=False)
    post_content = db.Column(db.Text, nullable=False)
    time_created = db.Column(db.DateTime, nullable=False)
    answer_count = db.Column(db.Integer, nullable=False)

    course = db.relationship("Courses", backref=db.backref("posts", lazy=True))
    user = db.relationship("Users", backref=db.backref("posts", lazy=True))

    def serialize(self):
        return {
            "post_id": self.post_id,
            "user_id": self.user_id,
            "course_id": self.course_id,
            "title": self.post_title,
            "post_content": self.post_content,
            "time_created": self.time_created.isoformat(),
            "answer_count": self.answer_count,
            "course": {
                "course_id": self.course.course_id,
                "course_number": self.course.course_number,
                "course_title": self.course.course_title,
            },
            "user": {
                "user_id": self.user.user_id,
                "username": self.user.username,
                "email": self.user.email,
            },
        }


class Courses(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    course_number = db.Column(db.String(50), nullable=False, unique=True)
    course_title = db.Column(db.String(255), nullable=False)

    def serialize(self):
        return {
            "course_id": self.course_id,
            "course_number": self.course_number,
            "course_title": self.course_title,
        }


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
