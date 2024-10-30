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

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.json['input']
    data = {'input': input_data}
    body = str.encode(json.dumps(data))
    
    url = 'https://cxqa-genai-project-igysf.eastus.inference.ml.azure.com/score'
    api_key = os.getenv('AZURE_API_KEY')  # Get API key from environment variables

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        return jsonify(result.decode('utf-8')), 200
    except urllib.error.HTTPError as error:
        return jsonify(error=str(error.code), info=error.read().decode("utf8", 'ignore')), error.code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))  # PORT environment variable used by Azure
