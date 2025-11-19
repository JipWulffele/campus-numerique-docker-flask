from src.models.image_description import ImageStroyTelling
from pydantic import ValidationError

GENRE_BG = {
    "Fantasy": "#f6e8ff",
    "Sci-fi": "#e8f4ff",
    "Horror": "#4a1f1f",
    "Mystery": "#f5f2e9",
    "Adventure": "#fff4e6",
    "Fairy-tale": "#fff0f6",
    "Childeren's story": "#fffbda",
    "Post-apocalyptic": "#efe9e0",
}


def get_info_from_database(existing_file):
    # Title and story
    title = existing_file.title if existing_file.title else "This is a story."
    story = existing_file.story if existing_file.story else existing_file.raw_description
    
    # Other info
    bg_color = GENRE_BG.get(existing_file.genre, "#FFFFFF") if existing_file.genre else "#FFFFFF"
    llm_color = existing_file.llm_color if existing_file.llm_color else "#FFFFFF"
    animal = existing_file.animal if existing_file.animal else "animal"
    num_animals = existing_file.num_animals if existing_file.num_animals else 1
    genre_reasoning = existing_file.genre_reasoning if existing_file.genre_reasoning else "various genres"
    genre = existing_file.genre if existing_file.genre else "various genres"

    return {"title": title,
            'story': story,
            'bg_color': bg_color,
            'llm_color': llm_color,
            'animal': animal,
            'num_animals': num_animals,
            'genre_reasoning': genre_reasoning,
            'genre': genre}

def parse_response(response_raw, model):
    try:
        parsed = model.parse_raw(response_raw)
        return parsed
    except ValidationError as e:
        raise Exception(f"Error parsing response: {e}, response_raw: {response_raw}")
        return None

def get_info_from_parsed(parsed):
     # Title and story
    title = parsed.title if parsed.title else "This is a story."
    story = parsed.story if parsed.story else parsed.raw_description
    
    # Other info
    bg_color = GENRE_BG.get(parsed.genre, "#FFFFFF") if parsed.genre else "#FFFFFF"
    llm_color = parsed.background_color if parsed.background_color else "#FFFFFF"
    animal = parsed.animal if parsed.animal else "animal"
    num_animals = parsed.num_animals if parsed.num_animals else 1
    genre_reasoning = parsed.genre_reasoning if parsed.genre_reasoning else "various genres"
    genre = parsed.genre if parsed.genre else "various genres"

    return {"title": title,
            'story': story,
            'bg_color': bg_color,
            'llm_color': llm_color,
            'animal': animal,
            'num_animals': num_animals,
            'genre_reasoning': genre_reasoning,
            'genre': genre}
