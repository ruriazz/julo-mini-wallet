from http import HTTPStatus
from typing import Any
from django.http import JsonResponse


class Status:
    HTTP_OK = HTTPStatus.OK
    CREATED = HTTPStatus.CREATED
    BAD_REQUEST = HTTPStatus.BAD_REQUEST
    UNAUTHORIZED = HTTPStatus.UNAUTHORIZED
    NOT_FOUND = HTTPStatus.NOT_FOUND

def SendJson(status: Status = Status.HTTP_OK, data: Any = None) -> JsonResponse:
    response = {
        "status": "success" if status >= HTTPStatus.OK and status <= HTTPStatus.IM_USED else "fail",
        "data": data
    }

    sanitized_response = {
        key: response[key]
        for key, value in response.items()
        if isinstance(value, bool) or response[key]
    }
    return JsonResponse(data=sanitized_response, status=status)