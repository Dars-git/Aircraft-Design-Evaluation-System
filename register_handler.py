from flask import Blueprint, render_template, request, session, redirect, flash
import sqlite3

from Document_Store import initialize_user

register_blueprint = Blueprint('register', __name__)

@register_blueprint.route('/register', methods=['POST'])
def register_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        # Check if the password and confirm_password match
        if password != confirm_password:
            # You may want to handle this case and return an error message
            flash('Password and confirm password dose not match')
            return render_template("register.html")

        # Store user data in the database
        conn = sqlite3.connect('aiaa.db')
        cursor = conn.cursor()
        print(name, email, password)
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        conn.close()
        session['name'] = name  # Store user ID in the session
        session['username'] = email  # Store user ID in the session
        session.permanent = True  # Use a permanent session
        initialize_user(email)
        return redirect('home')



