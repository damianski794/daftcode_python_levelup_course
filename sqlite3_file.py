import sqlite3

from fastapi import APIRouter, HTTPException, status, Response
from pydantic import BaseModel
from typing import Optional

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
    artist_id: int

class Album_response(BaseModel):
    AlbumId: int
    Title: str
    ArtistId: int

# zad. 3
@router.post('/albums', response_model=Album_response)
async def add_new_album(album: Album, response: Response):
    cursor = router.db_connection.cursor()
    check_if_artist_exitsts = cursor.execute(
        """SELECT * FROM artists WHERE ArtistId = :artist_id""", {"artist_id": album.artist_id}).fetchall()

    if not check_if_artist_exitsts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "given artist (artist_id) does not exist"})

    cursor.execute(
        """INSERT INTO albums (Title,ArtistId) VALUES (:title,:artist_id);""", {"title": album.title,"artist_id": album.artist_id})
    router.db_connection.commit()

    response.status_code = status.HTTP_201_CREATED

    return Album_response(AlbumId=cursor.lastrowid, Title=album.title, ArtistId=album.artist_id)


@router.get("/albums/{album_id}")
async def get_album(album_id: int):
    data = router.db_connection.execute(
        """SELECT * FROM albums WHERE AlbumId = :album_id""", {'album_id': album_id}).fetchone()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "no albums assigned to this album_id"})

    return data


 # zad. 4
class Customer(BaseModel):
     company: Optional[str] = None
     address: Optional[str] = None
     city: Optional[str] = None
     state: Optional[str] = None
     country: Optional[str] = None
     postalcode: Optional[str] = None
     fax: Optional[str] = None

class Customer_response(BaseModel):
    CustomerId: int
    FirstName: str
    LastName: str
    Company: str
    Address: str
    City: str
    State: str
    Country: str
    PostalCode: str
    Phone: str
    Fax: str
    Email: str
    SupportRepId: int

@router.put('/customers/{customer_id}')
async def update_customer(customer: Customer, customer_id: int = 1):
    cursor = router.db_connection.cursor()
    customer_check_if_exists = cursor.execute("SELECT * FROM customers WHERE CustomerId = :customer_id", {"customer_id": customer_id}).fetchone()

    if not customer_check_if_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"error": "no customer assigned to this album_id"})

    customer_dict: Customer = customer.dict()

    cursor = router.db_connection.execute(
        """UPDATE customers
        SET
        company = IFNULL(:company,company),
        address = IFNULL(:address, address),
        city = IFNULL(:city,city),
        state = IFNULL(:state,state),
        country = IFNULL(:country,country),
        PostalCode = IFNULL(:postal_code,PostalCode),
        Fax = IFNULL(:fax,Fax)
        
        WHERE CustomerId = :customer_id""", {"customer_id": customer_id,
                                             "company": customer_dict["company"],
                                             "address": customer_dict["address"],
                                             "city": customer_dict["city"],
                                             "state": customer_dict["state"],
                                             "country": customer_dict["country"],
                                             "postal_code":customer_dict["postalcode"],
                                             "fax": customer_dict["fax"]})
    router.db_connection.commit()

    customer_selected = cursor.execute("SELECT * FROM customers WHERE CustomerId = :customer_id", {"customer_id": customer_id}).fetchone()
    return customer_selected


@router.get('/customers/{customer_id}')
async def get_customer(customer_id: int):
    cursor = router.db_connection.cursor()
    customer_check_if_exists = cursor.execute("SELECT * FROM customers WHERE CustomerId = :customer_id",
                                              {"customer_id": customer_id}).fetchone()
    if not customer_check_if_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"error": "no customer assigned to this album_id"})

    return customer_check_if_exists


# zad. 5
@router.get('/sales')
async def get_statistics(category: str):
    if category == "customers":
        cursor = router.db_connection.cursor() #
        return cursor.execute(
            """SELECT c.customerid, c.Email, c.Phone, ROUND(SUM(ii.unitprice * ii.quantity),2) AS SUM FROM customers c
            JOIN invoices i 
            ON c.customerid = i.customerid
            JOIN invoice_items ii
            ON i.invoiceid = ii.invoiceid
            GROUP BY c.customerid
            ORDER BY SUM DESC, c.customerid""").fetchall()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"error": "incorrect category"})
