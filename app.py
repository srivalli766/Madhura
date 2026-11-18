from flask import Flask, render_template, request, make_response, session, redirect, url_for
from functools import wraps
from models.space_health_risk import assess_space_health
import csv
import io
from models.health_assessment import assess_health
from database import (
    create_table,
    save_health_data,
    get_health_records,
    create_astronaut_table,
    register_astronaut,
    verify_astronaut
)
from models.trend_analysis import analyze_trends

app = Flask(__name__)
app.secret_key = "astrocare_demo_secret_key"

# Create database table
create_table()
create_astronaut_table()
def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return function(*args, **kwargs)
    return wrapper


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    health_data = None
    assessment = None
    space_assessment = None
    error = None

    if request.method == 'POST':
        try:
            health_data = {
                'heart_rate': float(request.form['heart_rate']),
                'systolic': float(request.form['systolic']),
                'diastolic': float(request.form['diastolic']),
                'temperature': float(request.form['temperature']),
                'glucose': float(request.form['glucose']),
                'glucose_type': request.form['glucose_type'].strip().lower(),
                'hours_since_meal': float(request.form['hours_since_meal']),
                'sleep': float(request.form['sleep']),
                'mood': request.form['mood'].strip().lower()
            }

            if not all(
                value > 0
                for key, value in health_data.items()
                if key not in ['mood', 'glucose_type', 'hours_since_meal']
            ):
                raise ValueError()

            if not (
                20 <= health_data['heart_rate'] <= 250
                and 50 <= health_data['systolic'] <= 250
                and 30 <= health_data['diastolic'] <= 150
                and 30 <= health_data['temperature'] <= 45
                and 20 <= health_data['glucose'] <= 600
                and 0 <= health_data['sleep'] <= 24
                and 0 <= health_data['hours_since_meal'] <= 24
            ):
                raise ValueError()

            assessment = assess_health(health_data)

            space_assessment = assess_space_health({
                'heart_rate': health_data['heart_rate'],
                'temperature': health_data['temperature'],
                'glucose': health_data['glucose'],
                'glucose_type': health_data['glucose_type'],
                'hours_since_meal': health_data['hours_since_meal'],
                'systolic': health_data['systolic'],
                'diastolic': health_data['diastolic'],
                'sleep_hours': health_data['sleep'],
                'mood': health_data['mood']
            })
            print("GLUCOSE TYPE:", health_data['glucose_type'])
            print("HOURS SINCE MEAL:", health_data['hours_since_meal'])
            save_health_data(health_data)
            return render_template(
    'results.html',
    health_data=health_data,
    assessment=assessment,
    space_assessment=space_assessment
)

        except (ValueError, KeyError):
            health_data = None
            assessment = None
            space_assessment = None
            error = "Invalid measurements. Please check your entries."

    return render_template(
        'dashboard.html',
        health_data=health_data,
        assessment=assessment,
        space_assessment=space_assessment,
        error=error
    )
@app.route('/history')
@login_required
def history():

    records = get_health_records()
    trends = analyze_trends(records)
    total_records = len(records)

    return render_template(
        'history.html',
        records=records,
        trends=trends,
        total_records=total_records
    )
@app.route('/download')
def download():
    records = get_health_records()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        'ID', 'Heart Rate', 'Systolic',
        'Diastolic', 'Temperature',
        'Glucose', 'Sleep', 'Mood'
    ])

    for record in records:
        writer.writerow([
            record['id'],
            record['heart_rate'],
            record['systolic'],
            record['diastolic'],
            record['temperature'],
            record['glucose'],
            record['sleep'],
            record['mood']
        ])

    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = (
        'attachment; filename=astrocare_records.csv'
    )
    response.headers['Content-Type'] = 'text/csv'

    return response
@app.route('/hazards')
def hazards():
    records = get_health_records()

    latest_record = records[-1] if records else None

    return render_template(
        'hazards.html',
        latest_record=latest_record
    )
@app.route('/environment')
def environment():
    return render_template('environment.html')
@app.route('/profile', methods=['GET', 'POST'])
def profile():

    message = None

    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'agency': request.form['agency'],
            'mission': request.form['mission'],
            'role': request.form['role'],
            'duration': request.form['duration'],
            'username': request.form['username'],
            'password': request.form['password']
        }

        if register_astronaut(data):
            message = "Registration successful!"
        else:
            message = "Username already exists. Try another."

    return render_template('profile.html', message=message)
@app.route('/login', methods=['GET', 'POST'])
def login():

    message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if verify_astronaut(username, password):
            session["username"] = username
            return redirect(url_for('dashboard'))
        else:
            message = "Invalid username or password."

    return render_template('login.html', message=message)
if __name__ == '__main__':
    app.run(debug=True)