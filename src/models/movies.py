from datetime import date
from pydantic import BaseModel, Field, field_validator


class MovieUpdate(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str

class Movie(BaseModel):
    id: int
    title: str
    overview: str
    year: int
    rating: float
    category: str

class MovieCreate(BaseModel):
    id: int = Field(default=1)
    title: str # = Field(min_length=5, max_length=20)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=date.today().year, ge=1900)
    rating: float = Field(ge=0, le=10)
    category: str = Field(min_length=5, max_length=25)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "My action movie",
                "overview": "Default overview",
                "year": date.today().year,
                "rating": 10.0,
                "category": "action"
            }
        }
    }

    @field_validator("title")
    def validate_title(cls, value):
        if len(value) < 5:
            raise ValueError("Title field must have a minmum length 5 characters")
        elif len(value) > 20:
            raise ValueError("Title field must have a maximum length 20 characters")

        return value
