from datetime import date

class Booking:
    # We initialise with all of our attributes
    # Each column in the table should have an attribute here
    def __init__(self, id, booking_from, booking_to, bookers_id, request_outstanding, booked, space_id):
        self.id = id
        self.booking_from = booking_from
        self.booking_to = booking_to
        self.bookers_id = bookers_id
        self.request_outstanding = request_outstanding
        self.booked = booked
        self.space_id = space_id


    # This method allows our tests to assert that the objects it expects
    # are the objects we made based on the database records.
    def __eq__(self, other):
        return (self.id == other.id and
                str(self.booking_from) == str(other.booking_from) and
                str(self.booking_to) == str(other.booking_to) and
                self.bookers_id == other.bookers_id and
                self.request_outstanding == other.request_outstanding and
                self.booked == other.booked and
                self.space_id == other.space_id)

    # This method makes it look nicer when we print an Artist
    def __repr__(self):
        return f"Booking({self.id}, {self.booking_from}, {self.booking_to}, {self.bookers_id}, {self.request_outstanding}, {self.booked}, {self.space_id})"