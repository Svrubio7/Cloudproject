import requests
import time

# The URL of the Flask app to get the status of the valves
valve_status_url = 'http://127.0.0.1:5000/api/get-valve-status'

def get_valve_status():
    try:
        # Send a GET request to the Flask app
        response = requests.get(valve_status_url)
        response.raise_for_status()  # will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Something Else:",err)

    # Assuming the response is JSON and has a specific structure
    if response and response.status_code == 200:
        valve_status = response.json()
        return valve_status
    else:
        return None

def simulate_hardware_logic(valve_status):
    if valve_status:
        # Here you can add logic to simulate hardware behavior
        for valve_id, status in valve_status.items():
            print(f"Simulator: {valve_id} is currently {status}")

            # Example logic: if valve is 'open', simulate some operation
            if status == 'open':
                print(f"Simulator: Operating {valve_id}")
            else:
                print(f"Simulator: {valve_id} is idle")

# Run the simulation indefinitely, checking the valve status every 5 seconds
try:
    while True:
        valve_status = get_valve_status()
        simulate_hardware_logic(valve_status)
        time.sleep(5)  # Wait for 5 seconds before checking again
except KeyboardInterrupt:
    print("Simulation stopped.")
