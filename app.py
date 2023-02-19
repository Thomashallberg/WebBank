from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import db, seedData, seed_user, Customer, Account, Transaction
from forms import NewCustomerForm, DepositForm, WithdrawForm, TransferForm, ResetRequestForm
from datetime import datetime
from flask_security import roles_accepted, auth_required, logout_user, hash_password
import os
from utils import create_deposit, create_withdrawal, create_transfer
from flask_mail import Mail, Message

# active page
# Sorting
# paging
#pip install flask-security-too
#pip install flask_security

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://tompa:Aarin1991@bank.mysql.database.azure.com/bank?charset=utf8'
#'mysql+mysqlconnector://root:my-secret-pw@localhost/Bank'
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
app.config["SESSION_COOKIE_SAMESITE"] = "strict"

app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '11f618d9e4cbcf'
app.config['MAIL_PASSWORD'] = '0654bc9d6179b6'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
db.app = app
db.init_app(app)
migrate = Migrate(app,db)


def send_reset_mail(recipient, password):
  msg = Message('Password reset', sender =   'Admin@mailtrap.io', recipients = [recipient])
  msg.body = f"Hey, this is your new password: {password}"
  mail.send(msg)
  return "Message sent!"

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    form=ResetRequestForm()
    if form.validate_on_submit():
        send_reset_mail(form.email.data, form.password.data)
        Update_user = app.security.datastore.find_user(email="stefan.holmberg@systementor.se")
        Update_user.password=hash_password(form.password.data)
        app.security.datastore.db.session.commit()
        return render_template("reset_request.html", title="Reset request",form=form, mail_is_sent=True)
    
    return render_template("reset_request.html", title="Reset request", form=form, mail_is_sent=False)

@app.route("/")
def startpage():
    account = Account.query.filter(Account.Balance)
    balance = 0
    AllAccounts = Account.query.count()
    customers = Customer.query.count()
    for x in account:
        balance += x.Balance
    return render_template("index.html", activePage="startPage", balance=balance, AllAccounts=AllAccounts, customers=customers )
 
@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/customerimage/<id>")
def customerimagepage(id):
    customer = Customer.query.filter_by(Id = id).first()
    return render_template("customerimage.html", customer=customer, activePage="customersPage" )


@app.route("/customer/<id>")
@auth_required()
@roles_accepted("Admin","Staff")
def customerpage(id):
    customer = Customer.query.filter_by(Id = id).first()
    Saldo = 0
    for accounts in customer.Accounts:
        Saldo = Saldo + accounts.Balance
    return render_template("customer.html", customer=customer, activePage="customersPage", Saldo=Saldo )

@app.route("/adminblabla")
@auth_required()
@roles_accepted("Admin")
def adminblblapage():
    return render_template("adminblabla.html", activePage="secretPage" )

@app.route("/customer/account/<id>")
def Transaktioner(id):
    account = Account.query.filter_by(Id = id).first()
    transaktioner = Transaction.query.filter_by(AccountId=id)
    transaktioner = transaktioner.order_by(Transaction.Date.desc())
    return render_template("Transaktioner.html", account=account, transaktioner=transaktioner)

@app.route("/customers")
@auth_required()
@roles_accepted("Admin","Staff")
def customerspage():
    sortColumn = request.args.get('sortColumn', 'namn')
    sortOrder = request.args.get('sortOrder', 'asc')
    page = int(request.args.get('page', 1))
    searchWord = request.args.get('q','')

    listOfCustomers = Customer.query

    listOfCustomers = listOfCustomers.filter(
        Customer.GivenName.like('%' + searchWord + '%') | 
        Customer.City.like('%' + searchWord + '%') |
        Customer.NationalId.like('%' + searchWord + '%') |
        Customer.Streetaddress.like('%' + searchWord + '%') |
        Customer.City.like('%' + searchWord + '%') |
        Customer.Id.like('%' + searchWord + '%') )

    if sortColumn == "namn":
        if sortOrder == "asc":
            listOfCustomers = listOfCustomers.order_by(Customer.GivenName.asc())
        else:
            listOfCustomers = listOfCustomers.order_by(Customer.GivenName.desc())
    elif sortColumn == "city":
        if sortOrder == "asc":
            listOfCustomers = listOfCustomers.order_by(Customer.City.asc())
        else:
            listOfCustomers = listOfCustomers.order_by(Customer.City.desc())

    paginationObject = listOfCustomers.paginate(page=page,per_page=30,error_out=False )
    return render_template("customers.html", 
                    listOfCustomers=paginationObject.items, 
                    activePage="customersPage",
                    page=page,
                    sortColumn=sortColumn,
                    sortOrder=sortOrder,
                    has_next = paginationObject.has_next,
                    has_prev = paginationObject.has_prev,
                    pages=paginationObject.pages,
                    q = searchWord)
    
@app.route("/newcustomer", methods=['GET', 'POST'])
def newcustomer():
    now = datetime.now()
    form = NewCustomerForm()
    if form.validate_on_submit():
        #spara i databas
        customer = Customer()
        customer.GivenName = form.GivenName.data
        customer.Surname = form.Surname.data
        customer.Streetaddress = form.Streetaddress.data
        customer.City = form.City.data
        customer.Zipcode = form.Zipcode.data
        customer.Country = form.Country.data
        customer.CountryCode = form.CountryCode.data
        customer.Birthday = form.Birthday.data
        customer.NationalId = form.NationalId.data
        customer.TelephoneCountryCode = form.TelephoneCountryCode.data
        customer.Telephone = form.Telephone.data
        customer.EmailAddress = form.EmailAddress.data
        newaccount = Account()
        newaccount.AccountType = "Savings"
        newaccount.Created = now
        newaccount.Balance = 0
        customer.Accounts = [newaccount]
        
        db.session.add(customer)
        db.session.commit()
    return render_template("newcustomer.html", formen=form )

@app.route("/customer/account/newdeposit/<id>", methods=['GET', 'POST'])
def deposit(id):
    account = Account.query.filter_by(Id = id).first()
    customer = account.Customer
    form = DepositForm()
    if form.validate_on_submit():
        transaction = Transaction()
        transaction.Amount = form.Amount.data
        create_deposit(account, transaction)
        db.session.add(account)
        db.session.add(transaction)
        db.session.commit()
        
    return render_template("deposit.html", account=account, customer=customer, form=form)

@app.route("/customer/account/newwithdrawal/<id>", methods=['GET', 'POST'])
def withdrawal(id):
    account = Account.query.filter_by(Id = id).first()
    customer = account.Customer
    form = WithdrawForm()
    if form.validate_on_submit():
        transaction = Transaction()
        transaction.Amount = form.Amount.data
        create_withdrawal(account, transaction)
        db.session.add(account)
        db.session.add(transaction)
        db.session.commit()
        
    return render_template("withdrawal.html", account=account, customer=customer, form=form)

@app.route("/customer/account/transfer/<id>", methods=['GET', 'POST'])
def transfer(id):
    account = Account.query.filter_by(Id = id).first()
    customer = account.Customer
    form = TransferForm()
    if form.validate_on_submit():
        transaction_receiver = Transaction()
        transaction_sender = Transaction()
        ReceiverAccount = Account.query.filter_by(Id = form.Receiver.data).first()
        print(account.Balance)
        print(ReceiverAccount)
        print(ReceiverAccount.Balance)
        transaction_receiver.Amount = form.Amount.data
        transaction_sender.Amount = form.Amount.data
        
        create_transfer(account, ReceiverAccount, transaction_sender, transaction_receiver)
        db.session.add(account)
        db.session.add(ReceiverAccount)
        db.session.add(transaction_receiver)
        db.session.add(transaction_sender)
        db.session.commit()
        
    return render_template("transfer.html", account=account, customer=customer, form=form)

@app.route("/editcustomer/<id>", methods=['GET', 'POST'])
def editcustomer(id):
    customer = Customer.query.filter_by(Id=id).first()
    form = NewCustomerForm()

    if form.validate_on_submit():
        customer.GivenName = form.GivenName.data
        customer.Surname = form.Surname.data
        customer.Streetaddress = form.Streetaddress.data
        customer.City = form.City.data
        customer.Zipcode = form.Zipcode.data
        customer.Country = form.Country.data
        customer.CountryCode = form.CountryCode.data
        customer.Birthday = form.Birthday.data
        customer.NationalId = form.NationalId.data
        customer.TelephoneCountryCode = form.TelephoneCountryCode.data
        customer.Telephone = form.Telephone.data
        customer.EmailAddress = form.EmailAddress.data
        db.session.commit()
        return redirect("/customers" )
    if request.method == 'GET':
        form.GivenName.data = customer.GivenName
        form.Surname.data = customer.Surname
        form.Streetaddress.data = customer.Streetaddress
        form.City.data = customer.City
        form.Zipcode.data = customer.Zipcode
        form.Country.data = customer.Country
        form.CountryCode.data = customer.CountryCode
        form.Birthday.data = customer.Birthday
        form.NationalId.data = customer.NationalId
        form.TelephoneCountryCode.data = customer.TelephoneCountryCode
        form.Telephone.data = customer.Telephone
        form.EmailAddress.data = customer.EmailAddress
    return render_template("editcustomer.html", formen=form )


if __name__  == "__main__":
    with app.app_context():
        #upgrade()

        seedData(db)
        print("Startar seed")
        seed_user(app, db)
        print("Seeding done")
        app.run(host='0.0.0.0', debug=True)

        # while True:
        #     print("1. Create")
        #     print("2. List")        
        #     print("3. Exit")                
        #     action = input("Ange:")
        #     if action == "3":
        #         break
        #     if action == "1":
        #         print("Create")
        #     if action == "2":
        #         print("List")          
