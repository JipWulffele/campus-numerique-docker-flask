from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

import ollama

import os

app = Flask(__name__)

upload_folder = os.path.join('static', 'uploads')

app.config['UPLOAD'] = upload_folder


# Ollama description ---------------------------------------------------------
ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
client = ollama.Client(host=ollama_host)
MODEL = "moondream:v2"
client.pull(MODEL) # pull model

def get_img_description(filepath):
    with open(filepath, 'rb') as file:
        image_bytes = file.read()
        response = client.chat(
            model=MODEL,
            messages = [
                {
                    'role': 'user',
                    'content': 'Tell me a short science fiction story inspired by this image. 50 words maximum.',
                    'images': [image_bytes],
                }
                
            ]
        )
    return response['message']['content']

# Upload to database ---------------------------------------------------------

db = SQLAlchemy() # Create the SQLAlchemy instance

# Initialize database
def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        "DATABASE_URL", "postgresql://flaskuser:flaskpass@localhost:5432/flaskdb"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

init_db(app)

# db structure
class Upload(db.Model):
    __tablename__ = 'upload'

    filename = db.Column(db.String(50), primary_key=True)
    img = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

# Create tables on app startup
with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")

# Function to upload to db
def upload_to_database(file, filename, text):
    mimetype = file.mimetype

    upload = Upload(
        filename=filename,
        img=file.read(),
        description=text,
        mimetype=mimetype
    )

    db.session.add(upload)
    db.session.commit()


# App ------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        print("Received POST request")
        # Upload and save image
        file = request.files['img']
        filename = secure_filename(file.filename)
        os.makedirs(app.config['UPLOAD'], exist_ok=True)
        filepath = os.path.join(app.config['UPLOAD'], filename)
        file.save(filepath)
        
        # Check if file already exists in database
        existing_file = Upload.query.filter_by(filename=filename).first()
        if existing_file:
            return render_template('image_render.html', img=filename, description=existing_file.description)

        # Ask ollama description
        description = get_img_description(filepath)
        
        # Upload image and description to database
        upload_to_database(file, filename, description)

        return render_template('image_render.html', img=filename, description=description)
    return render_template('image_render.html')

# Lets go --------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")

