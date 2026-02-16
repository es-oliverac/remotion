#!/usr/bin/env python3
"""Simple HTTP server that serves index.html for all routes (SPA support)"""
import http.server
import socketserver
import os
from urllib.parse import unquote

class SPAHandler(http.server.SimpleHTTPRequestHandler):
    """Handler that serves index.html for non-existent routes (SPA routing)"""

    def do_GET(self):
        # Parse the path
        path = unquote(self.path.split('?')[0])

        # Remove leading slash
        if path.startswith('/'):
            path = path[1:]

        # If path is empty or doesn't exist, serve index.html
        if not path or path == '':
            path = 'index.html'
        elif not os.path.exists(path):
            # Check if it's a static file (has extension)
            if '.' in path.split('/')[-1]:
                # It's a file that doesn't exist
                super().do_GET()
                return
            else:
                # It's a route, serve index.html
                path = 'index.html'

        # Serve the file
        if os.path.exists(path):
            with open(path, 'rb') as f:
                self.send_response(200)
                # Set correct content type
                if path.endswith('.html'):
                    self.send_header('Content-type', 'text/html')
                elif path.endswith('.js'):
                    self.send_header('Content-type', 'application/javascript')
                elif path.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                elif path.endswith('.json'):
                    self.send_header('Content-type', 'application/json')
                elif path.endswith('.wasm'):
                    self.send_header('Content-type', 'application/wasm')
                elif path.endswith('.ico'):
                    self.send_header('Content-type', 'image/x-icon')
                else:
                    self.send_header('Content-type', 'application/octet-stream')
                self.end_headers()
                self.wfile.write(f.read())
        else:
            super().do_GET()

    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

PORT = 3000

with socketserver.TCPServer(("", PORT), SPAHandler) as httpd:
    print(f"Serving SPA at http://localhost:{PORT}", flush=True)
    httpd.serve_forever()
