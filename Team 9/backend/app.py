from flask import Flask, request, jsonify
from flask_cors import CORS
from db import init_db
import models

app = Flask(__name__)
CORS(app)

# Initialise DB on startup
init_db()


# ──────────────────────────────────────────────
#  HEALTH CHECK
# ──────────────────────────────────────────────
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "module": "Credit Score Estimator — Team 9"}), 200


# ──────────────────────────────────────────────
#  POST /api/credit/evaluate
#  Body: { customer_id, customer_name, monthly_income,
#           existing_loans, loan_repaid, overdraft_count }
# ──────────────────────────────────────────────
@app.route("/api/credit/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json(force=True)

    required = ["customer_id", "monthly_income"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        customer_id    = int(data["customer_id"])
        customer_name  = str(data.get("customer_name", f"Customer {data['customer_id']}")).strip()
        monthly_income = float(data["monthly_income"])
        existing_loans = int(data.get("existing_loans", 0))
        loan_repaid    = int(data.get("loan_repaid", 0))
        overdraft_count = int(data.get("overdraft_count", 0))
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid data types: {str(e)}"}), 400

    if monthly_income < 0:
        return jsonify({"error": "monthly_income cannot be negative"}), 400
    if any(v < 0 for v in [existing_loans, loan_repaid, overdraft_count]):
        return jsonify({"error": "Loan/overdraft counts cannot be negative"}), 400

    result = models.evaluate_and_save(
        customer_id, customer_name, monthly_income,
        existing_loans, loan_repaid, overdraft_count
    )

    return jsonify({"success": True, "data": result}), 200


# ──────────────────────────────────────────────
#  GET /api/credit/profile/<id>
# ──────────────────────────────────────────────
@app.route("/api/credit/profile/<int:customer_id>", methods=["GET"])
def get_profile(customer_id):
    profile = models.get_profile(customer_id)
    if not profile:
        return jsonify({"error": f"No profile found for customer_id {customer_id}"}), 404
    return jsonify({"success": True, "data": profile}), 200


# ──────────────────────────────────────────────
#  GET /api/credit/history/<id>
# ──────────────────────────────────────────────
@app.route("/api/credit/history/<int:customer_id>", methods=["GET"])
def get_history(customer_id):
    history = models.get_history(customer_id)
    return jsonify({
        "success": True,
        "customer_id": customer_id,
        "total_evaluations": len(history),
        "data": history
    }), 200


# ──────────────────────────────────────────────
#  GET /api/credit/all  (admin)
# ──────────────────────────────────────────────
@app.route("/api/credit/all", methods=["GET"])
def get_all():
    profiles = models.get_all_profiles()
    return jsonify({
        "success": True,
        "total": len(profiles),
        "data": profiles
    }), 200


# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  Team 9 — Credit Score Estimator API")
    print("  Running on  http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
