from flask_sqlalchemy import SQLAlchemy
import barnum
import random
from datetime import datetime  
from datetime import timedelta
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
from flask_security.models import fsqla_v3 as fsqla
from model import Account, Transaction
from utils import create_deposit, create_withdrawal, create_transfer
from flask import request, jsonify, Response
import pytest
from flask import Flask
import os




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
    
def test_negative_amount():
    newaccount = Account()
    newaccount.Id = 3
    newaccount.Balance = 1000
    transaction = Transaction()
    transaction.Amount = -10
    create_withdrawal(newaccount, transaction)
    
    assert newaccount.Balance == 1000
    assert transaction.NewBalance == 1000
    assert newaccount.Id == 3
    assert transaction.Date == None
    assert transaction.Type == None
    assert transaction.Operation == None
    assert len(newaccount.Transactions) == 0
    assert transaction not in newaccount.Transactions


    
def test_transfer():
    accountA = Account()
    accountA.Id = 1
    accountA.Balance = 1000
    accountB = Account()
    accountB.Id = 2
    accountB.Balance = 1000
    transactionA = Transaction()
    transactionB = Transaction()
    transactionA.Amount=10
    transactionB.Amount=10
    create_transfer(accountA,accountB,transactionA, transactionB)
    assert accountA.Balance == 990
    assert accountB.Balance == 1010
    
    assert transactionA.NewBalance == 990
    assert transactionB.NewBalance == 1010
    
    assert transactionA in accountA.Transactions
    assert transactionB in accountB.Transactions
    
    assert accountA.Id == transactionA.AccountId
    
    assert transactionA.Date != None
    assert transactionA.Type == "Credit"
    assert transactionA.Operation == "Transfer"
    assert len(accountA.Transactions) > 0
    
    assert accountB.Id == transactionB.AccountId
    assert transactionB.Date != None
    assert transactionB.Type == "Debit"
    assert transactionB.Operation == "Transfer"
    assert len(accountB.Transactions) > 0
    # AccountA and AccountB
    # Transaction from A to B
    # Check if transaction exist
    #check if transaction is correct
    # check if the accounts are changed correctly
    
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    
    
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app  

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()
    
def test_request_example(client):
    response = client.get('/hello')
    assert b"Hello, World!" in response.data
    
# def test_api(client):
#     List_of_transactions = []
#     page = int(request.args.get('page', 1))
#     Transaction.query.filter_by(AccountId=id).order_by(Transaction.Date.desc()).paginate(page,5,False)
    
#     for t in Transaction.items:
#         t = { "ID":t.Id, "Type": t.Operation, "Date":t.Date, "Amount": t.Amount, "NewBalance": t.NewBalance, "AccountId": t.AccountId}
#         List_of_transactions.append(t)
#     x =  jsonify(List_of_transactions)

#     response = x.get('/api/customer/account/<id>/')
#     assert Response.json == [ {'ID': 't.Id'}
#     {'result': 'OK - Healthy'}
    #]
    # def test_health_check(client):
    # response = client.get('/status')
    # assert response.json ==  [
    #     {'user': 'admin'},
    #     {'result': 'OK - Healthy'}
    # ]