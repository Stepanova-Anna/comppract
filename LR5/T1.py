from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime
import pytz


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()


        timezone = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(timezone).strftime('%d.%m.%y %H:%M:%S')
        login = "1147334"

        result = f"{login}, {current_time}"
        self.wfile.write(bytes(result, "utf-8"))


httpd = HTTPServer(('0.0.0.0', 8080), SimpleHTTPRequestHandler)
print('Сервер запущен на http://localhost:8080/')
httpd.serve_forever()
