import re
from main.models import *

# Define a function to query the database and retrieve the rules for a given course
def generate(user_input, course_id, db):
    # Connect to the database and execute a query to retrieve the rules for the given course
    rules = Rules.query.filter_by(course_id=course_id).all()
    for rule in rules:
        if re.search(rule.pattern, user_input, re.IGNORECASE):
            return rule.rule
        
    return "N/A"

