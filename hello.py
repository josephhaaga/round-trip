import datetime
import os
import time

import requests

API_KEY = os.getenv("API_KEY")
URL = "https://maps.googleapis.com/maps/api/directions/json"


def get_travel_times(origin, destination, time_at_destination: datetime.timedelta):
    getting_there = requests.get(
        URL, params={"origin": origin, "destination": destination, "key": API_KEY}
    ).json()
    time_to_get_there = getting_there["routes"][0]["legs"][0]["duration"]

    now = datetime.datetime.now()
    arrival_time = now + datetime.timedelta(seconds=time_to_get_there["value"])
    departure_time = arrival_time + datetime.timedelta(
        seconds=time_at_destination.seconds
    )

    time.sleep(10)

    getting_back = requests.get(
        URL,
        params={
            "origin": destination,
            "destination": origin,
            "key": API_KEY,
            "departure_time": departure_time.strftime("%s"),
        },
    ).json()
    time_to_get_back = getting_back["routes"][0]["legs"][0]["duration"]

    print(
        f"It'll take {time_to_get_there['text']} to get there, and {time_to_get_back['text']} to get back."
    )


def main():
    origin = "1600 Pennsylvania Avenue NW, Washington, DC 20500"
    destination = "2441 Market St NE, Washington, DC 20018" # Costco
    time_at_destination = datetime.timedelta(hours=2)
    print()
    get_travel_times(origin, destination, time_at_destination)


if __name__ == "__main__":
    raise SystemExit(main())
