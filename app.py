# Flask imports
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# Agents
from src.agents.database import Database, Upload
from src.agents.ollama_client import OllamaClient

# Pydantic models
from src.models.image_description import ImageStroyTelling

# helpers
from src.helpers.utils import parse_response, get_info_from_database, get_info_from_parsed

# Other
import ollama
import os

# Set testing flag ----------------------------------------------------------
TEST = False  # Set to False to use the actual Ollama client

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
            title, story, color = get_info_from_database(existing_file)
            return render_template('index.html', img=filename, title=title, description=story, color=color)

        # Ask ollama description
        if TEST: # for testing purposes
            response_raw = """{"background_color": "light blue",
                            "genre": "Horror",
                            "animal": "dragon",
                            "num_animals": 1,
                            "story": "In a mystical land, a lone dragon soars through the light blue skies, its scales shimmering in the sunlight as it embarks on an epic quest to find a hidden treasure."}"""
        else:
            response_raw = ollama_client.get_img_story(filepath)
        parsed = parse_response(response_raw, ImageStroyTelling)

        # Upload to database
        database.upload_to_database(filename, response_raw, parsed)

        # Render template
        title, story,  bg_color = get_info_from_parsed(parsed)
        return render_template('index.html', img=filename, title=title, description=story, bg_color=bg_color)

    return render_template('index.html')

# Lets go --------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")

