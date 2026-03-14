import http.server
import ssl

PORT = 4443

server = http.server.HTTPServer(
    ("0.0.0.0", PORT),
    http.server.SimpleHTTPRequestHandler
)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain("cert.pem", "key.pem")

server.socket = context.wrap_socket(server.socket, server_side=True)

print("HTTPS server running on port", PORT)
server.serve_forever()
