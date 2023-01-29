from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import db, seedData, Customer, Account, Transaction
from forms import NewCustomerForm
import os

# active page
# Sorting
# paging


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:my-secret-pw@localhost/Bank'
app.config['SECRET_KEY'] = os.urandom(32)
db.app = app
db.init_app(app)
migrate = Migrate(app,db)

@app.route("/")
def startpage():
	    return render_template("index.html", activePage="startPage" )

@app.route("/customerimage/<id>")
def customerimagepage(id):
    customer = Customer.query.filter_by(Id = id).first()
    return render_template("customerimage.html", customer=customer, activePage="customersPage" )


@app.route("/customer/<id>")
def customerpage(id):
    customer = Customer.query.filter_by(Id = id).first()
    Saldo = 0
    for accounts in customer.Accounts:
        Saldo = Saldo + accounts.Balance
        
        
    return render_template("customer.html", customer=customer, activePage="customersPage", Saldo=Saldo )

@app.route("/customer/account/<id>")
def Transaktioner(id):
    account = Account.query.filter_by(Id = id).first()
    transaktioner = Transaction.query.filter_by(AccountId=id)
    transaktioner = transaktioner.order_by(Transaction.Date.desc())
    return render_template("Transaktioner.html", account=account, transaktioner=transaktioner)

@app.route("/customers")
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
    form = NewCustomerForm()
    if form.validate_on_submit():
        #spara i databas
        customer = Customer()
        customer.GivenName = form.GivenName.data
        customer.Surname = form.Surname.data
        customer.Streetaddress = form.Steetaddress.data
        customer.City = form.City.data
        customer.Zipcode = form.Zipcode.data
        customer.Country = form.Country.data
        customer.CountryCode = form.countryCode.data
        customer.Birthday = form.Birthday.data
        customer.NationalId = form.NationalId.data
        customer.TelephoneCountryCode = form.TelephoneCountryCode.data
        customer.Telephone = form.Telephone.data
        customer.EmailAddress = form.EmailAddress.data
        db.session.add(customer)
        db.session.commit()
    return render_template("newcustomer.html", formen=form )

if __name__  == "__main__":
    with app.app_context():
        #upgrade()

        #seedData(db)

        app.run()

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
