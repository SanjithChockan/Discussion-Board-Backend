from flask import Flask
from flask_cors import CORS
import mysql.connector

# import aws_credentials as rds
import os

app = Flask(__name__)
CORS(app)

app.config["MYSQL_HOST"] = os.environ.get("DATABASE_HOST")
app.config["MYSQL_USER"] = os.environ.get("DATABASE_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("DATABASE_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("DATABASE_NAME")

db = mysql.connector.connect(
    host=os.environ.get("DATABASE_HOST"),
    user=os.environ.get("DATABASE_USER"),
    password=os.environ.get("DATABASE_PASSWORD"),
    database=os.environ.get("DATABASE_NAME"),
)

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
    cur = db.cursor()
    cur.execute("""SELECT * FROM answers""")
    data = cur.fetchall()
    cur.close()
    return str(data)
