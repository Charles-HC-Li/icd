from openai import OpenAI  # Import OpenAI library
import os
import json
import threading
from queue import Queue
import random 

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<Enter your api key here>")) 

def call_gpt_api(section_name, section_text):
    try:
        # List of 50 common ICD-9 codes
        codes_50 = ["401.9", "38.93", "428.0", "427.31", "414.01", "96.04", "96.6", "584.9", "250.00", "96.71", "272.4", "518.81", "99.04", "39.61", "599.0", "530.81", "96.72", "272.0", "285.9", "88.56", "244.9", "486", "38.91", "285.1", "36.15", "276.2", "496", "99.15", "995.92", "V58.61", "507.0", "038.9", "88.72", "585.9", "403.90", "311", "305.1", "37.22", "412", "33.24", "39.95", "287.5", "410.71", "276.1", "V45.81", "424.0", "45.13", "V15.82", "511.9", "37.23"]
        
        # Shuffle the list of codes
        random.shuffle(codes_50)

        # Generate completion from OpenAI's chat model
        completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "You are an ICD-9 coder that will predict ICD-9 codes for the input medical text, and the final result will only contain the predicted codes themselves, excluding irrelevant words and explanations"},
                {"role": "system", "content": f"You only need to consider the following 50 common icd-9 codes from codes_50: {codes_50}"},
                {"role": "system", "content": "The final output consists of [code], [summary of this medical record], [direct evidence of predicted code], each surrounded by [] and delimited by @@@. Use the following format for output: [ \"xxx.xx\", \"xxx.xx\", \"xxx.xx\"]@@@[summary of this medical record]@@@[direct evidence of predicted code] "},
                {"role": "user", "content": f"Please predict ICD-9 code for {section_name}: {section_text}"},
                {"role": "user", "content": "For the internal order of the final results, you need to rank them according to how confident you are with the code. Finish with a brief summary of what the medical notes are saying and the short and direct evidence that you predict this code."},
                {"role": "user", "content": "Use the following format for output: [ \"xxx.xx\", \"xxx.xx\", \"xxx.xx\"]@@@[summary of this medical record]@@@[direct evidence of predicted code] "}
            ]
        )
        return completion.choices[0].message.content  # Return the predicted result
    except Exception as e:
        return "Error: " + str(e)

def process_case(case, queue):
    hadm_id = case['hadm_id']
    sections = case['sections']
    result = {"hadm_id": hadm_id, "sections": {}}

    # Process each section of the case
    for section, text in sections.items():
        gpt_response = call_gpt_api(section, text)
        result["sections"][section] = gpt_response

    queue.put(result)

def save_to_json(data, filename):
    directory = "data/output"
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f"{directory}/{filename}.json", 'w') as file:
        json.dump(data, file, indent=4)  # Save data to JSON file with indentation

def main():
    # Load dataset from JSON file
    with open('data/dataset.json', 'r') as file:
        data = json.load(file)

    queue = Queue()  # Create a queue for storing processed results
    threads = []

    # Process each case in a separate thread
    for case in data[0:1]:
        thread = threading.Thread(target=process_case, args=(case, queue))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Save processed results to JSON files
    while not queue.empty():
        case_result = queue.get()
        save_to_json(case_result, case_result['hadm_id'])

if __name__ == "__main__":
    main()
