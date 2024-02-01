from typing import Optional, List
from django.utils import timezone
from apiv1 import BaseService as __BaseService
from apiv1.wallet import entities
from apiv1.wallet import repositories
from models.wallet.models import Wallet
from models.wallet.vars import WalletStatus
from models.wallet_transaction.models import WalletTransaction
from models.wallet_transaction.vars import TransactionType
from models.wallet_transaction.vars import TransactionStatus
from models.auth_data.models import AuthData
from utils.api import ExposedErrorMessage
from utils.helpers.auth import make_auth_token


class WalletRegistrationService(__BaseService):
    wallet_repo: repositories.WalletRepository
    auth_repo: repositories.AuthDataRepository
    data: entities.WalletRegistrationData

    def __init__(self, data: entities.WalletRegistrationData) -> None:
        super().__init__()

        self.data = data
        self.wallet_repo = repositories.WalletRepository()
        self.auth_repo = repositories.AuthDataRepository()
        self._main()

    def _main(self) -> "WalletRegistrationService":
        if wallet := self.wallet_repo.create_one(self.data):
            if auth_data := self._generate_authentication_data(wallet):
                return self.with_results(auth_data)
            else:
                self.wallet_repo.soft_delete(_id=wallet._id)
        
        return self.with_error(ExposedErrorMessage("An error occurred while saving data"))
    
    def _generate_authentication_data(self, wallet: Wallet) -> Optional[AuthData]:
        if auth_data := self.auth_repo.create_one(wallet):
            if updated_auth_data := self.auth_repo.update_one(auth_data=auth_data, token=make_auth_token(auth_data)):
                return updated_auth_data
            
class WalletActivationService(__BaseService):
    wallet_repo: repositories.WalletRepository
    wallet: Wallet

    def __init__(self, wallet: Wallet) -> None:
        super().__init__()

        self.wallet = wallet
        self.wallet_repo = repositories.WalletRepository()
        self._main()

    def _main(self) -> "WalletActivationService":
        if WalletStatus.from_value(self.wallet.status) == WalletStatus.ENABLED:
            return self.with_error(ExposedErrorMessage("Already enabled"))
        
        if updated_wallet := self.wallet_repo.update_one(wallet=self.wallet, status=WalletStatus.ENABLED.value, enabled_at=timezone.now()):
            return self.with_results(updated_wallet)

        return self.with_error(ExposedErrorMessage("An error occurred while activating the wallet"))
    

class CreateTransactionService(__BaseService):
    transaction_repo: repositories.WalletTransactionRepository
    wallet_repo: repositories.WalletRepository

    data: entities.CreateTransactionData
    wallet: Wallet

    def __init__(self, wallet: Wallet, transaction_type: TransactionType, data: entities.CreateTransactionData) -> None:
        super().__init__()

        self.transaction_repo = repositories.WalletTransactionRepository()
        self.wallet_repo = repositories.WalletRepository()

        self.data = data
        self.wallet = wallet

        { TransactionType.DEPOSIT: self._deposit, TransactionType.WITHDRAWAL: self._withdraw }.get(transaction_type)()

    def _deposit(self) -> "CreateTransactionService":
        if transaction := self.transaction_repo.create_one(wallet=self.wallet, data=self.data):
            if system_notes := self._validate_transaction(transaction):
                updated_transaction = self.transaction_repo.update_one(transaction, status=TransactionStatus.FAILED.value, system_notes=','.join(system_notes))

            else:
                balance = self.wallet.balance + transaction.amount
                if self.wallet_repo.update_one(self.wallet, balance=balance):
                    updated_transaction = self.transaction_repo.update_one(transaction, status=TransactionStatus.SUCCESS.value)
                else:
                    updated_transaction = self.transaction_repo.update_one(transaction, status=TransactionStatus.FAILED.value, system_notes='SYSTEM_EXCEPTION')

            if 'updated_transaction' in locals() and updated_transaction:
                return self.with_results(updated_transaction)
            else:
                self.transaction_repo.soft_delete(_id=transaction._id)

        return self.with_error(ExposedErrorMessage("An error occurred while creating transaction data"))
    
    def _withdraw(self) -> "CreateTransactionService":        
        if transaction := self.transaction_repo.create_one(wallet=self.wallet, data=self.data):
            if system_notes := self._validate_transaction(transaction):
                updated_transaction = self.transaction_repo.update_one(transaction, status=TransactionStatus.FAILED.value, system_notes=','.join(system_notes))

            else:
                balance = self.wallet.balance - transaction.amount
                if self.wallet_repo.update_one(self.wallet, balance=balance):
                    updated_transaction = self.transaction_repo.update_one(transaction, status=TransactionStatus.SUCCESS.value)
                else:
                    updated_transaction = self.transaction_repo.update_one(transaction, status=TransactionStatus.FAILED.value, system_notes='SYSTEM_EXCEPTION')

            if 'updated_transaction' in locals() and updated_transaction:
                return self.with_results(updated_transaction)
            else:
                self.transaction_repo.soft_delete(_id=transaction._id)

        return self.with_error(ExposedErrorMessage("An error occurred while creating transaction data"))
    
    def _validate_transaction(self, trx: WalletTransaction) -> List[str]:
        notes = []
        if WalletStatus.from_value(trx.wallet.status) == WalletStatus.DISABLED:
            notes.append('WALLET_DISABLED')

        is_same_reference = self.transaction_repo.reference_id_exists(trx)
        if is_same_reference:
            notes.append('SAME_REFERENCE')
        elif is_same_reference is None:
            notes.append('SYSTEM_EXCEPTION')
        
        if TransactionType.from_value(trx.transaction_type) == TransactionType.WITHDRAWAL and trx.amount > trx.wallet.balance:
            notes.append('INSUFFICIENT_BALANCE')

        return notes
    
class FetchWalletTransactionService(__BaseService):
    transaction_repo: repositories.WalletTransactionRepository

    wallet: Wallet

    def __init__(self, wallet: Wallet) -> None:
        super().__init__()

        self.transaction_repo = repositories.WalletTransactionRepository()

        self.wallet = wallet
        self._main()

    def _main(self) -> "FetchWalletTransactionService":
        if results := self.transaction_repo.retrieve_from_latest(wallet=self.wallet):
            return self.with_results(results)
        return self.with_results(None)
    
class DeactivateWalletService(__BaseService):
    wallet_repo: repositories.WalletRepository

    wallet: Wallet

    def __init__(self, wallet: Wallet) -> None:
        super().__init__()

        self.wallet_repo = repositories.WalletRepository()
        self.wallet = wallet
        self._main()

    def _main(self) -> "DeactivateWalletService":
        if updated_wallet := self.wallet_repo.update_one(self.wallet, status=WalletStatus.DISABLED.value):
            return self.with_results(updated_wallet)
        return self.with_error("An error occurred while deactivating the wallet")