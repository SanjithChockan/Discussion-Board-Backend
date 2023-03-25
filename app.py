from flask import Flask
from main.routes import *
from main.errors import *

app = Flask(__name__)

if __name__ == "__main__":
  app.run(debug=True)