import uuid
from django.db import models
from models.wallet.models import Wallet


class AuthData(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(to=Wallet, null=False, blank=False, on_delete=models.CASCADE, db_column='wallet_id')
    token = models.CharField(max_length=40, null=True, blank=False, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'auth_data'