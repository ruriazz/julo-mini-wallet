from pydantic import BaseModel as __BaseModel
from models.wallet_transaction.vars import TransactionType

class WalletRegistrationData(__BaseModel):
    customer_xid: str

class CreateTransactionData(__BaseModel):
    amount: int
    reference_id: str
    transaction_type: str