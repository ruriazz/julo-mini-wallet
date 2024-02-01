from typing import Optional
from django.utils import timezone
from django.db.models import QuerySet
from django.db.models import Q
from apiv1 import BaseRepository as __BaseRepository
from models.wallet.models import Wallet
from models.auth_data.models import AuthData
from models.wallet_transaction.models import WalletTransaction
from apiv1.wallet import entities
from utils.helpers.string import make_uuid4


class WalletRepository(__BaseRepository):
    def get_one(self, **filters) -> Optional[Wallet]:
        try:
            return Wallet.objects.filter(**filters).first()
        except Exception as err:
            self.log.error(msg=f"WalletRepository.get_one Exception: {err}", exc_info=True)

    def create_one(self, data: entities.WalletRegistrationData) -> Optional[Wallet]:
        try:
            wallet = Wallet(customer_xid=make_uuid4(data.customer_xid))
            wallet.save()

            return wallet
        except Exception as err:
            self.log.error(msg=f"WalletRepository.create_one Exception: {err}", exc_info=True)

    def update_one(self, wallet: Wallet, **new_data) -> Optional[Wallet]:
        try:
            Wallet.objects.filter(pk=wallet.pk).update(**new_data)
            return Wallet.objects.get(pk=wallet.pk)
        except Exception as err:
            self.log.error(msg=f"WalletRepository.update_one Exception: {err}", exc_info=True)

    def soft_delete(self, **filters) -> bool:
        try:
            wallets = Wallet.objects.filter(**filters)
            wallets.update(deleted_at=timezone.now())
            return True
        except Exception as err:
            self.log.error(msg=f"WalletRepository.soft_delete Exception: {err}", exc_info=True)
            return False


class AuthDataRepository(__BaseRepository):
    def create_one(self, wallet: Wallet) -> Optional[AuthData]:
        try:
            auth_data = AuthData(wallet=wallet)
            auth_data.save()

            return auth_data
        except Exception as err:
            self.log.error(msg=f"AuthDataRepository.create_one Exception: {err}", exc_info=True)

    def update_one(self, auth_data: AuthData, **new_data) -> Optional[AuthData]:
        try:
            AuthData.objects.filter(pk=auth_data.pk).update(**new_data)
            return AuthData.objects.get(pk=auth_data.pk)
        except Exception as err:
            self.log.error(msg=f"AuthDataRepository.update_one Exception: {err}", exc_info=True)


class WalletTransactionRepository(__BaseRepository):
    def reference_id_exists(self, trx: WalletTransaction) -> bool:
        try:
            return WalletTransaction.objects.only('pk') \
                .exclude(pk=trx.pk) \
                .filter(reference_id=trx.reference_id).exists()
        except Exception as err:
            self.log.error(msg=f"WalletTransactionRepository.reference_id_exists Exception: {err}", exc_info=True)

    def create_one(self, wallet: Wallet, data: entities.CreateTransactionData) -> Optional[WalletTransaction]:
        try:
            transaction = WalletTransaction(
                wallet=wallet,
                transaction_type=data.transaction_type,
                amount=data.amount,
                reference_id=make_uuid4(data.reference_id),
            )
            transaction.save()

            return transaction
        except Exception as err:
            self.log.error(msg=f"WalletTransactionRepository.create_one Exception: {err}", exc_info=True)

    def retrieve(self, objects: Optional[QuerySet[WalletTransaction]] = None, **filters) -> Optional[QuerySet[WalletTransaction]]:
        try:
            return (objects or WalletTransaction.objects).filter(**filters)
        except Exception as err:
            self.log.error(msg=f"WalletTransactionRepository.create_one Exception: {err}", exc_info=True)

    def retrieve_from_latest(self, **filters) -> Optional[QuerySet[WalletTransaction]]:
        if qs := self.retrieve(**filters):
            return qs.order_by('-transacted_at')

    def update_one(self, transaction_data: WalletTransaction, **new_data) -> Optional[WalletTransaction]:
        try:
            WalletTransaction.objects.filter(pk=transaction_data.pk).update(**new_data)
            return WalletTransaction.objects.get(pk=transaction_data.pk)
        except Exception as err:
            self.log.error(msg=f"WalletTransactionRepository.update_one Exception: {err}", exc_info=True)

    def soft_delete(self, **filters) -> bool:
        try:
            transaction = WalletTransaction.objects.filter(**filters)
            transaction.update(deleted_at=timezone.now())
            return True
        except Exception as err:
            self.log.error(msg=f"WalletTransactionRepository.soft_delete Exception: {err}", exc_info=True)
            return False