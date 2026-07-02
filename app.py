from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

API_KEY = "super-secret-key-12345"

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, password TEXT)")
    c.execute("INSERT INTO users VALUES (1, 'admin', 'admin123')")
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return "Welcome to the completely secure app!"

@app.route("/login")
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    result = c.execute(query).fetchall()

    if result:
        return "Login successful!"
    return "Invalid credentials"


@app.route("/ping")
def ping():
    host = request.args.get("host")
    return os.popen(f"ping -c 1 {host}").read()


@app.route("/calc")
def calc():
    expr = request.args.get("expr")
    return str(eval(expr))


@app.route("/config")
def config():
    return {
        "api_key": API_KEY,
        "debug": True,
        "db_path": "users.db"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)