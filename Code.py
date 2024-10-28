import http.server
import socketserver
import urllib.request
import json
import os
import ssl
from urllib.parse import parse_qs

PORT = 8000

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # Endpoint logic for processing the request
        if self.path == '/ask':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)  # Get the data sent in the request

            # Process the incoming JSON data
            data = json.loads(post_data.decode('utf-8'))
            user_input = data.get('question')
            
            if not user_input:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "Question not provided"}')
                return
            
            # Prepare to call the Azure ML endpoint
            body = str.encode(json.dumps({"input": user_input}))
            url = 'https://cxqa-genai-project-fawqm.eastus.inference.ml.azure.com/score'
            api_key = os.getenv('API_KEY')  # Set API key in Azure App Settings

            if not api_key:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b'{"error": "API key not provided"}')
                return
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }

            req = urllib.request.Request(url, body, headers)

            try:
                response = urllib.request.urlopen(req)
                result = response.read()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(result)
            except urllib.error.HTTPError as error:
                self.send_response(error.code)
                self.end_headers()
                self.wfile.write(f'{{"error": {error.code}, "message": "{error.reason}"}}'.encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'{{"error": "{str(e)}"}}'.encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "Not Found"}')

# Start the server
with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
