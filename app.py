from flask import Flask, render_template, request, jsonify
import urllib.request
import json
import os
import ssl

app = Flask(__name__)

def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)

url = 'https://cxqa-genai-project-igysf.eastus.inference.ml.azure.com/score'
api_key = 'YOUR_API_KEY'  # Replace with your actual API key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    data = {"input": user_input}
    
    body = str.encode(json.dumps(data))
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')  # Decode the response
        return jsonify({'response': result})
    except urllib.error.HTTPError as error:
        return jsonify({'error': str(error.code) + ': ' + error.read().decode("utf8", 'ignore')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)  # For local development
