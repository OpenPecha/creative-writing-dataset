import json
from collections import Counter

def check_duplicate_texts(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print("Loaded Data:", json.dumps(data, ensure_ascii=False, indent=4))
    
    text_entries = [entry['text'] for entry in data]
    text_counts = Counter(text_entries)
    
    print("Text Counts:", dict(text_counts))
    
    duplicates = {text: count for text, count in text_counts.items() if count > 1}
    
    if not duplicates:
        print("No duplicate texts found.")
    else:
        for text, count in duplicates.items():
            print(f"text: {text}\nCount: {count}\n")

check_duplicate_texts('data/input_creative_data/creative_writing.json')
