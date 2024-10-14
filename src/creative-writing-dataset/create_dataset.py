import json
import os

def load_json(file_path):

    with open(file_path, 'r', encoding='utf-8') as infile:
        return json.load(infile)

def filter_data_by_keyword(data, keyword):

    return [entry for entry in data if keyword in entry['tags']]

def filter_unclassified_data(data, classified_keywords):
  
    return [entry for entry in data if not any(keyword in entry['tags'] for keyword in classified_keywords)]

def save_json(data, output_file_path):
  
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

def process_json(input_json_path, keywords, output_dir):

    os.makedirs(output_dir, exist_ok=True)
    data = load_json(input_json_path)

    classified_entries = []

    for keyword in keywords:
        filtered_data = filter_data_by_keyword(data, keyword)
        if filtered_data:
            output_file_path = os.path.join(output_dir, f"{keyword}.json")
            save_json(filtered_data, output_file_path)
            classified_entries.extend(filtered_data)

    unclassified_data = filter_unclassified_data(data, keywords)
    if unclassified_data:
        unclassified_file_path = os.path.join(output_dir, 'unclassified.json')
        save_json(unclassified_data, unclassified_file_path)

def main(input_json_path, output_dir):
    keywords = [
        "ཡིག་སྒྲེལ་",
        "ངོས་སྦྱོར་",
        "གསལ་བསྒྲགས་",
        "རྩོམ་ཡིག",
        "གློག་དེབ།",
        "མགུར་གླུ།",
        "གསར་འགྱུར།",
        "སྙན་ངག"
    ]
    process_json(input_json_path, keywords, output_dir)

if __name__ == "__main__":
    input_json_path = 'data/input_creative_data/deduplicate_creative_writing.json' 
    output_dir = 'data/creative_dataset_output_json'   
    main(input_json_path, output_dir)
