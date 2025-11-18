# Flask imports
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# Agents
from src.agents.database import Database, Upload
from src.agents.ollama_client import OllamaClient

# Pydantic models
from src.models.image_description import ImageStroyTelling

# Other
import ollama
import os

# Initalize app -------------------------------------------------------------
app = Flask(__name__)

upload_folder = os.path.join('static', 'uploads')
app.config['UPLOAD'] = upload_folder

# Initialize database
database = Database(app)
database.create_tables()

# Initialize Ollama client
ollama_client = OllamaClient()

# App ------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':

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
        story_model = ollama_client.get_img_story(filepath)
        
        # Upload to database
        database.upload_to_database(filename, story_model)

        return render_template('image_render.html', img=filename, description=story_model)
    return render_template('image_render.html')

# Lets go --------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")

