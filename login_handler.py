from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login', methods=['POST'])
def login_user():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pass')
        # Check the user's credentials in the database
        conn = sqlite3.connect('aiaa.db')
        cursor = conn.cursor()
        cursor.execute("SELECT email, password, name FROM users WHERE email=?", (email,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data and user_data[1] == password:
            session['name'] = user_data[2]  # Store user ID in the session
            session['username'] = user_data[0]  # Store user ID in the session
            session.permanent = True  # Use a permanent session
            return redirect('home')

        else:
            # Authentication failed
            flash('Invalid email or password')

    return render_template("login.html")
