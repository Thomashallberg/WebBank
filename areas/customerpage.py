from flask import render_template, redirect, Blueprint
from model import Customer, Account
from flask_security import roles_accepted, auth_required, logout_user

customerBluePrint = Blueprint('customerpage', __name__)

@customerBluePrint.route("/customer/<id>")
@auth_required()
@roles_accepted("Admin","Staff")
def customerpage(id):
    customer = Customer.query.filter_by(Id = id).first()
    Saldo = 0
    for accounts in customer.Accounts:
        Saldo = Saldo + accounts.Balance
    return render_template("customer.html", customer=customer, activePage="customersPage", Saldo=Saldo )


