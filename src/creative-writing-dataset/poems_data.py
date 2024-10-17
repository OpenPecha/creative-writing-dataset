import json
import re

def count_syllables(text):
    clean_text = re.sub(r'[།༎༏༐༑༔]+', '', text)
    syllables = clean_text.split('་')
    syllables = [syll for syll in syllables if syll]
    return len(syllables) if syllables else None


def process_text(text):
    lines = re.split(r'\s+', text.strip())

    total_syllable_count = 0
    syllable_counts = []
    
    for line in lines:
        count = count_syllables(line)
        if count is not None:
            syllable_counts.append(count)
            total_syllable_count += count

    if len(syllable_counts) > 0:
        most_common_count = max(set(syllable_counts), key=syllable_counts.count)
        consistency = sum(1 for count in syllable_counts if count == most_common_count) / len(syllable_counts)
    else:
        most_common_count = 0
        consistency = 0

    is_consistent = consistency >= 0.8
    return {
        "syllable_count": total_syllable_count,
        "line_count": len(syllable_counts),
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
            "syllable_count": text_info["syllable_count"],
            "line_count": text_info["line_count"],
            "structured": text_info["structured"]
        }
        output_data.append(output_entry)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(output_data, outfile, ensure_ascii=False, indent=4)


input_file = 'data/creative_dataset_output_json/སྙན་ངག.json'
output_file = 'data/creative_dataset_output_json/སྙན་ངག_structured.json'
process_json(input_file, output_file)
