from flask import Flask
import mysql.connector
import aws_credentials as rds

app = Flask(__name__)
app.config['MYSQL_HOST'] = rds.host
app.config['MYSQL_USER'] = rds.user
app.config['MYSQL_PASSWORD'] = rds.password
app.config['MYSQL_DB'] = rds.db

db = mysql.connector.connect(
  host=rds.host,
  user=rds.user,
  password=rds.password,
  database=rds.db
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