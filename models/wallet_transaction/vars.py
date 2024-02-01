import contextlib
from typing import Optional
from enum import Enum


class TransactionStatus(Enum):
    SUCCESS = 'success'
    FAILED = 'failed'

    @staticmethod
    def from_value(value: str) -> Optional["TransactionStatus"]:
        with contextlib.suppress(Exception):
            return TransactionStatus(value)
        

class TransactionType(Enum):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'

    @staticmethod
    def from_value(value: str) -> Optional["TransactionType"]:
        if value.endswith('s'):
            value = value[:-1]

        with contextlib.suppress(Exception):
            return TransactionType(value)