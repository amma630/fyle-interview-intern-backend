from flask import Blueprint
from core import db
from core.libs import assertions
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentGradeSchema

teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)

@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns a list of assignments for the authenticated teacher."""

    # Ensure the teacher ID is present
    assertions.assert_valid(p.teacher_id, "Teacher ID is required.")

    # Fetch assignments for the authenticated teacher
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)

    # Serialize the assignments data
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)

    return APIResponse.respond(data=teachers_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grades an assignment for the authenticated teacher."""
    
    # Ensure payload is provided
    assertions.assert_valid(incoming_payload, "Missing payload.")

    # Validate the incoming payload for grading an assignment
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    # Fetch the assignment by ID
    assignment_with_payload = Assignment.get_by_id(grade_assignment_payload.id)

    # Ensure the assignment exists
    assertions.assert_found(assignment_with_payload, "Assignment not found.")

    # Ensure the authenticated teacher owns the assignment
    assertions.assert_valid(
        p.teacher_id == assignment_with_payload.teacher_id,
        "Assignment was submitted to another teacher."
    )

    # Proceed to grade the assignment after all validations
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )

    # Commit changes to the database
    db.session.commit()

    # Serialize the graded assignment data
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)

    return APIResponse.respond(data=graded_assignment_dump)
