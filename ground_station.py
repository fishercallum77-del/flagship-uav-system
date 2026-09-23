import csv


def parse_telemetry(telemetry):

    telemetry["simulation_time"] = float(
        telemetry["simulation_time"]
    )

    telemetry["latitude"] = float(
        telemetry["latitude"]
    )

    telemetry["longitude"] = float(
        telemetry["longitude"]
    )

    telemetry["altitude"] = float(
        telemetry["altitude"]
    )

    telemetry["speed"] = float(
        telemetry["speed"]
    )

    telemetry["battery"] = float(
        telemetry["battery"]
    )

    telemetry["heading"] = float(
        telemetry["heading"]
    )

    telemetry["target_heading"] = float(
        telemetry["target_heading"]
    )

    telemetry["heading_difference"] = float(
        telemetry["heading_difference"]
    )

    telemetry["current_waypoint"] = int(
        telemetry["current_waypoint"]
    )

    telemetry["distance_to_waypoint"] = float(
        telemetry["distance_to_waypoint"]
    )

    return telemetry


def load_telemetry(filename):

    telemetry_history = []

    with open(
        filename,
        "r",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            telemetry = parse_telemetry(row)

            telemetry_history.append(telemetry)

    return telemetry_history


telemetry = load_telemetry(
    "telemetry.csv"
)

print(
    f"Loaded telemetry records: {len(telemetry)}"
)