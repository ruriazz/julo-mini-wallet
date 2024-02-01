import uuid
from django.db import models
from models.wallet.vars import WalletStatus
from django.core.validators import MinValueValidator
from models import BaseModelManager


class Wallet(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_xid = models.UUIDField(null=False, blank=False)
    status = models.CharField(max_length=10, choices=[(choice.name, choice.value) for choice in WalletStatus], default=WalletStatus.DISABLED.value)
    enabled_at = models.DateTimeField(null=True, default=None)
    balance = models.PositiveBigIntegerField(null=False, default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    objects = BaseModelManager()
    default_objects = models.Manager()

    class Meta:
        db_table = 'wallet'
        managed = True