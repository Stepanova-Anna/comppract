from flask import Flask
import datetime
import pytz

app = Flask(__name__)

LOGIN = "1147334"

@app.route('/')
def do_get():

    timezone = pytz.timezone('Europe/Moscow')
    now = datetime.datetime.now(timezone)
    formatted_date_time = now.strftime("%d.%m.%y %H:%M:%S")

    result = f"{LOGIN}, {formatted_date_time}"
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)