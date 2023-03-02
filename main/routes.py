from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return 'blueprint test'


@main.route('/get-posts')
def getPosts():
    return 'Yet to be coded'