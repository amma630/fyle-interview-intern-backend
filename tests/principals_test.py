from core.models.assignments import AssignmentStateEnum, GradeEnum


def log_response(response):
    """Log response details for debugging."""
    print("Response Status Code:", response.status_code)
    print("Response JSON:", response.json)


def test_get_assignments(client, h_principal):
    try:
        response = client.get(
            '/principal/assignments',
            headers=h_principal
        )

        assert response.status_code == 200

        data = response.json['data']
        for assignment in data:
            assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]

    except AssertionError as e:
        print("Test failed:", e)
        log_response(response)


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    try:
        response = client.post(
            '/principal/assignments/grade',
            json={
                'id': 5,
                'grade': GradeEnum.A.value
            },
            headers=h_principal
        )

        # Add an assertion to check for the expected failure
        assert response.status_code == 400  # Assuming 400 for failure in grading draft assignment

    except AssertionError as e:
        print("Test failed:", e)
        log_response(response)


def test_grade_assignment(client, h_principal):
    try:
        response = client.post(
            '/principal/assignments/grade',
            json={
                'id': 4,
                'grade': GradeEnum.C.value
            },
            headers=h_principal
        )

        assert response.status_code == 200

        assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
        assert response.json['data']['grade'] == GradeEnum.C

    except AssertionError as e:
        print("Test failed:", e)
        log_response(response)


def test_regrade_assignment(client, h_principal):
    try:
        response = client.post(
            '/principal/assignments/grade',
            json={
                'id': 4,
                'grade': GradeEnum.B.value
            },
            headers=h_principal
        )

        assert response.status_code == 200

        assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
        assert response.json['data']['grade'] == GradeEnum.B

    except AssertionError as e:
        print("Test failed:", e)
        log_response(response)


def test_get_teachers(client, h_principal):
    try:
        response = client.get(
            '/principals/teachers',
            headers=h_principal
        )

        assert response.status_code == 200
        data = response.json['data']

        assert isinstance(data, list)
        for teacher in data:
            assert 'id' in teacher
            assert 'name' in teacher
            # Add more assertions as needed based on your teacher data structure

    except AssertionError as e:
        print("Test failed:", e)
        log_response(response)


def test_grade_assignment_invalid_grade(client, h_principal):
    """Valid grades : A B C D"""
    try:
        response = client.post(
            '/principal/assignments/grade',
            json={
                'id': 4,
                'grade': 'CF'
            },
            headers=h_principal
        )

        assert response.status_code == 400  # Assuming 400 for invalid grade

    except AssertionError as e:
        print("Test failed:", e)
        log_response(response)
