from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# The API URL and key (replace with your actual key)
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
API_KEY = "AIzaSyAwALlImGMpNlV0yJHzu6ebNf1k9pFCYJk"  # Your actual API key
FULL_URL = f"{API_URL}?key={API_KEY}"

@app.route("/")
def home():
    # Render the index.html page on GET request
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    # Get the user query from the request body
    user_query = request.json.get("query")
    print("The query from user is as : ",user_query)
    if not user_query:
        return jsonify({"error": "Query is missing"}), 400

    # Construct the payload to send to the Generative Language API
    payload = {
        "contents": [{
            "parts": [{"text": user_query}]
        }]
    }

    # Set the headers for the request
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Send the POST request to the Gemini API
        response = requests.post(FULL_URL, json=payload, headers=headers)
        response_data = response.json()
        
        # Extract only the answer text from the API response
        answer = None
        if 'candidates' in response_data and len(response_data['candidates']) > 0:
            answer = response_data['candidates'][0].get('content', {}).get('parts', [])[0].get('text')

        # Check if an answer was found
        if answer:
            return jsonify({"answer": answer})
        else:
            return jsonify({"error": "No valid answer found"}), 500

    except Exception as e:
        # Handle unexpected errors
        print("Unexpected Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
