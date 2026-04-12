============================================================
   Neo Banking System - Project 6 : UPI Payment Simulator
   Full Stack Version  |  Team Number : 6
============================================================

PROJECT STRUCTURE
------------------

  UPI_Fullstack_Team6/
  |
  |-- backend/
  |     |-- app.py           Flask backend (main server)
  |     |-- database.py      SQLite database helper functions
  |     |-- requirements.txt Python packages needed
  |
  |-- frontend/
  |     |-- index.html       Login page
  |     |-- register.html    Register new user
  |     |-- dashboard.html   Main dashboard (balance + recent txns)
  |     |-- send_money.html  Send money via UPI
  |     |-- transactions.html View transaction history
  |     |-- style.css        All CSS styles
  |
  |-- README.txt             This file


TECH STACK USED
----------------

  Backend  : Python + Flask + SQLite
  Frontend : HTML + CSS + JavaScript (Vanilla)
  Database : SQLite (file-based, no installation needed)


HOW TO RUN
-----------

STEP 1 : Install Python packages

  Open terminal/command prompt in the backend/ folder
  and type :

      pip install -r requirements.txt

STEP 2 : Start the Backend Server

  Still in the backend/ folder, type :

      python app.py

  You should see :
      Neo Bank UPI Simulator - Backend Running
      Server : http://127.0.0.1:5000

STEP 3 : Open the Frontend

  Open the frontend/ folder
  Double click on   index.html   to open it in browser

  OR right-click index.html --> Open with --> Chrome/Firefox


SAMPLE USERS (Added automatically on first run)
-------------------------------------------------

  UPI ID             Name           Balance
  sayan@okicici      sayan Mondal   Rs. 5000
  team6@ybl          team6 Verma    Rs. 2000
  csbs@okhdfcbank    csbs Gupta     Rs. 8000


PAGES EXPLAINED
----------------

  Login Page       : Enter your UPI ID to login
  Register Page    : Create a new user account
  Dashboard        : See your balance and recent transactions
  Send Money       : Transfer money to any registered UPI ID
  Transactions     : View last N transactions with filter option


API ROUTES (Backend)
---------------------

  POST  /register            Register a new user
  POST  /login               Login with UPI ID
  GET   /balance/<upi_id>    Get current balance
  POST  /send                Send money via UPI
  GET   /transactions/<upi>  Get last N transactions
  GET   /users               Get all users (for testing)


NOTES
------

  - The database file (neobank.db) is created automatically
    in the backend/ folder when you run the server
  - No internet connection needed (runs fully offline)
  - Both backend and frontend must be running at the same time


============================================================
   Team 6  |  Neo Banking Project  |  Project 6
============================================================
