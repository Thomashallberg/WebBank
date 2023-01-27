from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import db, seedData, Customer

# active page
# Sorting
# paging


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:my-secret-pw@localhost/Bank'
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
    return render_template("customer.html", customer=customer, activePage="customersPage" )



@app.route("/customers")
def customerspage():
    sortColumn = request.args.get('sortColumn', 'namn')
    sortOrder = request.args.get('sortOrder', 'asc')
    page = int(request.args.get('page', 1))
    searchWord = request.args.get('q','')

    listOfCustomers = Customer.query
#kundnummer, personnummer, namn, adress och city
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
