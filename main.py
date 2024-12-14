import argparse
from pathlib import Path
import datetime
import json
from utils.manage_json import parse_response, load_json, make_json_readable, load_conversation, extract_messages, save_json, inspect_messages
from utils.dialogue_to_html import view_dialogue_html
from utils.request_ai_api import get_completion
from utils.similarity_search import similarity_search, load_text_file, split_documents, embed_documents, create_text_file, generate_context_prompt, docs_to_text

def handle_chat_session(content=None, system="You are a software developer.", messages=None, chat_title=None, model='grok-beta'):
    """Handle a chat session with the AI model.
    
    Args:
        content (str): The user's input content
        system (str): System prompt for the AI
        messages (list): Existing messages for conversation continuation
        chat_title (str): Title for the chat session
        model (str): AI model to use
    """
    content = content.strip()
    if not content:
        print("No prompt provided")
        return
 
    today_date = datetime.datetime.now().strftime("20%y_%m_%d")
    folder = f'current/{today_date}'
    
    # Initialize or use existing messages
    messages = messages or []
    
    # Generate chat title if not provided
    if not chat_title:
        timestamp = datetime.datetime.now().strftime("%m_%d_%Hh%Mm%Ss")
        chat_title = timestamp

    try:
        # Get AI response
        new_messages, response = get_completion(content, system, messages, model)
        parsed_response = parse_response(response)

        # Save outputs
        view_dialogue_html(new_messages, f"{chat_title}.html")
        save_json(parsed_response, f"response_{parsed_response.get('id')}.json", folder)
        save_json(new_messages, f"{chat_title}.json", folder)
        
        return new_messages, parsed_response
        
    except Exception as e:
        print(f"Error during chat session: {str(e)}")
        return None, None

def main(args):
    if args.continue_chat:
        content = """

        """
        chat_title = ""
        
        messages = load_json(f'{chat_title}.json', 'current/2024_12_13')
        handle_chat_session(content=content, messages=messages)

    if args.first_message:
        content = """

        """
        system = "You are a senior software developer."
        chat_title = "context_generator"  # enter chat title
        handle_chat_session(content=content, system=system, chat_title=chat_title)

    if args.similarity_search:
        folder = 'current'
        file_name = 'claude-chat-problem.txt'
        file_path = f"{folder}/{file_name}"

        documents = load_text_file(file_path)
        splits = split_documents(documents)

        # for pos in range(len(splits)-3):
        #     previous_context = docs_to_text(splits[pos-3:pos])
        #     current_chunk = docs_to_text([splits[133]])
        #     next_context = docs_to_text(splits[pos+1:pos+3])

        #     system = "You are generate context for a chunk within a conversation for the purposes of improving search retrieval of the chunk."
        #     context_generation_prompt = generate_context_prompt(previous_context, current_chunk, next_context)
        #     handle_chat_session(content=context_generation_prompt, system=system, chat_title=pos)

        vectorstore = embed_documents(splits)

        query = "What context preservation already works well in your system?"
        similar_docs = similarity_search(vectorstore, query)

        file_path = f"{folder}/retrieved_result.txt"
        create_text_file(similar_docs, file_path)

    # if args.make_json_readable:
    #     file = 'dec6_2pm.json'
    #     folder = 'json'
    #     make_json_readable(file, folder)

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
    parser = argparse.ArgumentParser(description='AI Chat Interface')
    parser.add_argument('--continue_chat', action='store_true')
    parser.add_argument('--first_message', action='store_true')
    parser.add_argument('--similarity_search', action='store_true')
    # parser.add_argument('--util', action='store_true')
    # parser.add_argument('--html', action='store_true')
    # parser.add_argument('--inspect_messages', action='store_true')
    # parser.add_argument('--make_json_readable', action='store_true')

    args = parser.parse_args()
    main(args)