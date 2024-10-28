from flask import Flask, request, jsonify
import urllib.request
import json
import os
import ssl

app = Flask(__name__)

# Allow self-signed HTTPS certificates
def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)

@app.route('/score', methods=['POST'])  # Define the route for scoring
def score():
    try:
        # Get JSON data from the request body
        data = request.json
        
        # Prepare the request body for your Azure ML endpoint
        body = str.encode(json.dumps(data))
        
        # Replace this with your Azure ML endpoint URL
        url = 'https://cxqa-genai-project-fawqm.eastus.inference.ml.azure.com/score'
        
        # Fetch the API key from environment variables for security
        api_key = os.getenv('API_KEY')  # Set this in Azure App Settings for security
        
        if not api_key:
            return jsonify({'error': 'API key not provided'}), 403

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + api_key
        }

        # Create a request to the Azure ML service
        req = urllib.request.Request(url, body, headers)
        
        # Call the Azure ML scoring endpoint
        response = urllib.request.urlopen(req)
        result = response.read()
        
        # Return the result as JSON
        return jsonify(json.loads(result))

    except urllib.error.HTTPError as error:
        return jsonify({'error': str(error.code), 'message': str(error.info())}), error.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app on the specified port
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))  # Azure listens on port 8000
