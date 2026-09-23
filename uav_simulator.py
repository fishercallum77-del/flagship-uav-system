import csv
import math
import time


# ============================================================
# SIMULATION SETTINGS
# ============================================================

time_step = 1.0
simulation_steps = 180
simulation_time = 0.0


# ============================================================
# UAV STATE
# ============================================================

uav = {
    "altitude": 150,
    "speed": 12.0,
    "vertical_speed": 5,
    "turn_rate": 10,
    "battery": 100,
    "heading": 90,
    "target_heading": 0,
    "latitude": 50.2085,
    "longitude": -5.4875,
    "flight_state": "CLIMBING"
}


# ============================================================
# WAYPOINTS
# ============================================================

waypoints = [
    {"latitude": 50.2100, "longitude": -5.4800},
    {"latitude": 50.2115, "longitude": -5.4750},
    {"latitude": 50.2090, "longitude": -5.4700}
]

current_waypoint = 0


# ============================================================
# TELEMETRY STORAGE
# ============================================================

telemetry_history = []


# ============================================================
# BATTERY
# ============================================================

def get_battery_consumption_rate(uav):

    if uav["flight_state"] == "CLIMBING":
        return 0.08

    elif uav["flight_state"] == "CRUISE":
        return 0.05

    elif uav["flight_state"] == "LOW_BATTERY":
        return 0.03

    return 0.05


def update_battery(uav, time_step):

    battery_consumption_rate = get_battery_consumption_rate(uav)

    uav["battery"] = max(
        0,
        uav["battery"] - (
            battery_consumption_rate * time_step
        )
    )

    if uav["battery"] <= 0:
        uav["flight_state"] = "LOW_BATTERY"
        return False

    return True


# ============================================================
# FLIGHT STATE
# ============================================================

def update_flight_state(uav):

    if uav["flight_state"] == "CLIMBING":

        uav["altitude"] = (
            uav["altitude"]
            + uav["vertical_speed"]
        )

        if uav["altitude"] >= 180:
            uav["flight_state"] = "CRUISE"


# ============================================================
# SPEED
# ============================================================

def update_speed(uav):

    if uav["flight_state"] == "CLIMBING":

        uav["speed"] = 12.0

    elif uav["flight_state"] == "CRUISE":

        uav["speed"] = 15.0

    elif uav["flight_state"] == "LOW_BATTERY":

        uav["speed"] = 10.0


# ============================================================
# NAVIGATION
# ============================================================

def calculate_navigation(uav, waypoint):

    north_difference = (
        waypoint["latitude"]
        - uav["latitude"]
    ) * 111000

    east_difference = (
        waypoint["longitude"]
        - uav["longitude"]
    ) * 111000

    distance_to_waypoint = math.sqrt(
        north_difference ** 2
        + east_difference ** 2
    )

    target_heading_radians = math.atan2(
        east_difference,
        north_difference
    )

    target_heading = math.degrees(
        target_heading_radians
    )

    if target_heading < 0:
        target_heading = target_heading + 360

    return (
        north_difference,
        east_difference,
        distance_to_waypoint,
        target_heading
    )


# ============================================================
# HEADING CONTROL
# ============================================================

def update_heading(uav, simulation_time):

    heading_difference = (
        uav["target_heading"]
        - uav["heading"]
        + 180
    ) % 360 - 180

    if simulation_time >= 5:

        if heading_difference > 0:

            if heading_difference <= uav["turn_rate"]:

                uav["heading"] = uav["target_heading"]

            else:

                uav["heading"] = (
                    uav["heading"]
                    + uav["turn_rate"]
                ) % 360

        elif heading_difference < 0:

            if abs(heading_difference) <= uav["turn_rate"]:

                uav["heading"] = uav["target_heading"]

            else:

                uav["heading"] = (
                    uav["heading"]
                    - uav["turn_rate"]
                ) % 360

    return heading_difference


# ============================================================
# FLIGHT MODE
# ============================================================

def get_flight_mode(uav, heading_difference):

    if abs(heading_difference) > 0.1:

        return "TURNING"

    return "STRAIGHT"


# ============================================================
# MOVEMENT
# ============================================================

def calculate_movement(uav, time_step):

    heading_radians = math.radians(
        uav["heading"]
    )

    east_movement = (
        uav["speed"]
        * math.sin(heading_radians)
    )

    north_movement = (
        uav["speed"]
        * math.cos(heading_radians)
    )

    if abs(north_movement) < 1e-10:
        north_movement = 0

    if abs(east_movement) < 1e-10:
        east_movement = 0

    north_distance = (
        north_movement
        * time_step
    )

    east_distance = (
        east_movement
        * time_step
    )

    return (
        north_distance,
        east_distance
    )


# ============================================================
# POSITION UPDATE
# ============================================================

def update_position(
    uav,
    north_distance,
    east_distance
):

    uav["latitude"] = (
        uav["latitude"]
        + north_distance / 111000
    )

    uav["longitude"] = (
        uav["longitude"]
        + east_distance / 111000
    )


# ============================================================
# WAYPOINT MANAGEMENT
# ============================================================

def update_waypoint(
    current_waypoint,
    waypoints,
    distance_to_waypoint
):

    if distance_to_waypoint <= 20:

        print(
            f"Waypoint {current_waypoint + 1} Reached!"
        )

        if current_waypoint < len(waypoints) - 1:

            current_waypoint += 1

        else:

            print("Mission Complete!")

            return (
                current_waypoint,
                True
            )

    return (
        current_waypoint,
        False
    )


# ============================================================
# TELEMETRY CREATION
# ============================================================

def create_telemetry(
    uav,
    simulation_time,
    current_waypoint,
    distance_to_waypoint,
    flight_mode,
    heading_difference
):

    telemetry = {
        "simulation_time": simulation_time,
        "latitude": uav["latitude"],
        "longitude": uav["longitude"],
        "altitude": uav["altitude"],
        "speed": uav["speed"],
        "battery": uav["battery"],
        "heading": uav["heading"],
        "target_heading": uav["target_heading"],
        "heading_difference": heading_difference,
        "flight_state": uav["flight_state"],
        "flight_mode": flight_mode,
        "current_waypoint": current_waypoint,
        "distance_to_waypoint": distance_to_waypoint
    }

    return telemetry


# ============================================================
# TELEMETRY DISPLAY
# ============================================================

def display_telemetry(telemetry):

    print()
    print("=" * 50)
    print("                  UAV TELEMETRY")
    print("=" * 50)

    print(
        f"Time: {telemetry['simulation_time']:.1f} s"
    )

    print(
        f"Flight State: {telemetry['flight_state']}"
    )

    print(
        f"Flight Mode: {telemetry['flight_mode']}"
    )

    print(
        f"Current Waypoint: "
        f"{telemetry['current_waypoint'] + 1}"
    )

    print()

    print("POSITION")

    print(
        f"Latitude: "
        f"{telemetry['latitude']:.6f}"
    )

    print(
        f"Longitude: "
        f"{telemetry['longitude']:.6f}"
    )

    print(
        f"Altitude: "
        f"{telemetry['altitude']:.1f} m"
    )

    print()

    print("NAVIGATION")

    print(
        f"Distance to Waypoint: "
        f"{telemetry['distance_to_waypoint']:.1f} m"
    )

    print()

    print("FLIGHT")

    print(
        f"Speed: "
        f"{telemetry['speed']:.1f} m/s"
    )

    print(
        f"Heading: "
        f"{telemetry['heading']:.1f} degrees"
    )

    print(
        f"Target Heading: "
        f"{telemetry['target_heading']:.1f} degrees"
    )

    print(
        f"Heading Difference: "
        f"{telemetry['heading_difference']:.1f} degrees"
    )

    print(
        f"Battery: "
        f"{telemetry['battery']:.2f} %"
    )

    print("=" * 50)


# ============================================================
# TELEMETRY SUMMARY
# ============================================================

def calculate_total_distance(telemetry_history):

    total_distance = 0

    for i in range(1, len(telemetry_history)):

        previous = telemetry_history[i - 1]

        current = telemetry_history[i]

        north_difference = (
            current["latitude"]
            - previous["latitude"]
        ) * 111000

        east_difference = (
            current["longitude"]
            - previous["longitude"]
        ) * 111000

        distance = math.sqrt(
            north_difference ** 2
            + east_difference ** 2
        )

        total_distance += distance

    return total_distance


def display_telemetry_summary(
    telemetry_history,
    total_distance
):

    print()
    print("=" * 50)
    print("              TELEMETRY SUMMARY")
    print("=" * 50)

    print(
        f"Telemetry Records: "
        f"{len(telemetry_history)}"
    )

    print(
        f"Total Distance: "
        f"{total_distance:.1f} m"
    )

    if telemetry_history:

        first = telemetry_history[0]

        last = telemetry_history[-1]

        print()

        print("FIRST RECORD")

        print(
            f"Time: "
            f"{first['simulation_time']:.1f} s"
        )

        print(
            f"Latitude: "
            f"{first['latitude']}"
        )

        print(
            f"Longitude: "
            f"{first['longitude']}"
        )

        print(
            f"Battery: "
            f"{first['battery']:.2f} %"
        )

        print()

        print("LAST RECORD")

        print(
            f"Time: "
            f"{last['simulation_time']:.1f} s"
        )

        print(
            f"Latitude: "
            f"{last['latitude']}"
        )

        print(
            f"Longitude: "
            f"{last['longitude']}"
        )

        print(
            f"Battery: "
            f"{last['battery']:.2f} %"
        )

    print("=" * 50)


# ============================================================
# SAVE TELEMETRY TO CSV
# ============================================================

def save_telemetry_to_csv(
    telemetry_history,
    filename
):

    if not telemetry_history:
        return

    fieldnames = telemetry_history[0].keys()

    with open(
        filename,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            telemetry_history
        )


# ============================================================
# LOAD TELEMETRY FROM CSV
# ============================================================

def load_telemetry_from_csv(filename):

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


# ============================================================
# PARSE TELEMETRY
# ============================================================

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


# ============================================================
# MAIN SIMULATION LOOP
# ============================================================

for i in range(simulation_steps):

    simulation_time += time_step

    update_flight_state(uav)

    update_speed(uav)

    battery_ok = update_battery(
        uav,
        time_step
    )

    if not battery_ok:

        print("Battery Depleted!")

        print(
            "Flight State:",
            uav["flight_state"]
        )

        break

    waypoint = waypoints[current_waypoint]

    (
        north_difference,
        east_difference,
        distance_to_waypoint,
        target_heading
    ) = calculate_navigation(
        uav,
        waypoint
    )

    uav["target_heading"] = target_heading

    current_waypoint, mission_complete = update_waypoint(
        current_waypoint,
        waypoints,
        distance_to_waypoint
    )

    if mission_complete:

        break

    heading_difference = update_heading(
        uav,
        simulation_time
    )

    flight_mode = get_flight_mode(
        uav,
        heading_difference
    )

    north_distance, east_distance = calculate_movement(
        uav,
        time_step
    )

    update_position(
        uav,
        north_distance,
        east_distance
    )

    telemetry = create_telemetry(
        uav,
        simulation_time,
        current_waypoint,
        distance_to_waypoint,
        flight_mode,
        heading_difference
    )

    telemetry_history.append(
        telemetry
    )

    display_telemetry(
        telemetry
    )

    time.sleep(1)


# ============================================================
# END OF SIMULATION
# ============================================================

total_distance = calculate_total_distance(
    telemetry_history
)

display_telemetry_summary(
    telemetry_history,
    total_distance
)


# ============================================================
# SAVE TELEMETRY
# ============================================================

save_telemetry_to_csv(
    telemetry_history,
    "telemetry.csv"
)

print()
print("Telemetry saved to telemetry.csv")


# ============================================================
# LOAD TELEMETRY
# ============================================================

loaded_telemetry = load_telemetry_from_csv(
    "telemetry.csv"
)

print()
print("Telemetry loaded from telemetry.csv")
print(
    f"Loaded Records: {len(loaded_telemetry)}"
)