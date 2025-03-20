from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = '1147334'  # Замените это значение на свое собственное

data_file = 'data.json'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    login = request.form['login']
    current_time = request.form['current_time']

    # Сохранение данных в файл
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
    else:
        data = []

    # Добавляем новые данные
    data.append({
        'login': login,
        'current_time': current_time,
        'timestamp': datetime.now().isoformat()
    })

    # Сохраняем обновленные данные обратно в файл
    with open(data_file, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    flash('Данные были успешно сохранены!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
