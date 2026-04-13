from db import get_connection
from datetime import datetime


# ──────────────────────────────────────────────
#  SCORING ENGINE
# ──────────────────────────────────────────────

def calculate_credit_score(monthly_income, loan_repaid, overdraft_count, existing_loans):
    """
    Scoring model — returns (final_score, risk_category, breakdown_list)
    Base score : 300
    Max possible : ~900
    """
    breakdown = []
    score = 300
    breakdown.append({
        "label": "Base Score",
        "points": 300,
        "type": "neutral",
        "reason": "Starting baseline for all applicants"
    })

    # ── 1. Monthly Income Bracket (max +200 pts) ──────────────────────────
    if monthly_income >= 150000:
        pts = 200
        label = "Premium Income Bracket (₹1.5L+)"
    elif monthly_income >= 100000:
        pts = 170
        label = "High Income Bracket (₹1L – ₹1.5L)"
    elif monthly_income >= 75000:
        pts = 140
        label = "Upper-Mid Income Bracket (₹75K – ₹1L)"
    elif monthly_income >= 50000:
        pts = 110
        label = "Mid Income Bracket (₹50K – ₹75K)"
    elif monthly_income >= 30000:
        pts = 80
        label = "Lower-Mid Income Bracket (₹30K – ₹50K)"
    elif monthly_income >= 15000:
        pts = 50
        label = "Entry Income Bracket (₹15K – ₹30K)"
    else:
        pts = 20
        label = "Low Income Bracket (< ₹15K)"

    score += pts
    breakdown.append({
        "label": label,
        "points": pts,
        "type": "positive",
        "reason": "Income stability contributes to repayment capacity"
    })

    #2.Loans Repaid on Time (max +150 pts) 
    if loan_repaid > 0:
        repay_pts = min(loan_repaid * 30, 150)
        score += repay_pts
        breakdown.append({
            "label": f"Loans Repaid on Time ({loan_repaid})",
            "points": repay_pts,
            "type": "positive",
            "reason": "Timely repayment history strongly indicates creditworthiness"
        })
    else:
        breakdown.append({
            "label": "No Repayment History",
            "points": 0,
            "type": "neutral",
            "reason": "No loan repayment data available to score"
        })

    #3.Existing Active Loans (penalty, max −75 pts)
    if existing_loans > 0:
        loan_penalty = min(existing_loans * 15, 75)
        score -= loan_penalty
        breakdown.append({
            "label": f"Existing Active Loans ({existing_loans})",
            "points": -loan_penalty,
            "type": "negative",
            "reason": "Multiple open loans increase debt burden risk"
        })

    #4.Overdraft / Missed Payments (penalty, max −100 pts) 
    if overdraft_count > 0:
        od_penalty = min(overdraft_count * 20, 100)
        score -= od_penalty
        breakdown.append({
            "label": f"Overdraft / Missed Payments ({overdraft_count})",
            "points": -od_penalty,
            "type": "negative",
            "reason": "Overdrafts signal poor cash flow management"
        })

    #Clamp to 300–900 
    score = max(300, min(900, round(score, 2)))

    # Risk Category
    if score >= 750:
        risk = "Excellent"
    elif score >= 650:
        risk = "Good"
    elif score >= 500:
        risk = "Fair"
    else:
        risk = "Poor"

    return score, risk, breakdown


def generate_recommendations(score, overdraft_count, existing_loans, loan_repaid, monthly_income):
    """Returns a list of actionable advice strings."""
    advice = []

    if overdraft_count > 0:
        advice.append(f"Reduce overdrafts — you have {overdraft_count} recorded. Each overdraft deducts up to 20 pts.")
    if existing_loans >= 3:
        advice.append("Close or consolidate some active loans. High loan count reduces your score.")
    if loan_repaid == 0:
        advice.append("Take and repay a small loan on time — repayment history can add up to 150 pts.")
    if monthly_income < 30000:
        advice.append("Increasing your declared income bracket will significantly improve your base score.")
    if score >= 750:
        advice.append("Excellent credit! You are eligible for premium loan products and low interest rates.")
    elif score >= 650:
        advice.append("Good standing. Consistent repayments over 6 months can push you to Excellent tier.")
    elif score >= 500:
        advice.append("Fair risk tier. Focus on reducing overdrafts and repaying existing loans to improve.")
    else:
        advice.append("High risk tier. Avoid new loans, clear overdrafts, and build repayment history first.")

    return advice


# ──────────────────────────────────────────────
#  DATABASE OPERATIONS
# ──────────────────────────────────────────────

def evaluate_and_save(customer_id, customer_name, monthly_income,
                      existing_loans, loan_repaid, overdraft_count):
    score, risk, breakdown = calculate_credit_score(
        monthly_income, loan_repaid, overdraft_count, existing_loans
    )

    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Upsert credit_profiles
    cursor.execute("""
        INSERT INTO credit_profiles
            (customer_id, customer_name, monthly_income, existing_loans,
             loan_repaid, overdraft_count, credit_score, risk_category, evaluated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(customer_id) DO UPDATE SET
            customer_name   = excluded.customer_name,
            monthly_income  = excluded.monthly_income,
            existing_loans  = excluded.existing_loans,
            loan_repaid     = excluded.loan_repaid,
            overdraft_count = excluded.overdraft_count,
            credit_score    = excluded.credit_score,
            risk_category   = excluded.risk_category,
            evaluated_at    = excluded.evaluated_at
    """, (customer_id, customer_name, monthly_income,
          existing_loans, loan_repaid, overdraft_count,
          score, risk, now))

    # Always append to history
    cursor.execute("""
        INSERT INTO score_history (customer_id, score, risk_label, evaluated_at)
        VALUES (?, ?, ?, ?)
    """, (customer_id, score, risk, now))

    conn.commit()
    conn.close()

    recommendations = generate_recommendations(
        score, overdraft_count, existing_loans, loan_repaid, monthly_income
    )

    return {
        "customer_id": customer_id,
        "customer_name": customer_name,
        "credit_score": score,
        "risk_category": risk,
        "breakdown": breakdown,
        "recommendations": recommendations,
        "evaluated_at": now
    }


def get_profile(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM credit_profiles WHERE customer_id = ?", (customer_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def get_history(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT score, risk_label, evaluated_at
        FROM score_history
        WHERE customer_id = ?
        ORDER BY evaluated_at ASC
    """, (customer_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_profiles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM credit_profiles ORDER BY evaluated_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
