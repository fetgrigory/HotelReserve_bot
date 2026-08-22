from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    text: str = Field(
        min_length=60,
        max_length=512,
    )
