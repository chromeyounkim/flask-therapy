from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_FILE = 'test.db'

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                dob TEXT NOT NULL,
                therapist TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    return render_template('form.html', errors=[])

@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    dob = request.form.get('dob', '').strip()
    therapist = request.form.get('therapist', '').strip()

    errors = []
    if not first_name:
        errors.append("First name is required.")
    if not last_name:
        errors.append("Last name is required.")
    if not dob:
        errors.append("Date of Birth is required.")
    if not therapist:
        errors.append("Therapist name is required.")

    try:
        dob_date = datetime.strptime(dob, '%Y-%m-%d')
        if dob_date >= datetime.today():
            errors.append("Date of Birth must be in the past.")
    except ValueError:
        errors.append("Invalid Date of Birth format. Use YYYY-MM-DD.")

    if errors:
        return render_template('form.html', errors=errors,
                               first_name=first_name,
                               last_name=last_name,
                               dob=dob,
                               therapist=therapist)

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO patients (first_name, last_name, dob, therapist)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, dob, therapist))
        conn.commit()

    return render_template('confirmation.html',
                           first_name=first_name,
                           last_name=last_name,
                           dob=dob,
                           therapist=therapist)

if __name__ == '__main__':
    init_db()
    app.run()