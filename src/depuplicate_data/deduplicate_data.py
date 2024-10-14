import json
from collections import Counter


def deduplicate_texts(json_file_path, output_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    text_entries = [entry['text'] for entry in data]

    text_counts = Counter(text_entries)

    unique_texts = {text for text, count in text_counts.items() if count == 1}
    deduplicated_entries = [entry for entry in data if entry['text'] in unique_texts]

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(deduplicated_entries, output_file, ensure_ascii=False, indent=4)


input_file_path = 'data/input_creative_data/creative_writing.json'
output_file_path = 'data/input_creative_data/deduplicate_creative_writing.json'

deduplicate_texts(input_file_path, output_file_path)
