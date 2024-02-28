from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopping.db'
db = SQLAlchemy(app)

# Define models
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.String(200), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    # Define other fields like products, total amount, etc.
    is_archived = db.Column(db.Boolean, default=False)

# Routes
@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'GET':
        customers = Customer.query.all()
        return jsonify([customer.serialize() for customer in customers])
    elif request.method == 'POST':
        data = request.json
        new_customer = Customer(name=data['name'], email=data['email'], address=data['address'])
        db.session.add(new_customer)
        db.session.commit()
        return jsonify(new_customer.serialize()), 201

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        orders = Order.query.all()
        return jsonify([order.serialize() for order in orders])
    elif request.method == 'POST':
        data = request.json
        new_order = Order(customer_id=data['customer_id'])
        # Populate other fields of the order
        db.session.add(new_order)
        db.session.commit()
        return jsonify(new_order.serialize()), 201

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)