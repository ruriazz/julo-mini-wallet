import contextlib
from typing import Optional
from enum import Enum


class WalletStatus(Enum):
    ENABLED = 'enabled'
    DISABLED = 'disabled'

    @staticmethod
    def from_value(value: str) -> Optional["WalletStatus"]:
        with contextlib.suppress(Exception):
            return WalletStatus(value)