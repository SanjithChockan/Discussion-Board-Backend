from app import db


class Answer(db.Model):
    __tablename__ = "answers"

    answer_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    answer_content = db.Column(db.Text, nullable=False)
    time_created = db.Column(db.DateTime, nullable=False)

    post = db.relationship("Post", backref=db.backref("answers", lazy=True))
    user = db.relationship("User", backref=db.backref("answers", lazy=True))

    def serialize(self):
        return {
            "answer_id": self.answer_id,
            "post_id": self.post_id,
            "answer_content": self.answer_content,
            "user_id": self.user_id,
            "created_at": self.time_created,
        }


class Post(db.Model):
    __tablename__ = "posts"

    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.course_id"))
    post_title = db.Column(db.String(255), nullable=False)
    post_content = db.Column(db.Text, nullable=False)
    time_created = db.Column(db.DateTime, nullable=False)
    answer_count = db.Column(db.Integer, nullable=False)

    course = db.relationship("Course", backref=db.backref("posts", lazy=True))
    user = db.relationship("User", backref=db.backref("posts", lazy=True))

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


class Course(db.Model):
    __tablename__ = "courses"

    course_id = db.Column(db.Integer, primary_key=True)
    course_number = db.Column(db.String(50), nullable=False, unique=True)
    course_title = db.Column(db.String(255), nullable=False)

    def serialize(self):
        return {
            "course_id": self.course_id,
            "course_number": self.course_number,
            "course_title": self.course_title,
        }


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)


class Student(db.Model):
    __tablename__ = "students"

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)

    user = db.relationship("User", backref=db.backref("students", uselist=False))


class Professor(db.Model):
    __table__name = "professors"

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.course_id"))

    user = db.relationship("User", backref=db.backref("professors", uselist=False))
    course = db.relationship("Course", backref=db.backref("professors", uselist=False))


class Registration(db.Model):
    __tablename__ = "registrations"

    student_id = db.Column(
        db.Integer, db.ForeignKey("students.user_id"), primary_key=True
    )
    course_id = db.Column(
        db.Integer, db.ForeignKey("courses.course_id"), primary_key=True
    )

    student = db.relationship("Student", backref=db.backref("registrations"))
    course = db.relationship("Course", backref=db.backref("registrations"))


class Rules(db.Model):
    __tablename__ = "rules"

    rule_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, nullable=False)
    pattern = db.Column(db.String(255), nullable=False)
    rule = db.Column(db.String(255), nullable=False)
