from typing import Any
from rest_framework.views import exception_handler
from rest_framework.exceptions import MethodNotAllowed
from django.views.defaults import page_not_found


def api_exception_handler(exc: Any, context: Any) -> Any:
    response = exception_handler(exc, context)

    if isinstance(exc, MethodNotAllowed):
        if request := context.get('request'):
            return page_not_found(request, exc)

    return response