from flask_sqlalchemy import SQLAlchemy
import barnum
import random
from datetime import datetime  
from datetime import timedelta
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
from flask_security.models import fsqla_v3 as fsqla
from model import Account, Transaction
from utils import create_deposit, create_withdrawal



def test_deposit():
    newaccount = Account()
    newaccount.Id = 3
    newaccount.Balance = 0
    transaction = Transaction()
    transaction.Amount = 10
    create_deposit(newaccount, transaction)
    
    assert newaccount.Balance == 10
    assert transaction.NewBalance == 10
    assert newaccount.Id == transaction.AccountId
    assert transaction.Date != None
    assert transaction.Type == "Debit"
    assert transaction.Operation == "Deposit cash"
    assert len(newaccount.Transactions) > 0
    assert transaction in newaccount.Transactions


def test_withdraw():
    newaccount = Account()
    newaccount.Id = 3
    newaccount.Balance = 1000
    transaction = Transaction()
    transaction.Amount = 10
    create_withdrawal(newaccount, transaction)
    
    assert newaccount.Balance == 990
    assert transaction.NewBalance == 990
    assert newaccount.Id == transaction.AccountId
    assert transaction.Date != None
    assert transaction.Type == "Credit"
    assert transaction.Operation == "Bank withdrawal"
    assert len(newaccount.Transactions) > 0
    assert transaction in newaccount.Transactions
    