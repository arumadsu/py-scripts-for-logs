import json

INPUT_FILE = 'drone_manager_log.json'

armed_drones = set()
landed_drones = set()

hardware_uids = {}
last_locations = {}


with open(INPUT_FILE, 'r') as file:

    for line in file:
        if "WaitForArm.SUCCESS ARMED" in line:
            data = json.loads(line)
            drone_msg = data['src']
            clean_id = drone_msg.split('.DroneManager')[0]
            armed_drones.add(clean_id)

        elif "WaitForLand.SUCCESS landed" in line:
            data = json.loads(line)
            drone_msg = data['src']
            clean_id = drone_msg.split('.DroneManager')[0]
            landed_drones.add(clean_id)

        elif "GetDroneInfo.SUCCESS" in line:
            data = json.loads(line)
            drone_msg = data['src']
            clean_id = drone_msg.split('.DroneManager')[0]
            msg_text = data['msg']
            clean_json_string = msg_text.replace("GetDroneInfo.SUCCESS ", "")
            inner_data = json.loads(clean_json_string)
            uid = inner_data['mb']['mcu']['uid']
            hardware_uids[clean_id] = uid

        # elif '"lat":' in line and '"lon":' in line:
        #     data = json.loads(line)
        #     drone_msg = data['src']
        #     clean_id = drone_msg.split('.DroneManager')[0]
        #     telemetry = json.loads(data['msg'])
        #     lat = telemetry['lat']
        #     lon = telemetry['lon']
        #     last_locations[clean_id] = f"{lat}, {lon})"



missing_drones = armed_drones.difference(landed_drones)


for drone in missing_drones:
    drone_uid = hardware_uids.get(drone, "UID_non")
    coords = last_locations.get(drone, "No data found")
    print(f"Lost: {drone} | UID: {drone_uid}")
    # print(coords)

# print(f"Took of successfully: {len(armed_drones)} drones")
# print(f"Landed successfully: {len(landed_drones)}")

