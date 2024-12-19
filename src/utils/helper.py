from flask import Response
from http import HTTPStatus
import logging, json

def handle_error(e):
    error_message = str(e.args[0]) if e.args else 'An error occurred'
    status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
    logging.exception(error_message)
    return Response(
        json.dumps({'error': error_message, 'status': status_code}),
        status=status_code, mimetype='application/json'
    )
