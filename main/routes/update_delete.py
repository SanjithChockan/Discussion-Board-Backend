from flask import jsonify, request, Blueprint
from ..models import *
from datetime import datetime
update_delete_bp = Blueprint('update_delete', __name__)
from app import db

# Edit post
@update_delete_bp.route('/edit_post/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()
    cur = db.cursor()
    db.session.commit()
    #return jsonify(post.to_dict()), 200

# Edit answer
@update_delete_bp.route('/edit_answer/<int:id>', methods=['PUT'])
def update_answer(id):
    data = request.get_json()
    cur = db.cursor()
    db.session.commit()
    #return jsonify(post.to_dict()), 200

# Delete post
@update_delete_bp.route('/delete_post/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get_or_404(id) #Querying and deleting post
    db.session.delete(post)
    db.session.commit()
    return '', 204

# Delete answer
@update_delete_bp.route('/delete_answer/<int:id>', methods=['DELETE'])
def delete_answer(id):
    post = Post.query.get_or_404(id) #Querying and deleting post
    db.session.delete(post)
    db.session.commit()
    return '', 204