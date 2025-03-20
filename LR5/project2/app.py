from flask import Flask, request, render_template_string
import json
import os
from datetime import datetime

app = Flask(__name__)


DATA_FILE = 'data.json'

@app.route('/')
def index():
    return render_template_string(open('index.html').read())


@app.route('/submit', methods=['POST'])
def submit():
    moodle_login = request.form['moodle_login']
    current_time = request.form['current_time']

    # Считываем существующие данные
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
    else:
        data = []

    # Добавляем новые данные
    data.append({
        "moodle_login": moodle_login,
        "current_time": current_time
    })

    # Сохраняем в JSON файл
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return f"<h1>Данные успешно сохранены!</h1><p>Логин: {moodle_login}</p><p>Текущее время: {current_time}</p>"


if __name__ == '__main__':
    if not os.path.exists(DATA_FILE):
        # Создаем файл, если он не существует, и инициализируем его пустым массивом
        with open(DATA_FILE, 'w') as file:
            json.dump([], file)
    app.run(debug=True)
