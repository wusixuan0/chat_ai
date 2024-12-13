import pathlib
import json
import os

def parse_response(response):
    raw_response = response.to_json()
    parsed_response = json.loads(raw_response)
    return parsed_response
    
def load_json(file_name, folder):
    PATH = pathlib.Path().resolve()
    file_path = PATH / folder / file_name
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data
   
def save_json(data, file_name, folder="json", indent=2):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, file_name)
    # PATH = pathlib.Path().resolve()
    # file_path = PATH / folder / file_name
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=indent)
    print(f"Saved {file_name} to {folder}")

def make_json_readable(file_name, folder, indent=4):
    data = load_json(file_name, folder)
    new_file_name = file_name.replace(".json", "_readable.json")
    save_json(data, new_file_name, folder, indent)
    return new_file_name

def load_conversation(file, target_uuid, folder='json'):
    PATH = pathlib.Path().resolve()
    file_path = PATH / folder / file
    with open(file_path, 'r') as f:
        data = json.load(f)

    matching_item = _find_item_by_uuid(data, target_uuid)

    if matching_item:
        file_name=f'{target_uuid}.json'
        new_file_path = PATH / folder / file_name
        with open(new_file_path, 'w') as f:
            json.dump(matching_item, f, indent=4)
        print(f"Saved {file_name} to {folder}")
        return file_name

def extract_messages(file_name, folder):
    PATH = pathlib.Path().resolve()
    file_path = PATH / folder / file_name
    with open(file_path, 'r') as f:
        data = json.load(f)
        
    messages = []
    for message in data.get("chat_messages"):
        messages.append({
            "content": message.get("text"),
            "role": "assistant" if message.get("sender") == "assistant" else "user"
        })
    new_file_path = PATH / folder / f'messages_{file_name}'
    with open(new_file_path, 'w') as f:
        json.dump(messages, f, indent=4)

def inspect_messages(file_name, folder):
    PATH = pathlib.Path().resolve()
    file_path = PATH / folder / file_name
    with open(file_path, 'r') as f:
        data = json.load(f)
        
    chat_messages = data.get("chat_messages")
    print(len(chat_messages))

def _find_item_by_uuid(data, target_uuid):
    for item in data:
        if item.get("uuid") == target_uuid:
            return item
    return None