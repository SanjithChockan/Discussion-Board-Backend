class Answer:
    def __init__(self, post_id, user_id, content, time_created, answer_id=-1):
        self.answer_id = answer_id
        self.post_id = post_id
        self.user_id = user_id
        self.answer_content = content
        self.time_created = time_created


class Post:
    def __init__(
        self, user_id, course_id, title, content, time_created, answer_count, post_id=-1
    ):
        self.post_id = post_id
        self.user_id = user_id
        self.course_id = course_id
        self.post_title = title
        self.post_content = content
        self.time_created = time_created
        self.answer_count = answer_count


class Course:
    def __init__(self, course_number, title, course_id=-1):
        self.course_number = course_number
        self.course_title = title
        self.course_id = course_id


class User:
    def __init__(self, username, email, user_id=-1):
        self.username = username
        self.email = email
        # self.password = password
        self.user_id = user_id
