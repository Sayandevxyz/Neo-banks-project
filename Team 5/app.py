from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="77$@gmail.com",
        database="vaxtronbank"
    )

@app.route("/", methods=["GET", "POST"])
def home():
    rows = []

    if request.method == "POST":
        option = request.form.get("option")

        conn = get_connection()
        cursor = conn.cursor()

        if option == "last":
            n = int(request.form.get("n"))
            cursor.execute(
                "SELECT * FROM transactions ORDER BY date DESC LIMIT %s",
                (n,)
            )

        elif option == "date":
            start = request.form.get("start")
            end = request.form.get("end")
            cursor.execute(
                "SELECT * FROM transactions WHERE date BETWEEN %s AND %s",
                (start, end)
            )

        elif option == "user":
            user_id = int(request.form.get("user_id"))
            cursor.execute(
                "SELECT * FROM transactions WHERE user_id = %s",
                (user_id,)
            )

        rows = cursor.fetchall()
        conn.close()

    return render_template("index.html", data=rows)

app.run(debug=True)