import json


def extract_unique_strings_in_tags(input_file, output_file):
    unique_strings = set()

    with open(input_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            for entry in data:
                text = entry.get("text", "").strip()
                if text:
                    tags = entry.get("tags", [])
                    unique_strings.update(tags)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {input_file}")

    output_data = list(unique_strings)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"unique strings in tags: {len(unique_strings)}")


input_json_file = 'data/creative_dataset_output_json/unclassified.json'
output_json_file = 'data/all_tags/all_unique_unclassified_strings.json'
extract_unique_strings_in_tags(input_json_file, output_json_file)
