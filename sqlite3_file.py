import sqlite3
from fastapi import APIRouter


router = APIRouter()

@router.on_event("startup")
def startup():
    router.db_connection = sqlite3.connect('chinook.db', check_same_thread=False)


@router.on_event("shutdown")
def shutdown():
    router.db_connection.close()


@router.get('/tracks')
def get_tracks(page: int = 0, per_page: int = 10):
    limit = per_page
    offset = per_page * page

    router.db_connection.row_factory = sqlite3.Row
    cursor = router.db_connection.cursor()
    data = cursor.execute(
        """SELECT * FROM tracks ORDER BY TrackId
         LIMIT :limit 
         OFFSET :offset""", {'limit': limit,
                             'offset': offset}).fetchall()

    return data











