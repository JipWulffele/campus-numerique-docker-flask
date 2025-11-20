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

# Config
from src.config.config import Config
config = Config()

# Other
import ollama
import os

# Set testing flag ----------------------------------------------------------
TEST = False  # Set to False to use the actual Ollama client

# Initalize app -------------------------------------------------------------
app = Flask(__name__)
app.config.from_object(config)

# Set upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
database = Database(app)
database.create_tables()

# Initialize Ollama client
ollama_client = OllamaClient(model=config.OLLAMA_MODEL, host=config.OLLAMA_HOST)

# App ------------------------------------------------------------------------
@app.route("/", methods=["GET"])
def upload_page():
    return render_template("upload.html")

@app.route('/process', methods=['POST'])
def main():
    # Upload and save image
    file = request.files['img']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Check if file already exists in database
    existing_file = Upload.query.filter_by(filename=filename).first()
    if existing_file:
        context = get_info_from_database(existing_file)
        return render_template('result.html', img=filename, **context)

    # Ask ollama description
    if TEST: # for testing purposes
        response_raw = """{"background_color": "light blue",
                        "genre": "Horror",
                        "genre_reasoning": "The light blue background contrasts with the presence of a dragon, creating an eerie and unsettling atmosphere typical of the Horror genre.",
                        "animal": "dragon",
                        "num_animals": 1,
                        "story": "In a mystical land, a lone dragon soars through the light blue skies, its scales shimmering in the sunlight as it embarks on an epic quest to find a hidden treasure.",
                        "title": "The Dragon's Quest"}"""
    else:
        response_raw = ollama_client.get_img_story(filepath)
    parsed = parse_response(response_raw, ImageStroyTelling)

    # Upload to database
    database.upload_to_database(filename, response_raw, parsed)

    # Render template
    context = get_info_from_parsed(parsed)
    return render_template('result.html', img=filename, **context)



# Lets go --------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=config.FLASK_DEBUG, port=config.FLASK_PORT, host="0.0.0.0")

