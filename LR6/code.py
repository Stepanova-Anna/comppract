from flask import Flask, request, jsonify
from PIL import Image
import io

app = Flask(__name__)

MY_LOGIN = "1147334" 

@app.route("/size2json", methods=['POST'])
def size2json():
    if 'image' not in request.files:
        return jsonify({"result": "no file part"}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({"result": "no selected file"}), 400

    try:
        img = Image.open(io.BytesIO(image_file.read()))
        width, height = img.size
        return jsonify({"width": width, "height": height}), 200
    except Exception as e:
        print(e)
        return jsonify({"result": "invalid filetype"}), 400


@app.route("/login")
def login():
    return jsonify({"author": MY_LOGIN}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
