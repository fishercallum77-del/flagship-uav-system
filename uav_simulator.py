import time
import math


# ============================================================
# SIMULATION CONFIGURATION
# ============================================================

time_step = 1.0
simulation_steps = 180
simulation_time = 0.0


# ============================================================
# UAV INITIAL STATE
# ============================================================

uav = {
    "altitude": 150,
    "speed": 15.0,
    "vertical_speed": 5,
    "turn_rate": 10,
    "battery": 87,
    "heading": 90,
    "target_heading": 0,
    "latitude": 50.2085,
    "longitude": -5.4875,
    "flight_state": "CLIMBING"
}


# ============================================================
# NAVIGATION / WAYPOINTS
# ============================================================

waypoints = [
    {
        "latitude": 50.2100,
        "longitude": -5.4800
    },
    {
        "latitude": 50.2115,
        "longitude": -5.4750
    },
    {
        "latitude": 50.2090,
        "longitude": -5.4700
    }
]

current_waypoint = 0


# ============================================================
# FUNCTIONS
# ============================================================

def update_battery(uav):

    uav["battery"] = max(
        0,
        uav["battery"] - 1
    )

    if uav["battery"] <= 0:

        uav["flight_state"] = "LOW_BATTERY"

        return False

    return True


def update_flight_state(uav):

    if uav["flight_state"] == "CLIMBING":

        uav["altitude"] = (
            uav["altitude"]
            + uav["vertical_speed"]
        )

    if uav["altitude"] >= 180:

        uav["flight_state"] = "CRUISE"


def calculate_navigation(uav, waypoint):

    north_difference = (
        waypoint["latitude"] - uav["latitude"]
    ) * 111000

    east_difference = (
        waypoint["longitude"] - uav["longitude"]
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

    return north_distance, east_distance


def update_position(uav, north_distance, east_distance):

    uav["latitude"] = (
        uav["latitude"]
        + (north_distance / 111000)
    )

    uav["longitude"] = (
        uav["longitude"]
        + (east_distance / 111000)
    )


def update_waypoint(
    current_waypoint,
    waypoints,
    distance_to_waypoint
):

    if distance_to_waypoint <= 20:

        print("Waypoint Reached!")

        if current_waypoint < len(waypoints) - 1:

            current_waypoint = current_waypoint + 1

            return current_waypoint, False

        else:

            print("Mission Complete!")

            return current_waypoint, True

    return current_waypoint, False


# ============================================================
# MAIN SIMULATION LOOP
# ============================================================

for i in range(simulation_steps):

    # --------------------------------------------------------
    # SIMULATION TIME
    # --------------------------------------------------------

    simulation_time = simulation_time + time_step


    # --------------------------------------------------------
    # ALTITUDE / FLIGHT STATE
    # --------------------------------------------------------

    update_flight_state(uav)


    # --------------------------------------------------------
    # BATTERY
    # --------------------------------------------------------

    battery_ok = update_battery(uav)

    if not battery_ok:

        print("Battery Depleted!")
        print("Flight State:", uav["flight_state"])

        break


    # --------------------------------------------------------
    # CURRENT WAYPOINT
    # --------------------------------------------------------

    waypoint = waypoints[current_waypoint]


    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # WAYPOINT MANAGEMENT
    # --------------------------------------------------------

    current_waypoint, mission_complete = update_waypoint(
        current_waypoint,
        waypoints,
        distance_to_waypoint
    )

    if mission_complete:

        break


    # --------------------------------------------------------
    # HEADING / FLIGHT CONTROL
    # --------------------------------------------------------

    heading_difference = update_heading(
        uav,
        simulation_time
    )


    # --------------------------------------------------------
    # MOVEMENT CALCULATION
    # --------------------------------------------------------

    north_distance, east_distance = calculate_movement(
        uav,
        time_step
    )


    # --------------------------------------------------------
    # POSITION UPDATE
    # --------------------------------------------------------

    update_position(
        uav,
        north_distance,
        east_distance
    )


    # --------------------------------------------------------
    # TELEMETRY / OUTPUT
    # --------------------------------------------------------

    print("--------------------")
    print("Simulation Time:", simulation_time)
    print("Current Waypoint:", current_waypoint)
    print("Altitude:", uav["altitude"])
    print("Speed:", uav["speed"])
    print("Battery:", uav["battery"])
    print("Heading:", uav["heading"])
    print("Target Heading:", uav["target_heading"])
    print("Heading Difference:", heading_difference)
    print("Latitude:", uav["latitude"])
    print("Longitude:", uav["longitude"])
    print("Flight State:", uav["flight_state"])
    print("North Distance:", north_distance)
    print("East Distance:", east_distance)
    print("North to Waypoint:", north_difference)
    print("East to Waypoint:", east_difference)
    print("Distance to Waypoint:", distance_to_waypoint)


    # --------------------------------------------------------
    # SIMULATION DELAY
    # --------------------------------------------------------

    time.sleep(1)