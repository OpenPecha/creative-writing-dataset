import os
import json


def load_json(file_path):
    """Loads the JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as infile:
        return json.load(infile)


def save_json(data, output_file_path):
    """Saves the data to a JSON file."""
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)


def sample_json_files(input_dir, output_dir, sample_size=10):
    """Takes the first `sample_size` entries from each JSON file in `input_dir` and saves them in `output_dir`."""

    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(input_dir, file_name)

            data = load_json(file_path)
            sample_data = data[:sample_size]

            sample_file_name = file_name.replace('.json', '_sample.json')
            sample_file_path = os.path.join(output_dir, sample_file_name)

            save_json(sample_data, sample_file_path)

            print(f"Sampled {len(sample_data)} entries from {file_name} and saved to {sample_file_name}.")


input_dir = 'data/creative_dataset_output_json'
output_dir = 'data/output_sample_json_files'

sample_json_files(input_dir, output_dir, sample_size=10)
