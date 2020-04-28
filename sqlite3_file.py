import sqlite3

from fastapi import APIRouter, HTTPException, status

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
async def get_composer(composer_name: str = 'Miles Davis'):
    data = router.db_connection.execute("""SELECT Name from tracks WHERE Composer = :composer""",
                                        {'composer': composer_name,}).fetchall()
    if not data:
        print('nie ma takiego composera')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couldn't find tracks of given composer")
    return data



# zad. 3
# @router.post('/albums')
# def add_new_album(title: str, artist: int):
#     pass









