# main.py
from flask import Flask, jsonify, request, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required to use session

# Temporary database (username: password)
TEMP_USERS = {
    "leonard": "12345",
    "admin": "admin123"
}

@app.route("/")
def root():
    return jsonify({"status": "ok", "version": "1.0.0"})

@app.route("/add/<int:a>/<int:b>")
def add(a, b):
    return jsonify({"result": a + b})

@app.route("/login", methods=["POST"])
def login():
    """
    Login endpoint using temporary database.
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in TEMP_USERS and TEMP_USERS[username] == password:
        session["logged_in"] = True
        session["username"] = username
        return jsonify({"message": "Login success"}), 200
        
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/subtract/<int:a>/<int:b>")
def subtract(a, b):
    """
    Protected route - only accessible after login.
    """
    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({"result": a - b}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
