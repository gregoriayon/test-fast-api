from fastapi import FastAPI, HTTPException, Query
from schemas import GenreURLChoices, BandBase, BandCreate, BandWithID
from typing import List, Dict, Optional, Union
from typing_extensions import Annotated


app = FastAPI()


BANDS = [
    {'id': 1, 'name': 'The Kniks', 'genre': 'Rock'},
    {'id': 2, 'name': 'Aphex Twin', 'genre': 'Electronic'},
    {'id': 3, 'name': 'Black Sabbath', 'genre': 'Metal', 'albums': [
        {'title': 'Master of Reality', 'release_date': '1971-07-21'}
    ]},
    {'id': 4, 'name': 'Wu-Tang Clan', 'genre': 'Hip-Hop'},
    {'id': 5, 'name': 'The Calling', 'genre': 'Rock', 'albums': [
        {'title': 'Two', 'release_date': '2004-06-08'}
    ]},
]

@app.get("/")
async def index_view():
    return {"Hello": "Developers"}


@app.get("/bands/list/")
async def bands_list_view(
        genre: Optional[GenreURLChoices] = None, 
        has_albums: bool = False,
        q: Annotated[Union[str, None], Query(max_length=50)] = None
    ) -> List[BandWithID]:

    band_list =  [BandWithID(**b) for b in BANDS]
    if genre:
        band_list =  [
            b for b in band_list if b.genre.value.lower() == genre.value
        ]
    if has_albums:
        band_list =  [
            b for b in band_list if len(b.albums) > 0
        ]

    if q:
        band_list =  [
            b for b in band_list if q.lower() in b.name.lower()
        ]

    return band_list


@app.get("/band/{band_id}")
async def get_band_item(band_id: int) -> BandWithID:
    # band = []
    # for i in range(len(BANDS)):
    #     if BANDS[i]['id'] == band_id:
    #         band.append(BANDS[i])
    #         break

    band = next((BandWithID(**b) for b in BANDS if b['id'] == band_id), None)

    if band is None:
        raise HTTPException(status_code=404, detail='Band is not found!')

    return band



@app.get("/bands/genre/{genre}")
async def bands_for_genre(genre: GenreURLChoices) -> List[Dict]:
    return [
        b for b in BANDS if b['genre'].lower() == genre.value
    ]



@app.get("/about")
async def about_view():
    return "this is an about page!"


@app.post("/")
async def create_band_view(band_data: BandCreate) -> BandWithID:
    id = BANDS[-1]['id'] + 1
    band = BandWithID(id=id, **band_data.model_dump()).model_dump()
    print(band)
    BANDS.append(band)

    return band

