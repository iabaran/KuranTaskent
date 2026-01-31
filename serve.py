import http.server
import socketserver
import socket
import os

PORT = 8000

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(CORSRequestHandler, self).end_headers()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

Handler = CORSRequestHandler

try:
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        ip = get_ip()
        print(f"\n Server started successfully!")
        print(f" --------------------------------------------")
        print(f" Local Access:   http://localhost:{PORT}/KuranOkuyucu.html")
        print(f" Network Access: http://{ip}:{PORT}/KuranOkuyucu.html")
        print(f" --------------------------------------------")
        print(f" Press Ctrl+C to stop the server.\n")
        httpd.serve_forever()
except OSError as e:
    if e.errno == 98 or e.errno == 10048: # Address already in use
        print(f"Error: Port {PORT} is already in use. Try killing other python processes or change the PORT in the script.")
    else:
        print(f"Error starting server: {e}")
except KeyboardInterrupt:
    print("\nServer stopped.")
