# Back-end of the app
from flask import Flask, request, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

def control_valve(valve_id, action):
    print(f"Controlling {valve_id}: {action}")
    # Add hardware control logic here

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/api/set-time', methods=['POST'])
def set_time():
    data = request.json
    valve_id = data['deviceId']
    action = data['action']
    time = data['time']

    # Convert 'time' to a schedule format and add to scheduler
    # Example: scheduler.add_job(control_valve, trigger='cron', hour=time_hour, minute=time_minute, args=[valve_id, action])

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
