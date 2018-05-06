#!/usr/bin/env python

import requests
import http.server
import urllib.parse

def start(port, callback):
    def handler(*args):
        CallbackServer(callback, *args)
    server = http.server.HTTPServer(('', int(port)), handler)
    server.serve_forever()

class CallbackServer(http.server.BaseHTTPRequestHandler):
    def __init__(self, callback, *args):
        self.callback = callback
        http.server.BaseHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
    	print(self.path)
    	parsed_path = urllib.parse.urlparse(self.path)
    	#print(parsed_path)
    	#query = parsed_path.query
    	self.send_response(200)
    	self.end_headers()
    	result = self.callback(parsed_path.path)
    	# print(parsed_path.query)
    	message = '\r\n'.join(result)
    	self.wfile.write(message.encode('utf-8'))
    	return