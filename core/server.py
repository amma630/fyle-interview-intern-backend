from flask import jsonify
from marshmallow.exceptions import ValidationError
from core import app
from core.apis.assignments import (
    student_assignments_resources,
    teacher_assignments_resources,
    principal_assignments_resources
)
from core.apis.teachers import principal_teachers_resources
from core.libs import helpers
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

# Register blueprints
app.register_blueprint(student_assignments_resources, url_prefix='/student')
app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')
app.register_blueprint(principal_assignments_resources, url_prefix='/principal')
app.register_blueprint(principal_teachers_resources, url_prefix='/principals')

@app.route('/')
def ready():
    """Health check endpoint."""
    return jsonify({
        'status': 'ready',
        'time': helpers.get_utc_now()
    }), 200

@app.errorhandler(Exception)
def handle_error(err):
    """Generic error handler."""
    error_messages = {
        FyleError: (lambda e: (e.message, e.status_code)),
        ValidationError: (lambda e: (e.messages, 400)),
        IntegrityError: (lambda e: (str(e.orig), 400)),
        HTTPException: (lambda e: (str(e), e.code))
    }

    # Use .get to avoid KeyError and handle unknown exceptions gracefully
    error_response = error_messages.get(type(err), lambda e: (str(e), 500))(err)

    # Log the error for debugging (consider using logging module)
    app.logger.error(f"Error occurred: {error_response[0]}")

    return jsonify(error=err.__class__.__name__, message=error_response[0]), error_response[1]
