from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Load the API key from the file
with open("C:/Users/shiva/OneDrive/Desktop/Gemini-App/api.txt") as f:
    key = f.read().strip()

# Configure the Google Generative AI model
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-pro')

# Start a new chat session
chat = model.start_chat(history=[])

@app.route("/query", methods=["POST"])
def query():
    """
    This endpoint handles POST requests to process the user's query.
    It will send the query to the Generative AI model and return the generated response.
    """
    data = request.get_json()
    user_input = data.get("query", "")
    
    # Check if the input is valid
    if user_input:
        # Send user input to the Generative AI model
        chat.user_input = user_input
        response = chat.send_message(user_input)
        
        # Return the AI response as JSON
        return jsonify({"response": response.text})
    else:
        return jsonify({"error": "Invalid input"}), 400

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True, port=5000)
