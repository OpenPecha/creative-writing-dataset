import json
import re


def count_syllables(text):
    tibetan_syllable_pattern = re.compile(r'[ཀ-ཿ]+')
    syllables = tibetan_syllable_pattern.findall(text)
    return len(syllables)


def process_text(text):
 
    lines = re.split(r'\s+', text.strip()) 
    
    syllable_counts = [count_syllables(line) for line in lines]

    if len(syllable_counts) > 0:
        most_common_count = max(set(syllable_counts), key=syllable_counts.count)
        consistency = sum(1 for count in syllable_counts if count == most_common_count) / len(syllable_counts)
    else:
        most_common_count = 0
        consistency = 0

    is_consistent = consistency >= 0.8
    return {
        "syllable_count": syllable_counts,
        "line_count": len(lines),
        "structured": is_consistent
    }


def process_json(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    output_data = []
    for entry in data:
        tags = entry.get("tags", [])
        text = entry.get("text", "")

        text_info = process_text(text)

        output_entry = {
            "tags": tags,
            "text": text,
            "syllable": text_info["syllable_count"],
            "line": text_info["line_count"],
            "structured": text_info["structured"]
        }
        output_data.append(output_entry)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(output_data, outfile, ensure_ascii=False, indent=4)

input_file = 'data/creative_dataset_output_json/སྙན་ངག.json'
output_file = 'data/creative_dataset_output_json/སྙན་ངག_structured_output.json'
process_json(input_file, output_file)
