import time
from PIL import ImageGrab
import pytesseract
import ollama
from flask import Flask, jsonify
import threading
import logging
from functools import lru_cache
import re
import html

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Ollama Client Setup
ollama_client = ollama.Client()

latest_comment = "Waiting for initial comment..."

def preprocess_text(text):
    # Remove extra whitespace while preserving single line breaks
    text = re.sub(r'[^\S\n]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Limit to 1000 characters to allow for more context
    return text[:1000] + ('...' if len(text) > 1000 else '')

@lru_cache(maxsize=100)
def generate_comment(extracted_text):
    global latest_comment
    preprocessed_text = preprocess_text(extracted_text)
    prompt = f"""Provide a clear summary of the key points in this text. Format your response as a numbered list with 3-5 concise points. Preserve any important line breaks or paragraph structures:

```
{preprocessed_text}
```

Example format:
1. First key point
   (Additional details if necessary)

2. Second key point

3. Third key point
   - Subpoint if needed
   - Another subpoint"""

    try:
        response = ollama_client.generate(model="llama3.2:latest", prompt=prompt)
        latest_comment = response['response'].strip()
        logging.info("Generated new comment")
    except Exception as e:
        latest_comment = f"Error generating comment: {str(e)}"
        logging.error(f"Error generating comment: {str(e)}")

def capture_and_comment():
    while True:
        try:
            screenshot = ImageGrab.grab()
            extracted_text = pytesseract.image_to_string(screenshot)
            if extracted_text.strip():  # Only generate comment if there's text
                generate_comment(extracted_text)
            else:
                logging.info("No text detected in screenshot")
        except Exception as e:
            logging.error(f"Error capturing or processing screenshot: {str(e)}")
        time.sleep(10)

@app.route('/get_comment')
def get_comment():
    # Escape HTML to prevent XSS, then replace newlines with <br> tags
    formatted_comment = html.escape(latest_comment).replace('\n', '<br>')
    return jsonify({"comment": formatted_comment})

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Screen Commentator Tabajara</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; max-width: 800px; margin: 0 auto; }
            h1 { color: #333; }
            #comment { background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin-top: 20px; white-space: pre-wrap; }
            #copyButton { margin-top: 10px; padding: 5px 10px; cursor: pointer; }
        </style>
    </head>
    <body>
        <h1>Screen Commentator Tabajara</h1>
        <div id="comment">Waiting for comment...</div>
        <button id="copyButton">Copy to Clipboard</button>
        <script>
            function updateComment() {
                fetch('/get_comment')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('comment').innerHTML = data.comment;
                    })
                    .catch(error => console.error('Error fetching comment:', error));
            }

            document.getElementById('copyButton').addEventListener('click', function() {
                const commentText = document.getElementById('comment').innerText;
                navigator.clipboard.writeText(commentText).then(function() {
                    alert('Comment copied to clipboard!');
                }, function(err) {
                    console.error('Could not copy text: ', err);
                });
            });

            setInterval(updateComment, 5000);
            updateComment(); // Initial update
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    comment_thread = threading.Thread(target=capture_and_comment, daemon=True)
    comment_thread.start()
    app.run(debug=False, use_reloader=False, host='0.0.0.0', port=5000)