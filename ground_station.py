import csv


def parse_telemetry(telemetry):
    telemetry["simulation_time"] = float(telemetry["simulation_time"])
    telemetry["latitude"] = float(telemetry["latitude"])
    telemetry["longitude"] = float(telemetry["longitude"])
    telemetry["altitude"] = float(telemetry["altitude"])
    telemetry["speed"] = float(telemetry["speed"])
    telemetry["battery"] = float(telemetry["battery"])
    telemetry["heading"] = float(telemetry["heading"])
    telemetry["target_heading"] = float(telemetry["target_heading"])
    telemetry["heading_difference"] = float(telemetry["heading_difference"])
    telemetry["current_waypoint"] = int(telemetry["current_waypoint"])
    telemetry["distance_to_waypoint"] = float(
        telemetry["distance_to_waypoint"]
    )

    return telemetry


def validate_telemetry(telemetry):
    required_fields = [
        "simulation_time",
        "latitude",
        "longitude",
        "altitude",
        "speed",
        "battery",
        "heading",
        "target_heading",
        "heading_difference",
        "flight_state",
        "flight_mode",
        "current_waypoint",
        "distance_to_waypoint"
    ]

    errors = []

    for field in required_fields:
        if field not in telemetry:
            errors.append(f"Missing field: {field}")

    if "battery" in telemetry:
        if telemetry["battery"] < 0 or telemetry["battery"] > 100:
            errors.append("Battery must be between 0 and 100")

    if "heading" in telemetry:
        if telemetry["heading"] < 0 or telemetry["heading"] >= 360:
            errors.append("Heading must be between 0 and 359.99 degrees")

    if "target_heading" in telemetry:
        if telemetry["target_heading"] < 0 or telemetry["target_heading"] >= 360:
            errors.append(
                "Target heading must be between 0 and 359.99 degrees"
            )

    if "altitude" in telemetry:
        if telemetry["altitude"] < 0:
            errors.append("Altitude cannot be negative")

    if "speed" in telemetry:
        if telemetry["speed"] < 0:
            errors.append("Speed cannot be negative")

    return errors


def validate_telemetry_consistency(previous_telemetry, telemetry):
    errors = []

    expected_time = previous_telemetry["simulation_time"] + 1

    if telemetry["simulation_time"] != expected_time:
        errors.append(
            "Simulation time is not progressing correctly"
        )

    return errors


def load_telemetry(filename):
    telemetry_history = []
    previous_telemetry = None

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            telemetry = parse_telemetry(row)

            validation_errors = validate_telemetry(telemetry)

            if validation_errors:
                print("Invalid telemetry record:")

                for error in validation_errors:
                    print(f"  - {error}")

                continue

            if previous_telemetry is not None:
                consistency_errors = validate_telemetry_consistency(
                    previous_telemetry,
                    telemetry
                )

                if consistency_errors:
                    print("Telemetry consistency error:")

                    for error in consistency_errors:
                        print(f"  - {error}")

                    continue

            previous_telemetry = telemetry
            telemetry_history.append(telemetry)

    return telemetry_history


telemetry = load_telemetry("telemetry.csv")

print(f"Loaded telemetry records: {len(telemetry)}")