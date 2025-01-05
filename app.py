# app.py
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Koneksi ke database
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  # Ganti dengan username MySQL Anda
        password='',  # Ganti dengan password MySQL Anda
        database='user_management'  # Ganti dengan nama database Anda
    )
    return connection

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Mengambil data pengguna dari database
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('index.html', users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('INSERT INTO users (username, role, email, password_hash) VALUES (%s, %s, %s, %s)', 
                       (username, role, email, hashed_password))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            return redirect(url_for('index'))
        else:
            return 'Invalid email or password'

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
