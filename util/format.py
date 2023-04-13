from main.models import *


# Turn posts into the Post class and dictize, then add to list
def format_post_return(sql_posts):
    posts = []
    for row in sql_posts:
        post = Post(row[1], row[2], row[3], row[4], row[5], row[6], row[0])
        posts.append(post.__dict__)

    return posts


# Format course return
def format_course_return(sql_courses):
    courses = []
    for row in sql_courses:
        course = Course(row[1], row[2], row[0])
        courses.append(course.__dict__)

    return courses
