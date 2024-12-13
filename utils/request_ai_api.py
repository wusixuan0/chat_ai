import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

# client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

client = anthropic.Anthropic(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai",
)

def get_completion(content, system, messages, model):
    messages.append({"role": "user", "content": content})
    response = get_sonnet(system, messages, model)
    messages.append({"role": "assistant", "content": response.content[0].text})
    return messages, response

def get_sonnet(system, messages, model="claude-3-5-sonnet-20241022"):
  response = client.messages.create(
      model=model,
      max_tokens=4096,
      system=system,
      messages=messages,
  )

  return response

# TODO
# Add error handling for API calls
# Consider adding typing hints
# Could add docstrings for better documentation
# May want to add rate limiting/retries
# Could validate system/message inputs
# Consider adding logging
