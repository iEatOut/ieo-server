import os
import http.server
import socketserver
import urllib

PORT = int(os.getenv("VCAP_APP_PORT", "8000"))

class DietrHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_error(404)
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path != "/retrieve":
            self.send_error(404)
            return

        self.send_response(200)

        if parsed.path == "/retrieve":
            import retrieve
            out = retrieve.handleRetrieve(urllib.parse.parse_qs(parsed.query), self)

        self.send_header("Content-type", out[0])
        self.end_headers()

        self.wfile.write(bytes(out[1], "UTF-8"))

httpd = socketserver.TCPServer(("", PORT), DietrHandler)
print("Starting at port", PORT)
httpd.serve_forever()