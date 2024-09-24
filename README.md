Fyle Backend Challenge
Overview

This project is a backend service designed for a classroom management system as part of the Fyle internship challenge. It aims to handle assignments, grading, and student-teacher interactions effectively.
Who Is This For?

This challenge is intended for candidates interested in interning at Fyle and collaborating with our engineering team. A commitment of at least 6 months is required for the internship.
Why Work at Fyle?

Fyle is a rapidly growing Expense Management SaaS product with a robust engineering team of around 40 members. We pride ourselves on transparency and teamwork. For insights into our work culture, check our careers page and Glassdoor reviews.
Challenge Outline

Candidates are encouraged to utilize any online or AI tools (like ChatGPT, Gemini, etc.) to assist in completing the challenge. However, a thorough understanding of the code and logic is expected.
Key Features

    Assignments Management: Create, retrieve, submit, and grade assignments.
    User Roles: Support for students, teachers, and principals with role-specific functionalities.

Getting Started
Installation

    Fork this Repository: Create a copy of this repository in your GitHub account.
    Clone the Forked Repository:

    bash

    git clone <your-fork-url>
    cd <your-repo-name>

Install Requirements

    Create a virtual environment and activate it:

    bash

virtualenv env --python=python3.8
source env/bin/activate

Install the necessary dependencies:

bash

    pip install -r requirements.txt

Reset Database

    Set the Flask application:

    bash

export FLASK_APP=core/server.py

Remove the existing database and upgrade:

bash

    rm core/store.sqlite3
    flask db upgrade -d core/migrations/

Start Server

Run the server using the following command:

bash

bash run.sh

Run Tests

To execute the tests, use:

bash

pytest -vvv -s tests/

For a test coverage report, run:

bash

pytest --cov
open htmlcov/index.html

What Happens Next?

You will receive feedback within 48 hours via email after submission.

Feel free to adjust any sections as needed!
