from flask import Flask, request, jsonify
from flask_cors import CORS

from backend import login_user, resend_otp, verify_otp

app = Flask(__name__)
CORS(app)

# ================= LOGIN =================
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    result = login_user(username, password)

    return jsonify(result)


# ================= RESEND OTP =================
@app.route("/resend-otp", methods=["POST"])
def resend():
    data = request.json
    username = data["username"]

    result = resend_otp(username)

    return jsonify(result)


# ================= VERIFY OTP =================
@app.route("/verify-otp", methods=["POST"])
def verify():
    data = request.json
    username = data["username"]
    otp = data["otp"]

    result = verify_otp(username, otp)

    return jsonify(result)


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)