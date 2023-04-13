from main.models import *


# Turn posts into the Post class and dictize, then add to list
def format_post_return(sql_posts, cur):
    posts = []
    for row in sql_posts:
        post = Post(row[1], row[2], row[3], row[4], row[5], row[6], row[0])
        posts.append(post.__dict__)

    for i, post in enumerate(posts):
        # Get Course info
        course_id = post["course_id"]
        query = f"SELECT course_id, course_number, title FROM courses WHERE course_id = {course_id}"

        cur.execute(query)
        sql_course = cur.fetchone()

        course = Course(sql_course[1], sql_course[2], sql_course[0])

        # Get User info
        user_id = post["user_id"]
        query = f"SELECT user_id, username, email FROM users WHERE user_id = {user_id}"

        cur.execute(query)
        sql_user = cur.fetchone()

        user = User(sql_user[1], sql_user[2], sql_user[0])

        posts[i].update(course.__dict__)
        posts[i].update(user.__dict__)

    return posts


# Format course return
def format_course_return(sql_courses):
    courses = []
    for row in sql_courses:
        course = Course(row[1], row[2], row[0])
        courses.append(course.__dict__)

    return courses
