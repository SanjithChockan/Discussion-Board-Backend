import re

# Define a function to query the database and retrieve the rules for a given course
def generate(user_input, course_id, db):
    # Connect to the database and execute a query to retrieve the rules for the given course
    cur = db.cursor()
    cur.execute("SELECT pattern, rule FROM rules")
    rules = dict(cur.fetchall())
    response = ""
    for pattern, response in rules.items():
        if re.search(pattern, user_input, re.IGNORECASE):
            return response
    cur.close()
    return "N/A"

