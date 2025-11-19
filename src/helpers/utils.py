from src.models.image_description import ImageStroyTelling
from pydantic import ValidationError

GENRE_BG = {
    "Fantasy": "#f6e8ff",
    "Sci-fi": "#e8f4ff",
    "Horror": "#2b2b2b",
    "Mystery": "#f5f2e9",
    "Adventure": "#fff4e6",
    "Fairy-tale": "#fff0f6",
    "Childeren's story": "#fffbda",
    "Post-apocalyptic": "#efe9e0",
}


def get_info_from_database(existing_file):
    if existing_file.genre:
        title = f"This is a {existing_file.genre} story about {existing_file.animal}s."
    else:
        title = "This is a story."
    story = existing_file.story if existing_file.story else existing_file.raw_description
    color = GENRE_BG.get(existing_file.genre, "#FFFFFF") if existing_file.genre else "#FFFFFF"
    return title, story, color

def parse_response(response_raw, model):
    try:
        parsed = model.parse_raw(response_raw)
        return parsed
    except ValidationError as e:
        raise Exception(f"Error parsing response: {e}, response_raw: {response_raw}")
        return None

def get_info_from_parsed(parsed):
    title = f"This is a {parsed.genre} story about {parsed.animal}s." if parsed.genre else "This is a story."
    story = parsed.story if parsed.story else "No story available."
    color = GENRE_BG.get(parsed.genre, "#FFFFFF") if parsed.genre else "#FFFFFF"
    return title, story, color