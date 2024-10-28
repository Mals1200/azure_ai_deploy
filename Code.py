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
    data = request.json

    # Request to Azure ML scoring service
    body = str.encode(json.dumps(data))
    url = 'https://cxqa-genai-project-fawqm.eastus.inference.ml.azure.com/score'
    api_key = 'YOUR_API_KEY_HERE'  # Replace with a secure method to store your API key

    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}
    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        return jsonify(result)
    except urllib.error.HTTPError as error:
        return jsonify({'error': str(error.code), 'message': str(error.info())}), error.code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)))  # Ensure the correct port
