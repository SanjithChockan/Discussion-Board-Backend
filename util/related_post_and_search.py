import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import mysql.connector
from typing import List

threshold = 0.3


def cosine_similarity(posts, index, text):
    # Create a TfidfVectorizer to convert text to numerical vectors
    vectorizer = TfidfVectorizer(stop_words=None)

    # Create a list of all post contents and a dictionary mapping ids to indices
    all_posts = [post[index] for post in posts]

    # Create a matrix of all post contents
    post_matrix = vectorizer.fit_transform(all_posts)

    # Convert target post to numerical vector
    target_vector = vectorizer.transform([text])

    # Calculate cosine similarity between target post and all other posts
    similarities = np.dot(post_matrix, target_vector.T).toarray().flatten()

    # Sort similarities in descending order and get indices of top posts
    top_indices = similarities.argsort()[::-1]

    # Retrieve the ids of the top posts
    scores = [[posts[i][0], similarities[i]] for i in top_indices]

    # Return the ids of the top posts
    return scores


def find_most_related_posts(
    target_post_id: int, n: int, db: mysql.connector.connection.MySQLConnection
) -> List[int]:
    # Create a TfidfVectorizer to convert text to numerical vectors
    vectorizer = TfidfVectorizer(stop_words="english")

    # Retrieve the content and course ID of the target post from the MySQL database
    cursor = db.cursor()
    query = "SELECT title, content, course_id FROM posts WHERE post_id = %s"
    params = (target_post_id,)
    cursor.execute(query, params)
    target_post_title, target_post_content, target_post_course_id = cursor.fetchone()
    cursor.close()

    # Retrieve all posts in the same course as the target post from the MySQL database
    cursor = db.cursor()
    query = "SELECT post_id, title, content, course_id FROM posts WHERE course_id = %s AND post_id <> %s LIMIT %s"
    params = (target_post_course_id, target_post_id, n)
    cursor.execute(query, params)
    posts = cursor.fetchall()
    cursor.close()

    content_scores = cosine_similarity(posts, 2, target_post_content)
    title_scores = cosine_similarity(posts, 1, target_post_title)
    scale = 5

    combined_scores = {}
    for id, score in content_scores:
        if id not in combined_scores:
            combined_scores[id] = score * 1
        else:
            combined_scores[id] += score * 1
    for id, score in title_scores:
        if id not in combined_scores:
            combined_scores[id] = score * scale
        else:
            combined_scores[id] += score * scale

    keys_to_delete = [
        id for id in combined_scores if combined_scores[id] < (1 + 5) * threshold
    ]
    [combined_scores.pop(id) for id in keys_to_delete]

    # Sort dictionary by value (score) in descending order
    sorted_scores = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

    # Extract sorted list of ids
    sorted_ids = [item[0] for item in sorted_scores]
    return sorted_ids


def lookup_related_posts(
    search_sentence: str, n: int, db: mysql.connector.connection.MySQLConnection
) -> List[int]:
    # Retrieve all posts from the MySQL database
    cursor = db.cursor()
    query = "SELECT post_id, title, content, course_id FROM posts"
    cursor.execute(query)
    posts = cursor.fetchall()
    cursor.close()

    content_scores = cosine_similarity(posts, 2, search_sentence)
    title_scores = cosine_similarity(posts, 1, search_sentence)
    scale = 5

    combined_scores = {}
    for id, score in content_scores:
        if id not in combined_scores:
            combined_scores[id] = score * 1
        else:
            combined_scores[id] += score * 1
    for id, score in title_scores:
        if id not in combined_scores:
            combined_scores[id] = score * scale
        else:
            combined_scores[id] += score * scale

    keys_to_delete = [
        id for id in combined_scores if combined_scores[id] < (1 + 5) * threshold
    ]
    [combined_scores.pop(id) for id in keys_to_delete]

    # Sort dictionary by value (score) in descending order
    sorted_scores = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

    # Extract sorted list of ids
    sorted_ids = [item[0] for item in sorted_scores]
    return sorted_ids
