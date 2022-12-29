from api_client.api_requests import api_requests


def check_if_user_is_admin(id: int):
    response = api_requests.get(f"/admins/{id}")
    return response.json() if response.status_code == 200 else False


def check_if_user_exists(id: int):
    response = api_requests.get(f"/users/{id}")
    return response.json() if response.status_code == 200 else False
