from flask import Flask, render_template, request, jsonify, make_response
from cryptography.fernet import Fernet

app = Flask(__name__)

def decrypt_message(key_file_content, encrypted_message):
    """Расшифровывает зашифрованное сообщение с использованием Fernet."""
    try:
        f = Fernet(key_file_content)
        decrypted_message = f.decrypt(encrypted_message)
        return decrypted_message.decode('utf-8')
    except Exception as e:
        return f"Ошибка расшифровки: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return jsonify({"author": "1147334"})

@app.route('/decypher', methods=['POST'])
def decypher():
    if 'key' not in request.files or 'secret' not in request.files:
        return jsonify({"error": "Отсутствует ключ или зашифрованное сообщение"}), 400

    key_file = request.files['key']
    secret_file = request.files['secret']

    if not key_file or not secret_file:
        return jsonify({"error": "Не указан файл ключа или зашифрованное сообщение"}), 400

    try:
        key_file_content = key_file.read()
        secret_file_content = secret_file.read()
    except Exception as e:
        return jsonify({"error": f"Ошибка чтения файла: {str(e)}"}), 500

    try:
        decrypted_text = decrypt_message(key_file_content, secret_file_content)
    except Exception as e:
        return jsonify({"error": f"Ошибка расшифровки: {str(e)}"}), 500

    response = make_response(decrypted_text, 200)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)