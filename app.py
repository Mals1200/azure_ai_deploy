from flask import Flask, render_template, request
import urllib.request
import json
import os
import ssl

app = Flask(__name__)

def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['textbox']
        data = {"input": user_input}  # Structure your input based on your service's requirements.

        body = str.encode(json.dumps(data))
        url = 'https://cxqa-genai-project-igysf.eastus.inference.ml.azure.com/score'
        api_key = 'YOUR_API_KEY'  # Replace with your API key

        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key}
        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)
            result = response.read()
            return render_template('index.html', result=result.decode('utf-8'))  # Decode result for display
        except urllib.error.HTTPError as error:
            return f"Error: {str(error.code)} - {error.read().decode('utf-8', 'ignore')}"
    
    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)
