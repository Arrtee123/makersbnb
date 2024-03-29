from lib.booking_repository import BookingRepository
from lib.booking import Booking
from datetime import date

def test_all(db_connection):
    db_connection.seed("seeds/spaces.sql")
    repo = BookingRepository(db_connection)
    bookings = repo.all()
    assert bookings == [Booking(1, '2024-10-23', '2024-10-23', 2, True, False,  1), Booking(2, '2024-05-21', '2024-05-21', 1, True, False, 3), Booking(3, '2024-12-02', '2024-12-02', 3, True, False,  4), Booking(4, '2024-06-16', '2024-06-16', 1, True, False, 2)]

def test_find(db_connection):
    db_connection.seed("seeds/spaces.sql")
    repo = BookingRepository(db_connection)
    booking = repo.find(2)
    assert booking == Booking(2, '2024-05-21', '2024-05-21', 1, True, False, 3)

def test_create(db_connection):
    db_connection.seed("seeds/spaces.sql")
    repo = BookingRepository(db_connection)
    repo.create('2024-11-27', '2024-11-27', 1, 4)
    bookings = repo.all()
    assert bookings == [Booking(1, '2024-10-23', '2024-10-23', 2, True, False,  1), Booking(2, '2024-05-21', '2024-05-21', 1, True, False, 3), Booking(3, '2024-12-02', '2024-12-02', 3, True, False,  4), Booking(4, '2024-06-16', '2024-06-16', 1, True, False, 2), Booking(5,'2024-11-27', '2024-11-27', 1, True, False, 4)]
  
def test_update(db_connection):
    db_connection.seed("seeds/spaces.sql")
    repo = BookingRepository(db_connection)
    booking = repo.find(1)
    booking.booking_from = '2024-10-24'
    booking.booking_to = '2024-10-24'
    repo.update(booking)
    result = repo.find(1)
    assert result == Booking(1, '2024-10-24', '2024-10-24', 2, True, False, 1)

def test_delete(db_connection):
    db_connection.seed("seeds/spaces.sql")
    repo = BookingRepository(db_connection)
    repo.delete(2)
    assert repo.all() == [Booking(1, '2024-10-23', '2024-10-23', 2, True, False, 1), Booking(3, '2024-12-02', '2024-12-02', 3, True, False, 4), Booking(4, '2024-06-16', '2024-06-16', 1, True, False, 2)]

def test_find_requests(db_connection):
    db_connection.seed("seeds/spaces.sql")
    repo = BookingRepository(db_connection)
    booking = repo.find_requests_outstanding(2)
    assert booking == [Booking(1, '2024-10-23', '2024-10-23', 2, True, False,  1)]

