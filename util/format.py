from main.models import *


def format_post_return(sql_posts, cur):
    # Construct SQL query to retrieve all necessary information for each post
    query = """
        SELECT 
            p.post_id, 
            p.user_id, 
            p.course_id, 
            p.title, 
            p.content, 
            p.time_created, 
            p.answer_count, 
            c.course_number, 
            c.title AS course_title, 
            u.username, 
            u.email
        FROM 
            posts AS p 
            JOIN courses AS c ON p.course_id = c.course_id 
            JOIN users AS u ON p.user_id = u.user_id 
        WHERE 
            p.post_id IN (%s)
    """
    # Get a list of all the post IDs to retrieve information for
    post_ids = [row[0] for row in sql_posts]
    # Use a placeholder in the query for each post ID
    placeholders = ", ".join(["%s" for _ in post_ids])
    query = query % placeholders

    # Execute the query with the list of post IDs as a parameter
    cur.execute(query, post_ids)
    sql_results = cur.fetchall()

    posts = []

    # Loop over the query results and create objects for each row
    for row in sql_results:
        # Create Course and User objects
        course = Course(row[7], row[8], row[2])
        user = User(row[9], row[10], row[1])

        # Create Post object
        post = Post(row[1], row[2], row[3], row[4], row[5], row[6], row[0])

        # Add Course and User objects to Post object
        post.course = course.__dict__
        post.user = user.__dict__

        # Add Post object to list
        posts.append(post.__dict__)

    return posts


# Format course return
def format_course_return(sql_courses):
    courses = []
    for row in sql_courses:
        course = Course(row[1], row[2], row[0])
        courses.append(course.__dict__)

    return courses
