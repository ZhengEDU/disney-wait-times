from flask import Flask, render_template, request
import requests
import difflib

app = Flask(__name__)

quitInputs = ["quit", "stop", "q"]

def get_live_wait_times():
    urls = [
        "https://queue-times.com/parks/16/queue_times.json",  # Disneyland
        "https://queue-times.com/parks/17/queue_times.json"   # California Adventure
    ]

    ride_wait_times = {}

    for url in urls:
        response = requests.get(url)
        data = response.json()

        for land in data["lands"]:
            for ride in land["rides"]:
                if ride["is_open"]:
                    ride_wait_times[ride["name"].lower()] = ride["wait_time"]

    return ride_wait_times


@app.route("/", methods=["GET", "POST"])
def home():
    wait_time = None
    ride_name = None
    error = None

    if request.method == "POST":
        user_input = request.form["ride"].lower()
        ride_wait_times = get_live_wait_times()

        if user_input in quitInputs:
            error = "Please close the tab to quit 🙂"

        elif user_input in ride_wait_times:
            ride_name = user_input
            wait_time = ride_wait_times[ride_name]

        else:
            matches = difflib.get_close_matches(
                user_input,
                ride_wait_times.keys(),
                n=1,
                cutoff=0.5
            )
            if matches:
                ride_name = matches[0]
                wait_time = ride_wait_times[ride_name]
            else:
                error = "Ride not found. Try again."

    return render_template(
        "index.html",
        ride=ride_name,
        wait_time=wait_time,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
