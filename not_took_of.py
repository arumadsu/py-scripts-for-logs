import json

INPUT_FILE = 'drone_manager_log.json'
OUTPUT_FILE = 'failed_drones.txt'

hardware_uids = {}
mission_drones = {}
armed_drones = set()


with open(INPUT_FILE, 'r') as file:

    for line in file:
        if "WaitForDanceMission.SUCCESS" in line:
            data = json.loads(line)
            drone_id = data['src']
            clean_id = drone_id.split('.DroneManager')[0]
            mission_drones[clean_id] = line

        elif "WaitForArm.SUCCESS ARMED" in line:
            data = json.loads(line)
            drone_id = data['src']
            clean_id = drone_id.split('.DroneManager')[0]
            armed_drones.add(clean_id)

        elif "GetDroneInfo.SUCCESS" in line:
            data = json.loads(line)
            drone_id = data['src']
            clean_id = drone_id.split('.DroneManager')[0]
            msg_text = data['msg']
            clean_json_string = msg_text.replace("GetDroneInfo.SUCCESS ", "")
            inner_data = json.loads(clean_json_string)
            uid = inner_data['mb']['mcu']['uid']
            hardware_uids[clean_id] = uid

    for drone_id, line in mission_drones.items():
        if drone_id not in armed_drones:
            drone_uid = hardware_uids.get(drone_id, "UID_Non")
            print(f"ID: {drone_id} | UID: {drone_uid}")

print("Получили миссии", len(mission_drones))
print("Взлетели", len(armed_drones))
