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

from main.routes import CRUD
app.register_blueprint(CRUD.bp)

@app.route('/')
def index():
    cur = db.cursor()
    cur.execute('''SELECT * FROM Answers''')
    data = cur.fetchall()
    cur.close()
    return str(data)

if __name__ == "__main__":
  app.run(debug=True)