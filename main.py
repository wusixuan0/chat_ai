import argparse
from pathlib import Path
import datetime
import json
import pdb
from utils.manage_json import parse_response, load_json, make_json_readable, load_conversation, extract_messages, save_json, inspect_messages
from utils.dialogue_to_html import view_dialogue_html
from utils.request_ai_api import get_completion

def main(args):
    today_date = datetime.datetime.now().strftime("20%y_%m_%d")
    folder = f'current/{today_date}'
    system = "You are a software developer."

    if args.continue_chat:
        content = """

"""
        # load existing conversation
        messages = load_json('whisper.json', 'current/2024_12_13')
        ############################

        timestamp = '' or datetime.datetime.now().strftime("%m_%d_%Hh")
        model = 'grok-beta'
        new_messages, response = get_completion(content, system, messages, model)
        parsed_response = parse_response(response)


        view_dialogue_html(new_messages, f"{timestamp}.html")
        save_json(parsed_response, f"response_{parsed_response.get("id")}.json", folder)
        save_json(new_messages, f"{timestamp}.json", folder)
        print()
        print("messages:", timestamp, ".json")
        print()


    if args.first_message:
        content = """

"""
        system = "You are a software developer."
        messages = []

        # name of file
        chat_title = 'find_whisper' or datetime.datetime.now().strftime("%m_%d_%Hh")

        model = 'grok-beta'
        new_messages, response = get_completion(content, system, messages, model)
        parsed_response = parse_response(response)

        view_dialogue_html(new_messages, f"{chat_title}.html")
        save_json(parsed_response, f"response_{parsed_response.get("id")}.json", folder)
        save_json(new_messages, f"{chat_title}.json", folder)
        print()

    # if args.make_json_readable:
    #     file = 'dec6_2pm.json'
    #     folder = 'json'
    #     new_file = make_json_readable(file, folder)
    # if args.util:
    #     target_uuid = "0f6c6195-b563-4f25-b26d-9b40b6979fe5"
    #     new_file = 'readable.json'
    #     folder = 'json'
    #     chat_file_name = load_conversation(new_file, target_uuid, folder)
    #     chat_file_name = f'{target_uuid}.json'
    #     extract_messages(chat_file_name, folder)

    # if args.html:
    #     file_name = '12_08_21h13m50s.json'
    #     folder = '2024_12_08'
        
    #     messages = load_json(file_name, folder)
    #     new_file_name = Path(file_name).with_suffix('.html')
    #     view_dialogue_html(messages, new_file_name)

    # if args.inspect_messages:
    #     file_name = '0f6c6195-b563-4f25-b26d-9b40b6979fe5.json'
    #     folder = 'json'
    #     inspect_messages(file_name, folder)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Claude API')
    parser.add_argument('--continue_chat', action='store_true')
    parser.add_argument('--first_message', action='store_true')
    # parser.add_argument('--util', action='store_true')
    # parser.add_argument('--html', action='store_true')
    # parser.add_argument('--inspect_messages', action='store_true')
    # parser.add_argument('--make_json_readable', action='store_true')

    args = parser.parse_args()
    main(args)
