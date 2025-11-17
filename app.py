from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import ollama

import os

app = Flask(__name__)

upload_folder = os.path.join('static', 'uploads')

app.config['UPLOAD'] = upload_folder


# Ollama description ---------------------------------------------------------
def get_img_description(filepath):
    print(filepath)
    with open(filepath, 'rb')as file:
        response = ollama.chat(
            model='LLaVA-LLaMA3:8b',
            messages = [
                {
                    'role': 'user',
                    'content': 'Tell me a short (3 sentence) science fiction story inspired by this image',
                    'images': [file.read()],
                }
                
            ]
        )
    return response['message']['content']

# App ------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # Upload and save image
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))

        # Ask ollama description
        description = get_img_description(os.path.join(app.config['UPLOAD'], filename))
        print(description)

        return render_template('image_render.html', img=filename, description=description)
    return render_template('image_render.html')

# Lets go --------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=9000)

