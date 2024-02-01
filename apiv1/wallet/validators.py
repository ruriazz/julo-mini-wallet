import uuid
from rest_framework import serializers
from utils.helpers.string import valid_uuidv4


class RegisterWalletDataValidation(serializers.Serializer):
    customer_xid = serializers.CharField(required=True, error_messages={ 'required': 'Missing data for required field.' })

    def validate_customer_xid(self, val: str) -> str:
        if valid_uuidv4(val):
            return val
        raise serializers.ValidationError("Invalid data")
    
class CreateTransactionDataValidation(serializers.Serializer):
    amount = serializers.IntegerField(required=True, min_value=0, error_messages={ 'required': 'Missing data for required field.' })
    reference_id = serializers.CharField(required=True, error_messages={ 'required': 'Missing data for required field.' })

    def validate_reference_id(self, val: str) -> str:
        if valid_uuidv4(val):
            return val
        raise serializers.ValidationError("Invalid data")