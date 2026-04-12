# Neo Bank – Mini Transaction Dashboard

This is a simple web app built using Flask and MySQL to view and filter bank transactions.

---

## What this does

* Shows the latest N transactions
* Lets you filter transactions between two dates
* Lets you view transactions of a specific user

---

## How it works

* The backend is built using Flask
* It connects to a MySQL database
* Based on the option selected in the form, it runs different SQL queries
* The results are sent to the HTML page and displayed in a table

---

## Tech used

* Flask
* MySQL
* HTML + CSS

---

## Files

```
neo-bank/
│── app.py
│── templates/
│   └── index.html
```

---

## Setup

1. Install requirements:

```
pip install flask mysql-connector-python
```

2. Create database:

```
CREATE DATABASE vaxtronbank;
```

3. Create table:

```
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    amount FLOAT,
    date DATE,
    description VARCHAR(255),
    type VARCHAR(50)
);
```

4. Run:

```
python app.py
```

Open:

```
http://127.0.0.1:5000/
```

---

## Note

This is just a basic project for learning/demo purposes.
