def test_get_assignments_student_1(client, h_student_1):
    response = client.get('/student/assignments', headers=h_student_1)

    assert response.status_code == 200
    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1

def test_get_assignments_student_2(client, h_student_2):
    response = client.get('/student/assignments', headers=h_student_2)

    assert response.status_code == 200
    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2

def test_post_assignment_null_content(client, h_student_1):
    """Failure case: content cannot be null."""
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={'content': None}
    )

    assert response.status_code == 400

def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={'content': content}
    )

    assert response.status_code == 200
    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None

def test_submit_assignment_student_1(client, h_student_1):
    # First, create a draft assignment
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={'content': 'Test Assignment'}
    )
    
    assert response.status_code == 200, "Expected status code 200 for creating assignment."

    assignment_id = response.json['data']['id']  # Get the newly created assignment ID

    # Now, submit the newly created assignment
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={'id': assignment_id, 'teacher_id': 2}
    )

    assert response.status_code == 200, "Expected status code 200 for successful submission."
    
    data = response.json['data']
    assert data['student_id'] == 1, f"Expected student_id 1, got {data['student_id']}"
    assert data['state'] == 'SUBMITTED', f"Expected state 'SUBMITTED', got '{data['state']}'"
    assert data['teacher_id'] == 2, f"Expected teacher_id 2, got {data['teacher_id']}"

def test_assignment_resubmit_error(client, h_student_1):
    # First, create and submit a draft assignment
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={'content': 'Resubmit Test Assignment'}
    )
    assert response.status_code == 200, "Expected status code 200 for creating assignment."

    assignment_id = response.json['data']['id']  # Get the newly created assignment ID

    # Submit the assignment
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={'id': assignment_id, 'teacher_id': 2}
    )
    assert response.status_code == 200, "Expected status code 200 for successful submission."

    # Attempt to resubmit the same assignment
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={'id': assignment_id, 'teacher_id': 2}
    )
    
    assert response.status_code == 400
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'
