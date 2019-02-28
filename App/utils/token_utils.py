import uuid

ADMIN = "admin"

CINEMA = "cinema"

VIEWER = "viewer"


def generate_token(namespace):

    return namespace + uuid.uuid4().hex


def generate_admin_token():
    return generate_token(ADMIN)


def generate_cinema_token():
    return generate_token(CINEMA)


def generate_viewer_token():
    return generate_token(VIEWER)