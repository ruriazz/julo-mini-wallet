import logging
from typing import List, Any, Union
from rest_framework.viewsets import ViewSet
from utils.api import ExposedErrorMessage


class BaseHandler(ViewSet):
    """"""


class BaseService:
    errors: List[ExposedErrorMessage]
    results: Any

    def __init__(self) -> None:
        self.errors = []
        self.results = None

    def with_error(self, err: Union[ExposedErrorMessage, List[ExposedErrorMessage]]) -> "BaseService":
        if isinstance(err, (ExposedErrorMessage, str)):
            err = [err]
        self.errors += err
        return self
    
    def with_results(self, results: Any) -> "BaseService":
        self.results = results
        return self


class BaseRepository:
    log = logging.getLogger("julo-mini-wallet")