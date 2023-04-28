from flask import jsonify


class BadRequestError(Exception):
    def __init__(self, message):
        self.message = message


class NotFoundError(Exception):
    def __init__(self, message):
        self.message = message


def handle_bad_request_error(error):
    response = jsonify({"error": error.message})
    response.status_code = 400
    return response


def handle_not_found_error(error):
    response = jsonify({"error": error})
