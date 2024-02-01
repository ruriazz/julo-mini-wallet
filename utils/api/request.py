from rest_framework.request import Request
from models.auth_data.models import AuthData


class AuthorizedContext:
    request: Request
    auth_data: AuthData

    def __init__(self, request: Request, auth_data: AuthData) -> None:
        self.request = request
        self.auth_data = auth_data