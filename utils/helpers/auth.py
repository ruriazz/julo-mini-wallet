import hashlib
from typing import Any, Callable
from django.conf import settings
from models.auth_data.models import AuthData
from rest_framework.request import Request
from models.auth_data.models import AuthData
from models.wallet.vars import WalletStatus
from utils.api import response
from utils.api.request import AuthorizedContext


def make_auth_token(auth_data: AuthData) -> str:
    token = f"{auth_data.wallet._id}:{auth_data._id}({settings.SECRET_KEY})"
    sha1 = hashlib.sha1()
    sha1.update(token.encode('utf-8'))
    return sha1.hexdigest()

def authorized_wallet(allow_inactive_wallet: bool = False) -> Callable[..., Callable[..., response.JsonResponse | Any]]:
    def decorate(function):
        def wrapper(request: Request, *args, **kwargs):
            if authorization := request.headers.get('Authorization'):
                try:
                    token = authorization.split('Token ')[1]
                    auth_data = AuthData.objects.get(token=token)
                    if not allow_inactive_wallet and WalletStatus(auth_data.wallet.status) == WalletStatus.DISABLED:
                        return response.SendJson(status=response.Status.NOT_FOUND, data={'error': 'Wallet disabled'})
                    
                    if make_auth_token(auth_data) != token:
                        raise Exception('Token invalid')

                    auth_request = AuthorizedContext(request=request, auth_data=auth_data)
                except Exception as err:
                    return response.SendJson(status=response.Status.UNAUTHORIZED, data={'error': 'Invalid Authorization'})
                return function(auth_request, *args, **kwargs)
            return response.SendJson(status=response.Status.UNAUTHORIZED, data={'error': 'No Authorization data'})
        return wrapper
    return decorate