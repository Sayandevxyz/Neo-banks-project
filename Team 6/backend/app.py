from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import datetime
import database  


app = Flask(__name__)
CORS(app)   

def validate_upi(upi_id):
    pattern = r"^[a-zA-Z0-9._-]+@[a-z]{3,10}$"
    if re.match(pattern, upi_id):
        return True
    return False




@app.route("/register", methods=["POST"])
def register():

    
    data = request.get_json()

    name    = data.get("name", "").strip()
    upi_id  = data.get("upi_id", "").strip()
    phone   = data.get("phone", "").strip()
    balance = data.get("balance", 0)
    Email   = data.get("Email", "").strip()

    
    if not name or not upi_id or not phone or not Email:
        return jsonify({"success": False, "message": "All fields are required"}), 400

    
    if not phone.isdigit() or len(phone) != 10:
        return jsonify({"success": False, "message": "Phone number must be 10 digits"}), 400

    
    if not validate_upi(upi_id):
        return jsonify({"success": False, "message": "Invalid UPI ID format. Use : username@bankcode"}), 400

    
    try:
        balance = float(balance)
    except:
        return jsonify({"success": False, "message": "Balance must be a number"}), 400

    if balance < 0:
        return jsonify({"success": False, "message": "Balance cannot be negative"}), 400

    
    existing = database.get_user(upi_id)
    if existing:
        return jsonify({"success": False, "message": "This UPI ID is already registered"}), 400

    
    database.add_user(name, upi_id, phone, balance, Email)

    return jsonify({"success": True, "message": "User registered successfully!", "upi_id": upi_id})




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
            "balance" : user["balance"],
            "Email"   : user["Email"],
        }
    })




@app.route("/balance/<upi_id>", methods=["GET"])
def get_balance(upi_id):

    user = database.get_user(upi_id)

    if not user:
        return jsonify({"success": False, "message": "Account not found"}), 404

    return jsonify({
        "success" : True,
        "name"    : user["name"],
        "upi_id"  : user["upi_id"],
        "balance" : user["balance"],
        "Email"   : user["Email"],
    })




@app.route("/send", methods=["POST"])
def send_money():

    data         = request.get_json()
    sender_upi   = data.get("sender_upi", "").strip()
    receiver_upi = data.get("receiver_upi", "").strip()
    amount       = data.get("amount", 0)
    Email        = data.get("email", "").strip()

    
    if not validate_upi(sender_upi):
        return jsonify({"success": False, "message": "Sender UPI ID is invalid"}), 400

    if not validate_upi(receiver_upi):
        return jsonify({"success": False, "message": "Receiver UPI ID is invalid"}), 400

    
    if sender_upi == receiver_upi:
        return jsonify({"success": False, "message": "You cannot send money to yourself"}), 400

   
    try:
        amount = float(amount)
    except:
        return jsonify({"success": False, "message": "Amount must be a number"}), 400

    if amount <= 0:
        return jsonify({"success": False, "message": "Amount must be greater than zero"}), 400

   
    sender   = database.get_user(sender_upi)
    receiver = database.get_user(receiver_upi)

    if not sender:
        return jsonify({"success": False, "message": "Sender account not found"}), 404

    if not receiver:
        return jsonify({"success": False, "message": "Receiver account not found"}), 404

    
    if sender["balance"] < amount:
        return jsonify({
            "success" : False,
            "message" : "Insufficient balance. Your balance is Rs. " + str(sender["balance"])
        }), 400

    
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




@app.route("/transactions/<upi_id>", methods=["GET"])
def get_transactions(upi_id):

    
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




@app.route("/users", methods=["GET"])
def get_all_users():
    users = database.get_all_users()
    return jsonify({"success": True, "users": users})




if __name__ == "__main__":
    database.create_tables()   # create tables if not exist
    database.add_sample_data() # add two sample users for testing
    print("\n  Neo Bank UPI Simulator - Backend Running")
    print("  Server : http://127.0.0.1:5000")
    print("  Open frontend/index.html in your browser\n")
    app.run(debug=True)
