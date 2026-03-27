import http.server
import ssl
import threading
import time
import json

from random import uniform as aligned
PORT = 4443
telemetry = {}
interval = 1/50
telemetry = {}

def sensor_simulator():
    while True:
        telemetry["pressure"] = round(aligned(20, 30), 2)
        telemetry["humidity"] = round(aligned(20, 30), 2)  
        telemetry["temperature"] = round(aligned(20, 30), 2)
        telemetry["altitude"] = round(aligned(20, 30), 2)
        return telemetry

"""while True:
    start =time.time()
    print(sensor_simulator())
    elapsed = time.time() - start
    time.sleep(max(0, interval - elapsed))
"""
sensor_simulator()
print(telemetry)
server = http.server.HTTPServer(
    ("0.0.0.0", PORT),
    http.server.SimpleHTTPRequestHandler
)

#context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
#context.load_cert_chain("../cert.pem", "../key.pem")

#server.socket = context.wrap_socket(server.socket, server_side=True)

print("HTTP server running on port", PORT)
try:
    server.serve_forever(poll_interval = 5)
    print(344)
except KeyboardInterrupt:
    print("\nShutting down server...")
    server.shutdown()
    server.server_close()
##x = input("press 0 to terminate connection");
