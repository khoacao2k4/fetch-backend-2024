from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import os
from datetime import datetime

app = Flask(__name__)

# SQLite database configuration
DATABASE_FILE = "points.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE_FILE}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable Flask-SQLAlchemy's modification tracking

db = SQLAlchemy(app)


# Define the Transaction model
class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    payer = db.Column(db.String, nullable=False)
    init_points = db.Column(db.Integer, nullable=False) # points intially added (for documentation purpose)
    remain_points = db.Column(db.Integer, nullable=False) # actual points after user spend
    timestamp = db.Column(db.DateTime, nullable=False)


# Define the Balance model
class Balance(db.Model):
    __tablename__ = 'balances'
    payer = db.Column(db.String, primary_key=True)
    points = db.Column(db.Integer, nullable=False, default=0)


# Initialize the database
def initialize_database():
    """
    Initialize the SQLite database and create tables if they don't exist.

    This function checks if the database file exists. If not, it creates the
    database and initializes the required tables. Otherwise, do nothing.
    """
    if not os.path.exists(DATABASE_FILE):
        with app.app_context():
            db.create_all()
            print(f"Database created: {DATABASE_FILE}")
    else:
        print(f"Database already exists: {DATABASE_FILE}")

@app.route('/add', methods=['POST'])
def add_points():
    """
    Add points to a payer's balance and record the transaction.

    This endpoint expects a JSON payload with 'payer', 'points', and 'timestamp'.
    It updates the payer's balance and logs the transaction in the database.
    
    Returns:
        An empty response with a 200 status code upon successful completion.
    """
    data = request.json
    # Check if required fields are present
    if not data or'payer' not in data or 'points' not in data or 'timestamp' not in data:
        return jsonify({"error": "Missing required fields (payer, points, timestamp)."}), 400
    
    payer = data['payer']
    points = data['points']
    timestamp = datetime.fromisoformat(data['timestamp'].replace("Z", "+00:00"))

    # If negative points, handle by deducting from existing transactions (for convenient spending transaction)
    if points < 0:
        transactions = (
            Transaction.query
            .filter(Transaction.payer==payer, Transaction.remain_points>0)
            .order_by(Transaction.timestamp.asc())
            .all()
        )
        remaining_points = abs(points)

        for transaction in transactions:
            if remaining_points == 0:
                break

            # Deduct points from the current transaction
            spendable_points = min(transaction.remain_points, remaining_points)
            transaction.remain_points -= spendable_points
            remaining_points -= spendable_points

        if remaining_points > 0:
            return jsonify({"error": "Cannot complete transaction, payer's balance cannot go negative."}), 400

    # Add transaction to the database
    new_transaction = Transaction(payer=payer, init_points=points, remain_points=points, timestamp=timestamp)
    db.session.add(new_transaction)

    # Update the payer's balance
    # return error if payer's balance goes negative
    payer_balance = db.session.query(Balance).get(payer)
    if payer_balance is None:
        payer_balance = Balance(payer=payer, points=points)
        db.session.add(payer_balance)
    else:
        payer_balance.points += points

    # Commit the changes
    db.session.commit()
    # Return a success response with the transaction ID
    return jsonify({"message": "Transaction added successfully.", "id_transaction": new_transaction.id}), 200


@app.route('/spend', methods=['POST'])
def spend_points():
    data = request.json
    # Check if required fields are present
    if not data or 'points' not in data:
        return jsonify({"error": "Missing required fields (points)."}), 400
    # Check if points is negative
    points_spend = data['points']
    if points_spend < 0:
        return jsonify({"error": "'points' cannot be negative."}), 400
    elif points_spend == 0:
        return jsonify([]), 200

    # Calculate total points from all payers
    total_points = db.session.query(func.sum(Balance.points)).scalar() or 0
    if points_spend > total_points:
        return jsonify({"error": "Not enough points to spend."}), 400

    # Get transactions ordered by timestamp 
    transactions = Transaction.query.order_by(Transaction.timestamp.asc()).all()
    spent = {}

    for transaction in transactions:
        payer, transaction_points = transaction.payer, transaction.remain_points

        # Skip negative transactions since they don't contribute to available points
        if transaction_points <= 0:
            continue

        # Deduct points from the current transaction
        spendable_points = min(transaction_points, points_spend)
        transaction.remain_points -= spendable_points
        points_spend -= spendable_points

        # Add to the spent dict
        spent[payer] = spent.get(payer, 0) + spendable_points

        if points_spend == 0:
            break
    
    response = []
    # Update payer balance
    for payer, spent_points in spent.items():
        balance = Balance.query.filter_by(payer=payer).first()
        balance.points -= spent_points
        response.append({"payer": payer, "points": -spent_points})\
    
    # Commit the transaction and balance updates
    db.session.commit()
    return jsonify(response), 200


@app.route('/balance', methods=['GET'])
def get_balance():
    balances = Balance.query.all()
    return jsonify({balance.payer: balance.points for balance in balances}), 200


if __name__ == '__main__':
    initialize_database()  # Create the database and tables if they don't exist
    app.run(debug=True, port=8000)
