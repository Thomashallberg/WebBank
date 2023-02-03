from flask_sqlalchemy import SQLAlchemy
import barnum
import random
from datetime import datetime  
from datetime import timedelta
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
from flask_security.models import fsqla_v3 as fsqla
from model import Account, Transaction

#testa sätta in pengar
#testa skapa transaktion

#konto
#summa

def test_deposit():
    newaccount = Account()
    newaccount.Id = 3
    newaccount.Balance = 0
    transaction = Transaction()
    transaction.Amount = 10
    create_transaction(newaccount, transaction)
    
    
    
    assert newaccount.Balance == 10
    assert transaction.NewBalance == 10
    assert newaccount.Id == transaction.AccountId
    assert transaction.Date != None
    
def create_transaction(account, transaction):
    now = datetime.now()
    account.Balance = account.Balance + transaction.Amount
    transaction.NewBalance = account.Balance
    transaction.AccountId = account.Id
    transaction.Date = now
    
    

# def test_deposit():
#     newaccount = Account()
#     newaccount.Balance = 0
    
# assert newaccount.Balance

# def test_foo():
#     assert foo() == 10
    
# def foo():
#     return 10
    