from rest_framework import serializers
from models.wallet.vars import WalletStatus


class WalletRegistrationDataResponse(serializers.Serializer):
    token = serializers.CharField()

class WalletActivationDataResponse(serializers.Serializer):
    id = serializers.UUIDField(source='_id')
    owned_by = serializers.UUIDField(source='customer_xid')
    status = serializers.CharField(default=WalletStatus.DISABLED.value)
    enabled_at = serializers.DateTimeField()
    balance = serializers.IntegerField()
    
class WalletBalanceDataResponse(serializers.Serializer):
    id = serializers.UUIDField(source='_id')
    owned_by = serializers.UUIDField(source='customer_xid')
    status = serializers.CharField(default=WalletStatus.DISABLED.value)
    enabled_at = serializers.DateTimeField()
    balance = serializers.IntegerField()
    
class WalletDepositDataResponse(serializers.Serializer):
    id = serializers.UUIDField(source='_id')
    deposited_by = serializers.UUIDField(source='wallet.customer_xid')
    status = serializers.CharField()
    deposited_at = serializers.DateTimeField(source='transacted_at')
    amount = serializers.IntegerField()
    reference_id = serializers.UUIDField()

class WalletWithdrawDataResponse(serializers.Serializer):
    id = serializers.UUIDField(source='_id')
    withdrawn_by = serializers.UUIDField(source='wallet.customer_xid')
    status = serializers.CharField()
    withdrawn_at = serializers.DateTimeField(source='transacted_at')
    amount = serializers.IntegerField()
    reference_id = serializers.UUIDField()

class TransactionHistoryDataResponse(serializers.Serializer):
    id = serializers.UUIDField(source='_id')
    status = serializers.CharField()
    transacted_at = serializers.DateTimeField()
    type = serializers.CharField(source='transaction_type')
    amount = serializers.IntegerField()
    reference_id = serializers.UUIDField()