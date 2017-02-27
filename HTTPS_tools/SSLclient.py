s = socket.socket(socket.AF_INET)
serverAddress = ('localhost',4443)

context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True
context.load_verify_locations(r'path/to/server.crt')

ssl_sock = context.wrap_socket(s,server_hostname='some_hostname')
ssl_sock.connect(serverAddress)

cert = ssl_sock.getpeercert()
pprint.pprint(cert)

ssl_sock.sendall('HEAD / HTTP/1.0\r\nHost: "boo!"\r\n\r\n'.encode())
pprint.pprint(ssl_sock.recv(1024).split(b'\r\n'))
