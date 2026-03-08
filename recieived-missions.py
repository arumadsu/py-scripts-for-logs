import json

INPUT_FILE = 'drone_manager_log.json'
unique_drones = set()

with open(INPUT_FILE, 'r') as file:
    lines_in_log = file.readlines()

for line in lines_in_log:
    if "WaitForDanceMission.SUCCESS" in line:
        data = json.loads(line)
        drone_id = data['src']
        print(data)
        unique_drones.add(drone_id)

print(len(unique_drones))
