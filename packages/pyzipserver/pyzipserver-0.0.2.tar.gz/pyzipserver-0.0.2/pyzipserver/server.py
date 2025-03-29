#!/usr/bin/env python3

import os
import http.server
import socketserver
import ssl
import zipfile
from urllib.parse import urlparse, unquote

class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
	extensions_map = {
		'': 'application/octet-stream',
		'.manifest': 'text/cache-manifest',
		'.html': 'text/html',
		'.png': 'image/png',
		'.jpg': 'image/jpg',
		'.svg':	'image/svg+xml',
		'.css':	'text/css',
		'.js':'application/x-javascript',
		'.mjs':'application/x-javascript',
		'.wasm': 'application/wasm',
		'.json': 'application/json',
		'.xml': 'application/xml',
	}

	def __init__(self, zip_file_path, *args, **kwargs):
		self.zip_file_path = zip_file_path
		super().__init__(*args, **kwargs)
	
	#CORS correction
	def end_headers (self):
		self.send_header('Access-Control-Allow-Origin', '*')
		#self.send_header("Content-Security-Policy", "script-src '<content here>' 'strict-dynamic' 'wasm-unsafe-eval'")
		http.server.SimpleHTTPRequestHandler.end_headers(self)
	
	def do_GET(self):
		try:
			# Open the zip file
			with zipfile.ZipFile(self.zip_file_path, 'r') as zip_file:
				# Remove leading slash if present
				parsed_path = urlparse(self.path)
				file_path = unquote(parsed_path.path).lstrip('/')
				if file_path == '':
					file_path = 'index.html'
				# Check if the requested file is in the zip file
				if file_path in zip_file.namelist():
					# Read the file from the zip
					file_data = zip_file.read(file_path)
					# Guess the content type
					content_type = self.guess_type(file_path)
					
					# Send response
					self.send_response(200)
					self.send_header('Content-type', content_type)
					self.send_header('Content-length', len(file_data))
					self.end_headers()
					
					# Write file data to the response
					self.wfile.write(file_data)
				else:
					self.send_error(404, "File Not Found: %s" % self.path)
		except Exception as e:
			self.send_error(500, "Internal Server Error: %s" % str(e))

class CustomTCPServer(socketserver.TCPServer):
	def __init__(self, server_address, RequestHandlerClass, zip_file_path, **kwargs):
		self.zip_file_path = zip_file_path
		super().__init__(server_address, RequestHandlerClass, **kwargs)

	def finish_request(self, request, client_address):
		self.RequestHandlerClass(self.zip_file_path, request, client_address, self)


def serve(zipfilepath, ip:str, port:int = 8000, ssl_ctx = None):
	httpd = CustomTCPServer((ip, port), HttpRequestHandler, zipfilepath, bind_and_activate=False)
	if ssl_ctx is not None:
		httpd.socket = ssl_ctx.wrap_socket(httpd.socket, server_side=True)
	httpd.server_bind()
	httpd.server_activate()
	
	try:
		print(f"Serving at http://{ip}:{port}")
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	finally:
		httpd.socket.close()

def main():
	import argparse
	parser = argparse.ArgumentParser(description='Simple HTTP server')
	parser.add_argument('-a', '--address', default='0.0.0.0', help='IP/hostname to listen on')
	parser.add_argument('-p', '--port', type=int, default=8000, help='Port to listen on')
	parser.add_argument('--ssl-cert', help='Certificate file for SSL')
	parser.add_argument('--ssl-key',  help='Key file for SSL')
	parser.add_argument('--ssl-ca',  help='CA cert file for client cert validations')
	parser.add_argument('zipfile', help='Path to the zip file to serve')
	args = parser.parse_args()

	ssl_ctx = None
	if args.ssl_cert is not None:
		ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
		if args.ssl_key is None:
			raise Exception('TLS certificate is set but no keyfile!')
		ssl_ctx.load_cert_chain(args.ssl_cert, args.ssl_key)
		if args.ssl_ca is not None:
			ssl_ctx.load_verify_locations(args.ssl_ca)
			ssl_ctx.verify_mode = ssl.CERT_REQUIRED
		#if args.ssl_ciphers is not None:
		#	ssl_ctx.set_ciphers(args.ssl_ciphers)
		#if args.ssl_dh is not None:
		#	ssl_ctx.load_dh_params(args.ssl_dh)

	serve(args.zipfile, args.address, args.port, ssl_ctx)

if __name__ == '__main__':
	main()
