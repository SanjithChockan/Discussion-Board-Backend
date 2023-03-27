from flask import jsonify, request
from main import app
from main.models import *

#This is supposed to retrieve all the posts from the database
@app.route('/getposts', methods=['GET'])
def get_posts():
    posts = request.get_data #Query the database 
    return jsonify([posts.to_dict() for post in posts]), 200

#This is supposed to add a new post to the database
@app.route('/addpost', methods=['POST'])
def add_post():
    data = request.get_json()
    new_post = Post(title=data['title'], description=data['description']) #Adding to the database
    db.session.add(new_post)
    db.session.commit()
    return jsonify(new_post.to_dict()), 201

#This is supposed to retrieve a specific post based off of a unique identifier
@app.route('/post/<int:id>', methods=['GET'])
def get_specific_post(id):
    post = Post.query.get_or_404(id) #Retrieving the specific post
    return jsonify(post.to_dict()), 200

#This is supposed to allow updating of posts given the posts unique identifier
@app.route('/updatepost/<int:id>', methods=['PUT'])
def update_post(id):
    post = Post.query.get_or_404(id)#Queries to retrieve the specific post needed to be updated
    data = request.get_json()
    post.title = data['title']
    post.description = data['description']
    db.session.commit()
    return jsonify(post.to_dict()), 200

#Deleting the post given the unique identifier
@app.route('/deletepost/<int:id>', methods=['DELETE'])
def delete_book(id):
    post = Post.query.get_or_404(id) #Querying and deleting post
    db.session.delete(post)
    db.session.commit()
    return '', 204