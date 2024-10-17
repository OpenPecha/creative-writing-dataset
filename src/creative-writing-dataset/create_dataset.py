import json
import os
import re


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as infile:
        return json.load(infile)


def remove_empty_text_entries(data):
    return [entry for entry in data if entry.get('text', '').strip()]


def filter_data_by_keyword(data, keyword, additional_keywords=None, priority_keyword=None):
    """
    Filters data by keyword. If priority_keyword is provided, it ensures that
    entries containing the priority_keyword are classified under it.
    Supports additional keywords for matching.
    """
    keywords_to_match = [keyword] + (additional_keywords or [])

    def tag_contains_keywords(tags, kw_list):
        return any(kw in tag for kw in kw_list for tag in tags)

    if priority_keyword:
        return [
            entry for entry in data if tag_contains_keywords(entry['tags'], [priority_keyword]) or
            (tag_contains_keywords(entry['tags'], keywords_to_match)
             and not tag_contains_keywords(entry['tags'], [priority_keyword]))
        ]
    return [entry for entry in data if tag_contains_keywords(entry['tags'], keywords_to_match)]


def filter_unclassified_data(data, classified_entries):
    classified_content = {json.dumps(entry, sort_keys=True) for entry in classified_entries}
    return [entry for entry in data if json.dumps(entry, sort_keys=True) not in classified_content]


def save_json(data, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)


def count_syllables(text):
    clean_text = re.sub(r'[།༎༏༐༑༔]+', '', text)
    syllables = clean_text.split('་')
    syllables = [syll for syll in syllables if syll]
    return len(syllables) if syllables else None


def process_poems(text):
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
        "structured": is_consistent,
        "average_syllables_per_line": most_common_count
    }


def process_json(input_json_path, keywords, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    data = load_json(input_json_path)

    data = remove_empty_text_entries(data)
    classified_entries = []

    keyword_config = {
        "རྩོམ": {
            "priority_keyword": "སྙན་ངག",
            "additional_keywords": ["opinions", "Opinions", "བསམ་ཚུལ", "གཏམ་དཔེ", "སྣ་ཚོགས།", "ངོ་སྤྲོད།"]
        },
        "གསར་འགྱུར།": {
            "additional_keywords": ["news", "News", "བོད་ནང་", "གོང་ས་མཆོག", "རྒྱ་ནག", "བཙན་བྱོལ།", "འཕྲིན་གསར", "རྒྱ་དཀར་ནག",  "འཛམ་གླིང་།", "སྤྱི་ཚོགས།", "བརྒྱུད་ལམ་གཞན་གྱི་གསར་གནས།", "ཨ་རི།"]
        },
        "མགུར་གླུ།": {
            "additional_keywords": ["གླུ་གཞས།"]
        },
        "ཡིག་སྒྲེལ་": {
            "additional_keywords": ["ངོས་སྦྱོར་", "འཕྲིན་ཡིག"]
        },
        "བརྩམས་སྒྲུང": {
            "additional_keywords": ["མཚར་གཏམ།"]
        },
    }

    for keyword in keywords:
        config = keyword_config.get(keyword, {})
        filtered_data = filter_data_by_keyword(
            data,
            keyword,
            additional_keywords=config.get("additional_keywords"),
            priority_keyword=config.get("priority_keyword")
        )

        if filtered_data:
            if keyword == "སྙན་ངག":
                structured_output_file = os.path.join(output_dir, f"{keyword}.json")
                process_syllable_structure(filtered_data, structured_output_file)
            else:

                output_file_path = os.path.join(output_dir, f"{keyword}.json")
                save_json(filtered_data, output_file_path)

            classified_entries.extend(filtered_data)

    # unclassified entries
    unclassified_data = filter_unclassified_data(data, classified_entries)
    if unclassified_data:
        unclassified_file_path = os.path.join(output_dir, 'unclassified.json')
        save_json(unclassified_data, unclassified_file_path)


def process_syllable_structure(data, output_file):
    output_data = []
    for entry in data:
        tags = entry.get("tags", [])
        text = entry.get("text", "")
        text_info = process_poems(text)

        output_entry = {
            "tags": tags,
            "text": text,
            "syllable_count": text_info["syllable_count"],
            "line_count": text_info["line_count"],
            "structured": text_info["structured"],
            "average_syllable": text_info["average_syllables_per_line"]
        }
        output_data.append(output_entry)

    save_json(output_data, output_file)


def main(input_json_path, output_dir):
    keywords = [
        "ཡིག་སྒྲེལ་",
        "གསལ་བསྒྲགས",
        "རྩོམ",
        "མགུར་གླུ།",
        "གསར་འགྱུར།",
        "སྙན་ངག",
        "བརྩམས་སྒྲུང",
        "དྲ་ཐོག་གི་གཏམ་རྒྱུན།"
    ]
    process_json(input_json_path, keywords, output_dir)


if __name__ == "__main__":
    input_json_path = 'data/input_creative_data/creative_writing.json'
    output_dir = 'data/creative_dataset_output_json'
    main(input_json_path, output_dir)
