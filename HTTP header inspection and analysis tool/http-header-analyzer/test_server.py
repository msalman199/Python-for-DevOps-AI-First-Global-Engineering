from http.server import HTTPServer, SimpleHTTPRequestHandler

class CustomHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add only one security header for testing
        self.send_header('X-Content-Type-Options', 'nosniff')
        SimpleHTTPRequestHandler.end_headers(self)

# Run on port 8000
HTTPServer(('', 8000), CustomHandler).serve_forever()
