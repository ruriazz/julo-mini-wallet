from apiv1 import BaseHandler as __BaseHandler
from rest_framework.request import Request
from django.http.response import JsonResponse
from utils.api.request import AuthorizedContext
from utils.api import response
from utils.helpers.auth import authorized_wallet
from models.wallet_transaction.vars import TransactionType
from apiv1.wallet import validators
from apiv1.wallet import services
from apiv1.wallet import entities
from apiv1.wallet import serializers


class WalletHandler(__BaseHandler):
    @staticmethod
    def wallet_registration(request: Request) -> JsonResponse:
        validation = validators.RegisterWalletDataValidation(data=request.data)
        if not validation.is_valid():
            return response.SendJson(status=response.Status.BAD_REQUEST, data={'error': validation.errors})

        service = services.WalletRegistrationService(entities.WalletRegistrationData(**validation.validated_data))
        if service.errors:
            return response.SendJson(status=response.Status.BAD_REQUEST, data={'error': service.errors})

        return response.SendJson(status=response.Status.CREATED, data=serializers.WalletRegistrationDataResponse(instance=service.results).data)
    
    @staticmethod
    @authorized_wallet(True)
    def activate_wallet(context: AuthorizedContext) -> JsonResponse:
        service = services.WalletActivationService(context.auth_data.wallet)
        if service.errors:
            return response.SendJson(status=response.Status.BAD_REQUEST, data={'error': service.errors[0]})
        return response.SendJson(status=response.Status.CREATED, data={'wallet': serializers.WalletActivationDataResponse(instance=service.results).data})
    
    @staticmethod
    @authorized_wallet()
    def wallet_balance(context: AuthorizedContext) -> JsonResponse:
        return response.SendJson(data={'wallet': serializers.WalletBalanceDataResponse(instance=context.auth_data.wallet).data})
    
    @staticmethod
    @authorized_wallet()
    def transaction_history(context: AuthorizedContext) -> JsonResponse:
        service = services.FetchWalletTransactionService(wallet=context.auth_data.wallet)
        if service.errors:
            return response.SendJson(status=response.Status.BAD_REQUEST, data={'error': service.errors[0]})
        results = serializers.TransactionHistoryDataResponse(instance=service.results or [], many=True)
        return response.SendJson(data={'transactions': results.data})
    
    @staticmethod
    @authorized_wallet(True)
    def create_transaction(context: AuthorizedContext, action: str) -> JsonResponse:
        transaction_type = TransactionType.from_value(action)
        if not transaction_type:
            return response.SendJson(status=response.Status.NOT_FOUND, data={'error': f"'{action}' is invalid transaction type"})

        validation = validators.CreateTransactionDataValidation(data=context.request.data)
        if not validation.is_valid():
            return response.SendJson(status=response.Status.BAD_REQUEST, data={'error': validation.errors})
        
        service = services.CreateTransactionService(
            wallet=context.auth_data.wallet,
            transaction_type=transaction_type,
            data=entities.CreateTransactionData(transaction_type=transaction_type.value, **validation.validated_data)
        )

        if service.errors:
            return response.SendJson(status=response.Status.BAD_REQUEST, data={'error': service.errors[0]})
        
        if transaction_type == TransactionType.DEPOSIT:
            result = serializers.WalletDepositDataResponse(instance=service.results)
        else:
            result = serializers.WalletWithdrawDataResponse(instance=service.results)

        return response.SendJson(data=result.data, status=response.Status.CREATED)
    
    @staticmethod
    @authorized_wallet(True)
    def deactivate_wallet(context: AuthorizedContext) -> JsonResponse:
        service = services.DeactivateWalletService(context.auth_data.wallet)
        if service.errors:
            return response.SendJson(status=response.Status.BAD_REQUEST, data={'error': service.errors[0]})
        return response.SendJson(data={'wallet': serializers.WalletActivationDataResponse(instance=service.results).data})