from pydantic import BaseModel, Field

class ImageStroyTelling(BaseModel):
    background_color: str = Field(description="Background color of the image")
    genre: Literal[
        "Fantasy",
        "Sci-fi",
        "Horror",
        "Mystery",
        "Adventure",
        "Fairy-tale",
        "Childeren's story",
        "Post-apocalyptic"
        ] = Field(description="Genre of the image")
    animal: str = Field(description="Type of animal in the image")
    num_animals: int = Field(description="Number of animals in the image")
    story: str = Field(description="A short story inspired by the image in the associated genre, maximum 100 words")