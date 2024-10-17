import json
from datasets import Dataset
from huggingface_hub import HfApi, HfFolder

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_dataset(data):
    return Dataset.from_list(data)

def save_dataset_locally(dataset, save_path, format='arrow'):
    if format == 'arrow':
        dataset.save_to_disk(save_path)
    elif format == 'parquet':
        dataset.to_parquet(save_path)
    elif format == 'csv':
        dataset.to_csv(save_path)
    else:
        raise ValueError(f"Unsupported format: {format}")
    print(f"Dataset saved locally at '{save_path}' in {format} format.")

def upload_dataset(dataset, repo_id):
    dataset.push_to_hub(repo_id)
    print(f"Dataset uploaded successfully to '{repo_id}'.")

def main(save_to_disk=False, disk_format='arrow'):
    json_file_path = 'data/creative_dataset_output_json/སྙན་ངག_structured.json'
    dataset_name = 'tibetan-poems'  
    repo_id = f'tenkal/{dataset_name}' 
    data = load_json(json_file_path)

    dataset = create_dataset(data)


    if save_to_disk:
        save_path = f'data/hf_dataset/{dataset_name}-local'
        save_dataset_locally(dataset, save_path, disk_format)

    upload_dataset(dataset, repo_id)

if __name__ == '__main__':

    main(save_to_disk=True, disk_format='parquet')
