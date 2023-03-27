from flask import Flask

app = Flask(__name__)

# app.config['SECRET_KEY'] = 'mysecretkey'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
@app.route('/')
def index():
    return "Hey Testing"

from main import routes, models, errors