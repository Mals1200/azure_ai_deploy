from flask import Flask, request, jsonify
import urllib.request
import json
import os
import ssl

app = Flask(__name__)

def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)

@app.route('/score', methods=['POST'])
def score():
    data = request.json  # Get JSON data from the HTTP request body
    
    # Prepare the request for your Azure ML endpoint
    body = str.encode(json.dumps(data))
    url = 'https://cxqa-genai-project-fawqm.eastus.inference.ml.azure.com/score'
    api_key = 'YOUR_API_KEY_HERE'  # Secure your key using Azure App Settings

    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}
    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        return jsonify(result)  # Return the result as JSON
    except urllib.error.HTTPError as error:
        return jsonify({'error': str(error.code), 'message': str(error.info())}), error.code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)))  # Make sure to listen on port 8000
