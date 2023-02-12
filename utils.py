from flask_sqlalchemy import SQLAlchemy
import barnum
import random
from datetime import datetime  
from datetime import timedelta
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
from flask_security.models import fsqla_v3 as fsqla
from model import Account, Transaction

def create_deposit(account, transaction):
    now = datetime.now()
    
    account.Balance = account.Balance + transaction.Amount
    transaction.NewBalance = account.Balance
    transaction.AccountId = account.Id
    transaction.Date = now
    transaction.Type = "Debit"
    transaction.Operation = "Deposit cash"
    account.Transactions.append(transaction)
    
def create_withdrawal(account, transaction):
    now = datetime.now()
    
    account.Balance = account.Balance - transaction.Amount
    transaction.NewBalance = account.Balance
    transaction.AccountId = account.Id
    transaction.Date = now
    transaction.Type = "Credit"
    transaction.Operation = "Bank withdrawal"
    account.Transactions.append(transaction)