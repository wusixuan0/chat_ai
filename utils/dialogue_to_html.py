import os
import webbrowser
from markdown_it import MarkdownIt
md = MarkdownIt()

def view_dialogue_html(messages, file_name):
    dialogue_html = markdown_to_html(messages)
    chat_html = ''.join([two_column_layout_html_opening, dialogue_html, html_closing])

    folder = 'html'
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, file_name)
    with open(file_path, 'w') as f:
        f.write(chat_html)
    
    abs_path = os.path.abspath(f"{folder}/{file_name}")
    
    file_url = f'file://{abs_path}'
    webbrowser.open(file_url, new=2)

def create_html(chat_html, folder='html', file_name='chat.html'):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, file_name)
    with open(file_path, 'w') as f:
        f.write(chat_html)

def markdown_to_html(messages):
    html_strings = []
    for message in messages:
        markdown_html = md.render(message.get("content"))
        if message.get("role") == "user":
            html_strings.extend(['<div class="message user-message">', markdown_html, '</div>'])
        else:
            html_strings.extend(['<div class="message assistant-message">', markdown_html, '</div>'])
    return ''.join(html_strings)

two_column_layout_html_opening = """
<!DOCTYPE html>
<html>
<head>
  <title>Chat history</title>
  <style>
    @font-face {
      font-family: 'Tiempos Text';
      src: url('Tiempos/TestTiemposText-Regular.otf') format('opentype');
      font-weight: normal;
      font-style: normal;
    }

    @font-face {
      font-family: 'Tiempos Text';
      src: url('Tiempos/TestTiemposText-RegularItalic.otf') format('opentype');
      font-weight: normal;
      font-style: italic;
    }
    body {
      font-family: 'Tiempos Text', serif;
      line-height: 1.65rem;
      font-size: 16px;
      padding: 2rem;
      margin: 0 auto;
      color: #333333;
      -webkit-font-smoothing: antialiased;
      max-width: 1400px; /* Adjusted to accommodate two columns */
    }

    .chat-container {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
      width: 1332px; /* Double the original width */
      margin: 0 auto;
    }

    .message {
      width: 666px;
      margin-bottom: 1rem;
      padding: 2.5rem;
    }

    .user-message {
      background-color: #f2f0e8;
    }

    .assistant-message {
      background-color: #f9f9f9;
    }
    pre {
      background-color: #edf2f7;
      border: 1px solid #e2e8f0;
      padding: 1rem;
      border-radius: 5px;
      overflow-x: auto;
    }
    code {
      font-family: monospace;
      font-size: 0.9em;
      padding: 0.2em 0.4em;
      border-radius: 3px;
    }
  </style>
</head>
<body>
  <div class="chat-container">
"""

html_closing = """
  </div>
</body>
</html>
"""

linear_dialogue_html_opening = """
<!DOCTYPE html>
<html>
<head>
  <title>Chat history</title>
  <style>
    @font-face {
      font-family: 'Tiempos Text';
      src: url('Tiempos/TestTiemposText-Regular.otf') format('opentype');
      font-weight: normal;
      font-style: normal;
    }

    @font-face {
      font-family: 'Tiempos Text';
      src: url('Tiempos/TestTiemposText-RegularItalic.otf') format('opentype');
      font-weight: normal;
      font-style: italic;
    }
    body {
      width: 666px;
      font-family: 'Tiempos Text', serif;
      line-height: 1.65rem;
      font-size: 16px;
      padding: 2rem;
      margin: 0 auto;
      color: #333333;
      -webkit-font-smoothing: antialiased;
    }

    .message {
      margin-bottom: 2.5rem;
      padding-right: 1rem;
    }

    .user-message {
      background-color: #f2f0e8;
      padding: 1rem;
    }

    .assistant-message {
      background-color: #f9f9f9;
      padding: 1rem;
    }
    pre {
      background-color: #edf2f7;
      border: 1px solid #e2e8f0;
      padding: 1rem;
      border-radius: 5px;
      overflow-x: auto;
    }
    code {
      font-family: monospace;
      font-size: 0.9em;
      padding: 0.2em 0.4em;
      border-radius: 3px;
    }
  </style>
</head>
<body>
"""