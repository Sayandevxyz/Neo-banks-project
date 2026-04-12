# ============================================================
#  Neo Banking System - Project 6
#  UPI Payment Simulator - Backend (Flask)
#  Team Number : 6
# ============================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import datetime
import database   # our own database file

# create flask app
app = Flask(__name__)
CORS(app)   # this allows frontend to talk to backend

# -------------------------------------------------------
# Helper Function : Validate UPI ID Format
# -------------------------------------------------------

def validate_upi(upi_id):
    pattern = r"^[a-zA-Z0-9._-]+@[a-z]{3,10}$"
    if re.match(pattern, upi_id):
        return True
    return False


# -------------------------------------------------------
# Route 1 : Register a New User
# POST /register
# -------------------------------------------------------

@app.route("/register", methods=["POST"])
def register():

    # get data sent from frontend
    data = request.get_json()

    name    = data.get("name", "").strip()
    upi_id  = data.get("upi_id", "").strip()
    phone   = data.get("phone", "").strip()
    balance = data.get("balance", 0)

    # check all fields are filled
    if not name or not upi_id or not phone:
        return jsonify({"success": False, "message": "All fields are required"}), 400

    # check phone number
    if not phone.isdigit() or len(phone) != 10:
        return jsonify({"success": False, "message": "Phone number must be 10 digits"}), 400

    # check upi format
    if not validate_upi(upi_id):
        return jsonify({"success": False, "message": "Invalid UPI ID format. Use : username@bankcode"}), 400

    # check balance
    try:
        balance = float(balance)
    except:
        return jsonify({"success": False, "message": "Balance must be a number"}), 400

    if balance < 0:
        return jsonify({"success": False, "message": "Balance cannot be negative"}), 400

    # check if upi id already exists
    existing = database.get_user(upi_id)
    if existing:
        return jsonify({"success": False, "message": "This UPI ID is already registered"}), 400

    # save user in database
    database.add_user(name, upi_id, phone, balance)

    return jsonify({"success": True, "message": "User registered successfully!", "upi_id": upi_id})


# -------------------------------------------------------
# Route 2 : Login (just check if upi id exists)
# POST /login
# -------------------------------------------------------

@app.route("/login", methods=["POST"])
def login():

    data   = request.get_json()
    upi_id = data.get("upi_id", "").strip()

    if not validate_upi(upi_id):
        return jsonify({"success": False, "message": "Invalid UPI ID format"}), 400

    user = database.get_user(upi_id)

    if not user:
        return jsonify({"success": False, "message": "Account not found. Please register first."}), 404

    return jsonify({
        "success" : True,
        "message" : "Login successful",
        "user"    : {
            "name"    : user["name"],
            "upi_id"  : user["upi_id"],
            "phone"   : user["phone"],
            "balance" : user["balance"]
        }
    })


# -------------------------------------------------------
# Route 3 : Get User Balance
# GET /balance/<upi_id>
# -------------------------------------------------------

@app.route("/balance/<upi_id>", methods=["GET"])
def get_balance(upi_id):

    user = database.get_user(upi_id)

    if not user:
        return jsonify({"success": False, "message": "Account not found"}), 404

    return jsonify({
        "success" : True,
        "name"    : user["name"],
        "upi_id"  : user["upi_id"],
        "balance" : user["balance"]
    })


# -------------------------------------------------------
# Route 4 : Send Money
# POST /send
# -------------------------------------------------------

@app.route("/send", methods=["POST"])
def send_money():

    data         = request.get_json()
    sender_upi   = data.get("sender_upi", "").strip()
    receiver_upi = data.get("receiver_upi", "").strip()
    amount       = data.get("amount", 0)

    # validate upi ids
    if not validate_upi(sender_upi):
        return jsonify({"success": False, "message": "Sender UPI ID is invalid"}), 400

    if not validate_upi(receiver_upi):
        return jsonify({"success": False, "message": "Receiver UPI ID is invalid"}), 400

    # sender and receiver should not be same
    if sender_upi == receiver_upi:
        return jsonify({"success": False, "message": "You cannot send money to yourself"}), 400

    # check amount
    try:
        amount = float(amount)
    except:
        return jsonify({"success": False, "message": "Amount must be a number"}), 400

    if amount <= 0:
        return jsonify({"success": False, "message": "Amount must be greater than zero"}), 400

    # check if both accounts exist
    sender   = database.get_user(sender_upi)
    receiver = database.get_user(receiver_upi)

    if not sender:
        return jsonify({"success": False, "message": "Sender account not found"}), 404

    if not receiver:
        return jsonify({"success": False, "message": "Receiver account not found"}), 404

    # check sender balance
    if sender["balance"] < amount:
        return jsonify({
            "success" : False,
            "message" : "Insufficient balance. Your balance is Rs. " + str(sender["balance"])
        }), 400

    # do the transaction in database
    txn_id    = database.do_transaction(sender_upi, receiver_upi, amount)
    new_bal   = sender["balance"] - amount
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    return jsonify({
        "success"     : True,
        "message"     : "Transaction Successful!",
        "txn_id"      : txn_id,
        "amount"      : amount,
        "receiver"    : receiver_upi,
        "new_balance" : new_bal,
        "timestamp"   : timestamp
    })


# -------------------------------------------------------
# Route 5 : View Last N Transactions
# GET /transactions/<upi_id>?n=5
# -------------------------------------------------------

@app.route("/transactions/<upi_id>", methods=["GET"])
def get_transactions(upi_id):

    # get n from query parameter, default is 5
    n = request.args.get("n", 5)

    try:
        n = int(n)
    except:
        n = 5

    if n <= 0:
        n = 5

    user = database.get_user(upi_id)
    if not user:
        return jsonify({"success": False, "message": "Account not found"}), 404

    txns = database.get_transactions(upi_id, n)

    return jsonify({
        "success"      : True,
        "upi_id"       : upi_id,
        "transactions" : txns
    })


# -------------------------------------------------------
# Route 6 : Get All Users (for testing/admin)
# GET /users
# -------------------------------------------------------

@app.route("/users", methods=["GET"])
def get_all_users():
    users = database.get_all_users()
    return jsonify({"success": True, "users": users})


# -------------------------------------------------------
# Run the App
# -------------------------------------------------------

if __name__ == "__main__":
    database.create_tables()   # create tables if not exist
    database.add_sample_data() # add two sample users for testing
    print("\n  Neo Bank UPI Simulator - Backend Running")
    print("  Server : http://127.0.0.1:5000")
    print("  Open frontend/index.html in your browser\n")
    app.run(debug=True)
