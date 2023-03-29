import re

# Define a function to query the database and retrieve the rules for a given course
def generate(user_input, course, db):
    # Connect to the database and execute a query to retrieve the rules for the given course
    cur = db.cursor()
    cur.execute("SELECT pattern, response FROM rules WHERE course = ?", (course,))
    rules = dict(cur.fetchall())
    for pattern, response in rules.items():
        if re.match(pattern, user_input):
            return response
    return "N/A"

