from flask import Flask, request
import threading
import datetime

app = Flask(__name__)

valve_status = {
    'valve1': 'closed',
    'valve2': 'closed',
    'valve3': 'closed',
    'valve4': 'closed'
}

def schedule_valve(valve, action, time_str):
    time_format = "%H:%M"
    target_time = datetime.datetime.strptime(time_str, time_format).time()
    now = datetime.datetime.now().time()

    # Calculate time difference
    delta_seconds = (datetime.datetime.combine(datetime.date.today(), target_time) - 
                     datetime.datetime.combine(datetime.date.today(), now)).seconds

    if delta_seconds < 0:
        # If time is past, schedule for the next day
        delta_seconds += 86400  # seconds in a day

    threading.Timer(delta_seconds, change_valve_status, [valve, action]).start()

def change_valve_status(valve, action):
    global valve_status
    valve_status[valve] = action
    print(f"Valve {valve} is now {action}")

@app.route('/control', methods=['POST'])
def control():
    data = request.json
    valve = data['valve']
    action = data['action']
    time = data.get('time')

    if time:
        schedule_valve(valve, action, time)
    else:
        change_valve_status(valve, action)

    return f"Request to {action} {valve} received."

if __name__ == "__main__":
    app.run(debug=True)
