import os

def get_credentials(file_name):
    credentials_file = os.path.join(os.path.dirname(__file__), file_name)
    with open(credentials_file, 'r') as credentials:
        user = credentials.readline().rstrip()
        password = credentials.readline().rstrip()
    return user, password
