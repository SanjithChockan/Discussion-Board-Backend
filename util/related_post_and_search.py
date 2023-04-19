import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List
import os

threshold = 0.1
scale = 5

# Define your database URI
host = os.environ.get("DATABASE_HOST")
username = os.environ.get("DATABASE_USER")
pw = os.environ.get("DATABASE_PASSWORD")
db_name = os.environ.get("DATABASE_NAME")

db_uri = f"mysql+pymysql://{username}:{pw}@{host}:3306/{db_name}"

# Create the SQLAlchemy engine
engine = create_engine(db_uri)

# Define the Post class to represent the posts table
Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True)
    post_title = Column(String)
    post_content = Column(String)
    course_id = Column(Integer)


# Create a session factory and a session
Session = sessionmaker(bind=engine)


def cosine_similarity(posts, choice, text):
    # Create a TfidfVectorizer to convert text to numerical vectors
    vectorizer = TfidfVectorizer(stop_words=None)

    # Create a list of all post contents and a dictionary mapping ids to indices
    if choice == "content":
        all_posts = [post.post_content for post in posts]
    else:
        all_posts = [post.post_title for post in posts]
    post_matrix = vectorizer.fit_transform(all_posts)
    target_vector = vectorizer.transform([text])
    similarities = np.dot(post_matrix, target_vector.T).toarray().flatten()

    # Sort similarities in descending order and get indices of top posts
    top_indices = similarities.argsort()[::-1]
    scores = [[posts[i].post_id, similarities[i]] for i in top_indices]

    # Return the ids of the top posts
    return scores


def find_most_related_posts(target_post_id: int, n: int) -> List[int]:
    # Create a TfidfVectorizer to convert text to numerical vectors
    vectorizer = TfidfVectorizer(stop_words="english")
    session = Session()
    # Retrieve the content and course ID of the target post from the database
    target_post = session.query(Post).filter(Post.post_id == target_post_id).one()
    target_post_title, target_post_content, target_post_course_id = (
        target_post.post_title,
        target_post.post_content,
        target_post.course_id,
    )

    # Retrieve all posts in the same course as the target post from the database
    posts = (
        session.query(Post)
        .filter(Post.course_id == target_post_course_id, Post.post_id != target_post_id)
        .limit(n)
        .all()
    )

    content_scores = cosine_similarity(posts, "content", target_post_content)
    title_scores = cosine_similarity(posts, "title", target_post_title)

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
        id for id in combined_scores if combined_scores[id] < (1 + scale) * threshold
    ]
    [combined_scores.pop(id) for id in keys_to_delete]

    # Sort dictionary by value (score) in descending order
    sorted_scores = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

    # Extract sorted list of ids
    sorted_ids = [item[0] for item in sorted_scores]
    return sorted_ids


def lookup_related_posts(search_sentence: str, n: int) -> List[int]:
    # Retrieve all posts from the MySQL database
    session = Session()
    posts = session.query(Post).all()

    content_scores = cosine_similarity(posts, "content", search_sentence)
    title_scores = cosine_similarity(posts, "title", search_sentence)

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
        id for id in combined_scores if combined_scores[id] < (1 + scale) * threshold
    ]
    [combined_scores.pop(id) for id in keys_to_delete]

    # Sort dictionary by value (score) in descending order
    sorted_scores = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

    # Extract sorted list of ids
    sorted_ids = [item[0] for item in sorted_scores]
    return sorted_ids
