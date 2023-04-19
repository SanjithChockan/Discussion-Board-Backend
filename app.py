from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# import aws_credentials as rds
import os

app = Flask(__name__)
CORS(app)

# set sql alchemy database uri like this 'mysql+pymysql://username:password@host/database'

host = os.environ.get("DATABASE_HOST")
username = os.environ.get("DATABASE_USER")
pw = os.environ.get("DATABASE_PASSWORD")
db_name = os.environ.get("DATABASE_NAME")

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{username}:{pw}@{host}:3306/{db_name}"

db = SQLAlchemy(app)

# Importing CRUD blueprints
from main.routes.read_posts import *
from main.routes.read_other import *
from main.routes.create import *
from main.routes.update_delete import *

app.register_blueprint(read_posts_bp)
app.register_blueprint(read_other_bp)
app.register_blueprint(create_bp)
app.register_blueprint(update_delete_bp)


@app.route("/")
def index():
    posts = Posts.query.all()
    return jsonify([post.serialize() for post in posts]), 200
