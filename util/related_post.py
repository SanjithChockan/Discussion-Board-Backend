import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import mysql.connector
from typing import List

def find_most_related_posts(target_post_id: int, n: int, db: mysql.connector.connection.MySQLConnection) -> List[int]:
    # Create a TfidfVectorizer to convert text to numerical vectors
    vectorizer = TfidfVectorizer(stop_words='english')

    # Retrieve the content and course ID of the target post from the MySQL database
    cursor = db.cursor()
    query = "SELECT content, course_id FROM posts WHERE post_id = %s"
    params = (target_post_id,)
    cursor.execute(query, params)
    target_post_content, target_post_course_id = cursor.fetchone()
    cursor.close()

    # Retrieve all posts in the same course as the target post from the MySQL database
    cursor = db.cursor()
    query = "SELECT post_id, content FROM posts WHERE course_id = %s AND post_id <> %s"
    params = (target_post_course_id, target_post_id)
    cursor.execute(query, params)
    posts = cursor.fetchall()
    cursor.close()

    # Create a list of all post contents and a dictionary mapping ids to indices
    all_posts = [post[1] for post in posts]
    id_to_index = {post[0]: i for i, post in enumerate(posts)}

    # Create a matrix of all post contents
    post_matrix = vectorizer.fit_transform(all_posts)

    # Convert target post to numerical vector
    target_vector = vectorizer.transform([target_post_content])

    # Calculate cosine similarity between target post and all other posts
    similarities = np.dot(post_matrix, target_vector.T).toarray().flatten()

    # Sort similarities in descending order and get indices of top n posts
    if n > len(posts):
        top_n_indices = similarities.argsort()[::-1]
    else:
        top_n_indices = similarities.argsort()[::-1][:n]

    # Retrieve the ids of the top n posts
    top_n_ids = [posts[i][0] for i in top_n_indices]

    # Return the ids of the top n posts
    return top_n_ids
