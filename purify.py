import json

codes_50 = ["401.9", '38.93', '428.0', '427.31', '414.01', '96.04', '96.6', '584.9', '250.00', '96.71', '272.4', '518.81', '99.04', '39.61', '599.0', '530.81', '96.72', '272.0', '285.9', '88.56', '244.9', '486', '38.91', '285.1', '36.15', '276.2', '496', '99.15', '995.92', 'V58.61', '507.0', '038.9', '88.72', '585.9', '403.90', '311', '305.1', '37.22', '412', '33.24', '39.95', '287.5', '410.71', '276.1', 'V45.81', '424.0', '45.13', 'V15.82', '511.9', '37.23']

input_json_file_path = r'D:\baseline\gpt4\111\output_full.json'
output_json_file_path = r'D:\baseline\gpt4\111\output_full_purified.json'

with open(input_json_file_path, 'r') as file:
    data = json.load(file)

purified_data = []

for record in data:
    purified_record = {}
    for key, value in record.items():
        if isinstance(value, list):
            purified_record[key] = [code for code in value if code in codes_50]
        else:
            purified_record[key] = value
    purified_data.append(purified_record)

with open(output_json_file_path, 'w') as file:
    json.dump(purified_data, file, indent=4)

print("Purified JSON file has been created successfully.")