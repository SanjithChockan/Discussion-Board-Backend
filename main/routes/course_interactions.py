from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models import *
from util import rule_based, gpt_api
from datetime import datetime

courses_bp = Blueprint("courses", __name__)

# Register for list of courses
@courses_bp.route("/register", methods=["POST"])