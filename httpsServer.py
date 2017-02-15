import http.server
import ssl
import socket

server_address = ('localhost', 4443)
keyfile = r'path/to/server.key'
certfile = r'path/to/server.crt'

webd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
webd.socket = ssl.wrap_socket(httpd.socket,keyfile,certfile,server_side=True)
webd.serve_forever()
