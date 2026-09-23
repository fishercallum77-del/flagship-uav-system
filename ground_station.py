import csv
import math


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


def get_current_uav_status(telemetry_history):
    if not telemetry_history:
        return None

    latest_telemetry = telemetry_history[-1]

    return {
        "latitude": latest_telemetry["latitude"],
        "longitude": latest_telemetry["longitude"],
        "altitude": latest_telemetry["altitude"],
        "speed": latest_telemetry["speed"],
        "heading": latest_telemetry["heading"],
        "battery": latest_telemetry["battery"],
        "flight_state": latest_telemetry["flight_state"],
        "flight_mode": latest_telemetry["flight_mode"],
        "current_waypoint": latest_telemetry["current_waypoint"],
        "distance_to_waypoint": latest_telemetry["distance_to_waypoint"]
    }


def calculate_total_distance(telemetry_history):
    if len(telemetry_history) < 2:
        return 0

    total_distance = 0

    for i in range(1, len(telemetry_history)):
        previous = telemetry_history[i - 1]
        current = telemetry_history[i]

        north_difference = (
            current["latitude"] - previous["latitude"]
        ) * 111000

        east_difference = (
            current["longitude"] - previous["longitude"]
        ) * 111000

        distance = math.sqrt(
            north_difference ** 2 + east_difference ** 2
        )

        total_distance += distance

    return total_distance


def get_mission_summary(telemetry_history):
    if not telemetry_history:
        return None

    first_telemetry = telemetry_history[0]
    latest_telemetry = telemetry_history[-1]

    mission_duration = (
        latest_telemetry["simulation_time"]
        - first_telemetry["simulation_time"]
    )

    starting_battery = first_telemetry["battery"]
    current_battery = latest_telemetry["battery"]

    battery_consumed = starting_battery - current_battery

    highest_altitude = max(
        telemetry["altitude"]
        for telemetry in telemetry_history
    )

    total_distance = calculate_total_distance(telemetry_history)

    return {
        "telemetry_records": len(telemetry_history),
        "mission_duration": mission_duration,
        "starting_position": (
            first_telemetry["latitude"],
            first_telemetry["longitude"]
        ),
        "current_position": (
            latest_telemetry["latitude"],
            latest_telemetry["longitude"]
        ),
        "starting_battery": starting_battery,
        "current_battery": current_battery,
        "battery_consumed": battery_consumed,
        "highest_altitude": highest_altitude,
        "total_distance": total_distance,
        "current_waypoint": latest_telemetry["current_waypoint"]
    }


def display_uav_status(status):
    print()
    print("===== UAV STATUS =====")
    print(f"Position: {status['latitude']}, {status['longitude']}")
    print(f"Altitude: {status['altitude']} m")
    print(f"Speed: {status['speed']} m/s")
    print(f"Heading: {status['heading']:.2f}°")
    print(f"Battery: {status['battery']:.1f}%")
    print(f"Flight State: {status['flight_state']}")
    print(f"Flight Mode: {status['flight_mode']}")
    print(f"Current Waypoint: {status['current_waypoint']}")
    print(f"Distance to Waypoint: {status['distance_to_waypoint']:.2f} m")
    print("======================")


telemetry = load_telemetry("telemetry.csv")

print(f"Loaded telemetry records: {len(telemetry)}")

current_status = get_current_uav_status(telemetry)

display_uav_status(current_status)

mission_summary = get_mission_summary(telemetry)

print()
print("===== MISSION SUMMARY =====")
print(f"Telemetry Records: {mission_summary['telemetry_records']}")
print(f"Mission Duration: {mission_summary['mission_duration']} seconds")
print(f"Starting Battery: {mission_summary['starting_battery']:.1f}%")
print(f"Current Battery: {mission_summary['current_battery']:.1f}%")
print(f"Battery Consumed: {mission_summary['battery_consumed']:.1f}%")
print(f"Highest Altitude: {mission_summary['highest_altitude']:.1f} m")
print(f"Total Distance: {mission_summary['total_distance']:.1f} m")
print(f"Current Waypoint: {mission_summary['current_waypoint']}")
print("==========================")