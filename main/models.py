class Answer:
    def __init__(self, post_id, user_id, content, time_created, answer_id=-1):
        self.answer_id = answer_id
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        self.time_created = time_created


class Post:
    def __init__(
        self, user_id, course_id, title, content, time_created, answer_count, post_id=-1
    ):
        self.post_id = post_id
        self.user_id = user_id
        self.course_id = course_id
        self.title = title
        self.content = content
        self.time_created = time_created
        self.answer_count = answer_count


class Course:
    def __init__(self, course_number, title, course_id=-1):
        self.course_number = course_number
        self.title = title
        self.course_id = course_id
