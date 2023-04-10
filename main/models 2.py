class Answer:
    def __init__(self, post_id, user_id, content, time_created):
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        self.time_created = time_created

class Post:
    def __init__(self, user_id, course_id, title, content, time_created, answer_count):
        self.user_id = user_id
        self.course_id = course_id
        self.title = title
        self.content = content
        self.time_created = time_created
        self.answer_count = answer_count