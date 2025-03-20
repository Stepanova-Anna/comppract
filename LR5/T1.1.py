from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import datetime
import pytz

LOGIN = "1147334" 

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()

            # Определяем часовой пояс
            timezone = pytz.timezone('Europe/Moscow')


            now = datetime.datetime.now(timezone)
            formatted_date_time = now.strftime("%d.%m.%y %H:%M:%S")

            result = f"{LOGIN}, {formatted_date_time}"
            self.wfile.write(result.encode('utf-8'))
        else:
            # Если запрошен другой путь, возвращаем ошибку 404
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(b"404 Not Found")

httpd = HTTPServer(('0.0.0.0', 8080), SimpleHTTPRequestHandler)

print('Сервер запущен на http://localhost:8080/')
httpd.serve_forever()