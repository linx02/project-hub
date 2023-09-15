import subprocess

test_file_order = [
    'test_noauth_protection.py',
    'test_auth.py',
    'test_misc.py',
    'test_like_comment.py',
    'test_submission_update.py'
]

pytest_command = ["pytest"] + test_file_order

subprocess.run(pytest_command)
