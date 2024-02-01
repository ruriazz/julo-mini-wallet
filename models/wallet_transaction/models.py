import uuid
from django.db import models
from django.core.validators import MinValueValidator
from models import BaseModelManager
from models.wallet.models import Wallet
from models.wallet_transaction.vars import TransactionStatus
from models.wallet_transaction.vars import TransactionType


class WalletTransaction(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(to=Wallet, null=False, blank=False, db_column='wallet_id', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[(choice.name, choice.value) for choice in TransactionStatus], null=True, blank=False, default=None)
    transacted_at = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=10, choices=[(choice.name, choice.value) for choice in TransactionType], null=False, blank=False)
    amount = models.PositiveBigIntegerField(null=False, default=0, validators=[MinValueValidator(0)])
    reference_id = models.UUIDField(null=False, blank=False)
    system_notes = models.TextField(null=True, blank=True, default=None)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    objects = BaseModelManager()
    default_objects = models.Manager()

    class Meta:
        db_table = 'wallet_transaction'