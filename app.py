from flask import Flask, render_template, request, jsonify
from model import get_groq_reply
import json

app = Flask(__name__)

# Store conversation history in memory (for demo purposes)
conversations = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data['message']
    conversation_id = data.get('conversation_id', 'default')
    
    # Initialize conversation if it doesn't exist
    if conversation_id not in conversations:
        conversations[conversation_id] = [
            {"role": "system", "content": "You are a helpful assistant. Keep your responses concise."}
        ]
    
    # Add user message to conversation
    conversations[conversation_id].append({"role": "user", "content": user_input})
    
    # Get assistant response
    response_stream = get_groq_reply(conversations[conversation_id])
    full_response = ""
    for chunk in response_stream:
        full_response += chunk
    
    # Add assistant response to conversation
    conversations[conversation_id].append({"role": "assistant", "content": full_response})
    
    return jsonify({
        "response": full_response,
        "conversation_id": conversation_id
    })

if __name__ == '__main__':
    app.run(debug=True)