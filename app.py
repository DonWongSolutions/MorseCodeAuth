from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = "Thisisverysecret"
USERS_FILE = "users.json"

def load_users():
    with open(USERS_FILE, 'r') as file:
        return json.load(file)

def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

def is_valid_morse_code(password):
    return re.fullmatch(r'[.\- ]*', password) is not None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Morse code input

        if not is_valid_morse_code(password):
            flash('Invalid password format. Use only dots (.) and dashes (-).')
            return redirect(url_for('register'))

        users = load_users()

        if any(user['username'] == username for user in users):
            flash('Username already exists. Please choose another one.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        users.append({"username": username, "password": hashed_password})
        save_users(users)
        flash('Registration successful!')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not is_valid_morse_code(password):
            flash('Invalid password format. Use only dots (.) and dashes (-).')
            return redirect(url_for('login'))

        users = load_users()
        user = next((user for user in users if user['username'] == username), None)

        if user and check_password_hash(user['password'], password):
            flash('Login successful!')
            return render_template('calculator.html')
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))

    return render_template('login.html')

if __name__ == '__main__':
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as file:
            json.dump([], file)
    app.run(debug=True)