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

# zad. 2 NIE WIEM CZEMU TO CUDO NIE PRZECHODZI TESTOW
@router.get('/tracks/composers')
async def get_composer(composer_name: str):
    data = router.db_connection.execute("""SELECT Name from tracks WHERE Composer = :composer
                                        ORDER BY Name""",
                                        {'composer': composer_name,}).fetchall()
    if not data:
        print('nie ma takiego composera')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Couldn't find tracks of given composer"})

    data_as_list = [i["Name"] for i in data]
    return data_as_list



# zad. 3
# @router.post('/albums')
# def add_new_album(title: str, artist: int):
#     pass









