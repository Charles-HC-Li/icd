import os
import json
import re

# Define input folder and dataset paths
data_folder = r'data/output'  
dataset_path = r'data/dataset.json' 

# Initialize list to store new data
new_data = []

# Load dataset
with open(dataset_path, 'r', encoding='utf-8') as dataset_file:
    dataset100 = json.load(dataset_file)

# Iterate through each file in the input folder
for filename in os.listdir(data_folder):
    if filename.endswith('.json'):
        input_file_path = os.path.join(data_folder, filename)
        
        # Load data from input JSON file
        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            input_data = json.load(input_file)
        
        # Extract relevant information from the input data
        hadm_id = input_data.get("hadm_id", "")
        sections = input_data.get("sections", {})
        final_code = sections.get("final_code", "") 
        
        # Perform regex replacement on final_code
        final_code_normalized = re.sub(r'\[', '[ ', final_code)
        final_code_normalized = re.sub(r'\]', ' ]', final_code_normalized)
        
        # Find corresponding labels from dataset_100.json based on hadm_id
        labels_50 = []
        for entry in dataset100:
            if entry.get("hadm_id") == hadm_id:
                labels_50 = entry.get("LABELS_50", [])
                break
        
        # Create a new entry with relevant information
        new_entry = {
            "hadm_id": hadm_id,
            "final_code": final_code_normalized,
            "LABELS_50": labels_50
        }
        
        # Append the new entry to the list
        new_data.append(new_entry)

# Define output file path
output_file_path = os.path.join(data_folder, 'output.json')

# Write the new data to the output JSON file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(new_data, output_file, ensure_ascii=False, indent=4)

# Print message confirming the creation of the new JSON file
print(f'Created new JSON file: {output_file_path}')
