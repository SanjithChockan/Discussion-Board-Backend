from flask import Flask
from flask_cors import CORS
import mysql.connector
#import aws_credentials as rds
import os

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = os.environ.get('host')
app.config['MYSQL_USER'] = os.environ.get('user')
app.config['MYSQL_PASSWORD'] = os.environ.get('password')
app.config['MYSQL_DB'] = os.environ.get('db')

db = mysql.connector.connect(
  host=os.environ.get('host'),
  user=os.environ.get('user'),
  password=os.environ.get('password'),
  database=os.environ.get('db')
)

# Importing CRUD blueprints
from main.routes.read import *
from main.routes.create import *
from main.routes.update_delete import *
app.register_blueprint(read_bp)
app.register_blueprint(create_bp)
app.register_blueprint(update_delete_bp)

@app.route('/')
def index():
    cur = db.cursor()
    cur.execute('''SELECT * FROM answers''')
    data = cur.fetchall()
    cur.close()
    return str(data)