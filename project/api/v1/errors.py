from flask import jsonify


class ApiError(Exception):

    def __init__(self, message, status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload or ()

    def get_response(self):
        rv = dict(self.payload)
        rv['message'] = self.message
        return jsonify(rv), self.status_code
