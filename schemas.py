from enum import Enum
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, field_validator


class GenreURLChoices(Enum):
    ROCK = 'rock'
    ELECTRONIC = 'electronic'
    METAL = 'metal'
    HIP_HOP = 'hip-hop'

class GenreChoices(Enum):
    ROCK = 'Rock'
    ELECTRONIC = 'Electronic'
    METAL = 'Metal'
    HIP_HOP = 'Hip-Hop'


class Album(BaseModel):
    title: str
    release_date: date


# class Band(BaseModel):
#     id: int
#     name: str
#     genre: str
#     albums: List[Album] = []


class BandBase(BaseModel):
    name: str
    genre: GenreChoices
    albums: List[Album] = []


class BandCreate(BandBase):
    @field_validator('genre', mode='before')
    def title_case_genre(cls, value):
        print(value)
        return value.title()

class BandWithID(BandBase):
    id: int