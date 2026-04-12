# Neo Bank Authentication System

This project is a simple authentication system with OTP verification built using Python, Flask, and MySQL.

## Project Structure

The project is divided into separate components for better organization:

- app.py  
  Handles API routes using Flask. It receives requests from the frontend and calls backend functions.

- backend.py  
  Contains all core logic including:
  - Login validation
  - OTP generation
  - OTP verification
  - Resend OTP logic
  - Database operations

- templates/index.html  
  Contains the frontend UI for login and OTP verification.

## How It Works

1. User enters username and password in the frontend.
2. app.py receives the request and calls backend.py.
3. backend.py validates credentials and generates an OTP.
4. OTP is stored in the database.
5. User enters OTP in the frontend.
6. backend.py verifies the OTP and returns the result.

## Setup Instructions

1. Install required packages:
   pip install flask flask-cors mysql-connector-python

2. Create database:

   CREATE DATABASE neobank;

   USE neobank;

   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(50),
       password VARCHAR(50),
       email VARCHAR(100),
       otp VARCHAR(6),
       otp_expiry DATETIME,
       login_attempts INT DEFAULT 0,
       is_locked BOOLEAN DEFAULT FALSE,
       otp_resend_count INT DEFAULT 0
   );

3. Run the application:
   python app.py

4. Open the frontend:
   Open templates/index.html in your browser.

## Accessing OTP

The OTP is not sent through email or SMS in this project.  
To access the OTP, check the database directly using:

SELECT otp FROM users WHERE username = 'your_username';

## Notes

- OTP is stored in the database.
- Passwords are stored as plain text for simplicity.
- The project separates API and backend logic for clarity and modularity.
