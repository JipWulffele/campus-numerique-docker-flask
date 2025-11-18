from pydantic import BaseModel, Field

class ImageStroyTelling(BaseModel):
    background_color: str = Field(description="Background color of the image")
    genre: str = Field(description="Genre of the image (e.g., fantasy, sci-fi, horror)")
    animal: str = Field(description="Type of animal in the image")
    num_animals: int = Field(description="Number of animals in the image")
    story: str = Field(description="A short story inspired by the image in the associated genre, maximum 100 words")