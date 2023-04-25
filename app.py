from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from util.gpt_api import generate_answer

# from util.gpt_api import generate_answer
# import aws_credentials as rds
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})

# set sql alchemy database uri like this 'mysql+pymysql://username:password@host/database'

host = os.environ.get("DATABASE_HOST")
username = os.environ.get("DATABASE_USER")
pw = os.environ.get("DATABASE_PASSWORD")
db_name = os.environ.get("DATABASE_NAME")

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{username}:{pw}@{host}:3306/{db_name}"
app.config["JWT_SECRET_KEY"] = "your-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=1440)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Importing CRUD blueprints
from main.routes import read_posts, read_other, create, update_delete, auth, votes

app.register_blueprint(read_posts.read_posts_bp)
app.register_blueprint(read_other.read_other_bp)
app.register_blueprint(create.create_bp)
app.register_blueprint(update_delete.update_delete_bp)
app.register_blueprint(auth.auth_blueprint, url_prefix="/auth")
app.register_blueprint(votes.votes_bp)


# Testing generating answer based on chat gpt
@app.route("/")
def index():
    #print(generate_answer('When is my final exam', 5))
    # print(generate_answer("when is office hours"))
    return "hello!"
