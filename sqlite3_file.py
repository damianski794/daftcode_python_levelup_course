import sqlite3

from fastapi import APIRouter, HTTPException, status, Response
from pydantic import BaseModel

router = APIRouter()

@router.on_event("startup")
async def startup():
    router.db_connection: sqlite3.Connection = sqlite3.connect('chinook.db')#, check_same_thread=False)
    router.db_connection.row_factory = sqlite3.Row

@router.on_event("shutdown")
async def shutdown():
    router.db_connection.close()


@router.get('/tracks')
async def get_tracks(page: int = 0, per_page: int = 10):
    limit = per_page
    offset = per_page * page

    cursor = router.db_connection.cursor()
    data = cursor.execute(
        """SELECT * FROM tracks ORDER BY TrackId
         LIMIT :limit 
         OFFSET :offset;""", {'limit': limit,
                             'offset': offset}).fetchall()

    return data

# zad. 2
@router.get('/tracks/composers')
async def get_composer(composer_name: str):
    data = router.db_connection.execute("""SELECT Name from tracks WHERE Composer = :composer
                                        ORDER BY Name""",
                                        {'composer': composer_name,}).fetchall()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Couldn't find tracks of given composer"})

    data_as_list = [i["Name"] for i in data]
    return data_as_list


class Album(BaseModel):
    title: str
    artist: int

class Album_response(BaseModel):
    AlbumId: int
    Title: str
    ArtistId: int

# zad. 3
@router.post('/albums', response_model=Album_response)
async def add_new_album(album: Album, response: Response):
    cursor = router.db_connection.cursor()
    check_if_artist_exitsts = cursor.execute(
        """SELECT * FROM artists WHERE ArtistId = :artist_id""", {"artist_id": album.artist}).fetchall()
    # print(check_if_artist_exitsts)
    if not check_if_artist_exitsts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "given artist (artist_id) does not exist"})

    cursor.execute(
        """INSERT INTO albums (Title,ArtistId) VALUES (:title,:artist_id);""", {"title": album.title,"artist_id": album.artist})
    router.db_connection.commit()

    response.status_code = status.HTTP_201_CREATED

    return Album_response(AlbumId=cursor.lastrowid, Title=album.title, ArtistId=album.artist)



@router.get("/albums/{album_id}")
async def get_album(album_id: int):
    data = router.db_connection.execute(
        """SELECT * FROM albums WHERE AlbumId = :album_id""", {'album_id': album_id}).fetchone()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "no albums assigned to this album_id"})

    print("return data w get album id, to:")
    print(data)
    
    return data
