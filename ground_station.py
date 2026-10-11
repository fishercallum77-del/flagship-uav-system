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
            errors.append(
                "Heading must be between 0 and 359.99 degrees"
            )

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
        errors.append("Simulation time is not progressing correctly")

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

    battery_consumed = (
        starting_battery - current_battery
    )

    highest_altitude = max(
        telemetry["altitude"]
        for telemetry in telemetry_history
    )

    total_distance = calculate_total_distance(
        telemetry_history
    )

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


def analyze_flight_states(telemetry_history):
    state_analysis = {}

    for telemetry in telemetry_history:
        state = telemetry["flight_state"]

        if state not in state_analysis:
            state_analysis[state] = {
                "records": 0,
                "start_time": telemetry["simulation_time"],
                "end_time": telemetry["simulation_time"],
                "starting_battery": telemetry["battery"],
                "current_battery": telemetry["battery"],
                "total_speed": 0
            }

        state_analysis[state]["records"] += 1

        state_analysis[state]["end_time"] = (
            telemetry["simulation_time"]
        )

        state_analysis[state]["current_battery"] = (
            telemetry["battery"]
        )

        state_analysis[state]["total_speed"] += (
            telemetry["speed"]
        )

    for state, data in state_analysis.items():
        data["duration"] = (
            data["end_time"]
            - data["start_time"]
            + 1
        )

        data["average_speed"] = (
            data["total_speed"]
            / data["records"]
        )

        data["battery_consumed"] = (
            data["starting_battery"]
            - data["current_battery"]
        )

        del data["total_speed"]

    return state_analysis


def analyze_movement(telemetry_history):
    if not telemetry_history:
        return None

    total_distance = calculate_total_distance(
        telemetry_history
    )

    speeds = [
        telemetry["speed"]
        for telemetry in telemetry_history
    ]

    altitudes = [
        telemetry["altitude"]
        for telemetry in telemetry_history
    ]

    turning_events = 0
    currently_turning = False

    for telemetry in telemetry_history:
        if telemetry["flight_mode"] == "TURNING":
            if not currently_turning:
                turning_events += 1

            currently_turning = True
        else:
            currently_turning = False

    return {
        "total_distance": total_distance,
        "average_speed": sum(speeds) / len(speeds),
        "maximum_speed": max(speeds),
        "average_altitude": sum(altitudes) / len(altitudes),
        "maximum_altitude": max(altitudes),
        "turning_events": turning_events
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
    print(
        f"Distance to Waypoint: "
        f"{status['distance_to_waypoint']:.2f} m"
    )
    print("======================")


telemetry = load_telemetry("telemetry.csv")

print(f"Loaded telemetry records: {len(telemetry)}")

current_status = get_current_uav_status(telemetry)

display_uav_status(current_status)

mission_summary = get_mission_summary(telemetry)

print()
print("===== MISSION SUMMARY =====")
print(
    f"Telemetry Records: "
    f"{mission_summary['telemetry_records']}"
)
print(
    f"Mission Duration: "
    f"{mission_summary['mission_duration']} seconds"
)
print(
    f"Starting Battery: "
    f"{mission_summary['starting_battery']:.1f}%"
)
print(
    f"Current Battery: "
    f"{mission_summary['current_battery']:.1f}%"
)
print(
    f"Battery Consumed: "
    f"{mission_summary['battery_consumed']:.1f}%"
)
print(
    f"Highest Altitude: "
    f"{mission_summary['highest_altitude']:.1f} m"
)
print(
    f"Total Distance: "
    f"{mission_summary['total_distance']:.1f} m"
)
print(
    f"Current Waypoint: "
    f"{mission_summary['current_waypoint']}"
)
print("==========================")


flight_state_analysis = analyze_flight_states(telemetry)

print()
print("===== FLIGHT STATE ANALYSIS =====")

for state, data in flight_state_analysis.items():
    print()
    print(state)
    print(f"Duration: {data['duration']} seconds")
    print(
        f"Average Speed: "
        f"{data['average_speed']:.2f} m/s"
    )
    print(
        f"Battery Consumed: "
        f"{data['battery_consumed']:.2f}%"
    )

print()
print("=================================")


movement_analysis = analyze_movement(telemetry)

print()
print("===== MOVEMENT ANALYSIS =====")
print(
    f"Total Distance: "
    f"{movement_analysis['total_distance']:.1f} m"
)
print(
    f"Average Speed: "
    f"{movement_analysis['average_speed']:.2f} m/s"
)
print(
    f"Maximum Speed: "
    f"{movement_analysis['maximum_speed']:.2f} m/s"
)
print(
    f"Average Altitude: "
    f"{movement_analysis['average_altitude']:.2f} m"
)
print(
    f"Maximum Altitude: "
    f"{movement_analysis['maximum_altitude']:.2f} m"
)
print(
    f"Turning Events: "
    f"{movement_analysis['turning_events']}"
)
print("============================")