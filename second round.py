from openai import OpenAI
import os
import json
import threading
from queue import Queue

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<Enter your api key here>")) 

# Path to the folder containing output JSON files
folder_path = r'data/output'

# Iterate through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        
        # Open the JSON file
        with open(file_path, 'r') as json_file:
            json_data = json.load(json_file)
            
            # Extract data from JSON
            hadm_id = json_data['hadm_id']
            sections = json_data['sections']
            
            # Define messages for completion generation
            #{"role": "system", "content": "The following is the icd code predicted by different medical texts for the same patient. Please get the most likely set of icd codes from them according to your understanding of the importance of different texts and logical inference."},
            messages = [
                {"role": "system", "content": "The following is the icd code predicted by different medical texts for the same patient, but there may be inaccurate codes. You need to get the final accurate code as an auditor, according to your understanding of the importance of different texts and logical inference. The number of codes in the final result is usually between several and 15. "},
                {"role": "system", "content": "For example, i. codes that are predicted in multiple sections are usually correct. When there are some codes that are very similar among the predicted results of multiple sections, you can think that the overlapping part is correct, and then you can make choices based on other text summaries and speculated reasons. iii. You can think about the retention and deletion of certain codes based on the text summary and inferred evidence. iv. You need to think about which sections are more important according to the contents of different sections, and the code inferred from these texts may have a higher degree of confidence"},
                {"role": "system", "content": "Use the following format for output: [ \"xxx.xx\", \"xxx.xx\", \"xxx.xx\"] "},
                {"role": "user", "content": f"Please note that for the final answer, you only need to return the predicted code in the format without any additional text or explanation. Generate 'final_code' for this case: {sections}"},
                {"role": "user", "content": "Use the following format for output: [ \"xxx.xx\", \"xxx.xx\", \"xxx.xx\"] "}
            ]
            
            # Generate completion from OpenAI's chat model
            completion = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=messages
            )

            generated_content = completion.choices[0].message.content
            
            # Update the JSON data with the generated content
            json_data['sections']['final_code'] = generated_content

            # Write the updated JSON data back to the file
            with open(file_path, 'w') as updated_json_file:
                json.dump(json_data, updated_json_file, indent=4)
