from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
scheduler = BackgroundScheduler()
scheduler.start()

valve_status = {
    "valve1": "closed",
    "valve2": "closed",
    "valve3": "closed",
    "valve4": "closed"
}

def control_valve(valve_id, action):
    global valve_status
    print(f"Controlling {valve_id}: {action}")
    valve_status[valve_id] = action

# New function to parse time and add job to the scheduler
def schedule_valve_operation(valve_id, action, time_str):
    time = datetime.strptime(time_str, '%H:%M').time()
    scheduler.add_job(
        func=control_valve,
        trigger='cron',
        hour=time.hour,
        minute=time.minute,
        args=[valve_id, action],
        replace_existing=True
    )
    print(f"Scheduled {valve_id} to {action} at {time_str}")


@app.route('/')
def index():
    if 'user_email' in session:
        return render_template('frontend.html')
    else:
        return redirect(url_for('login'))


@app.route('/api/set-time', methods=['POST'])
def set_time():
    data = request.json
    valve_id = data['deviceId']
    action = data['action']
    time = data['time']
    schedule_valve_operation(valve_id, action, time)
    return jsonify(success=True)


# New endpoint to handle immediate valve status changes
@app.route('/api/change-valve-status', methods=['POST'])
def change_valve_status():
    data = request.json
    valve_id = data['valveId']
    action = data['action']

    # Call control_valve directly
    control_valve(valve_id, action)

    return jsonify(success=True, status=valve_status[valve_id])


@app.route('/api/get-valve-status', methods=['GET'])
def get_valve_status():
    global valve_status
    return jsonify(valve_status)

# Login system
ALLOWED_EMAILS = {"betroy.ieu2022@student.ie.edu",
                  "jfernandez.ieu2022@student.ie.edu",
                  "sverdugo.ieu2022@student.ie.edu",
                  "ffruhling.ieu2022@student.ie.edu",
                  "Ptorrado.ieu2022@student.ie.edu"}

SHARED_PASSWORD = "password"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in ALLOWED_EMAILS and password == SHARED_PASSWORD:
            session['user_email'] = email  # Log in the user
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your credentials.')
            return redirect(url_for('login'))
    return render_template('loginSystem.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return '', 200


if __name__ == '__main__':
    app.run(debug=True)
