# testing unit
from people.people import Person
from people.passenger import Passenger
from aircraft.aircraft import Aircraft
from flight_trip import FlightTrip
from db_wrapper import DbWrapper
import unittest

global db
db = DbWrapper()

class SimpleTest(unittest.TestCase):

    def test_create_passenger(self):  # naming convention - using 'test' in the name of your function
        p = Passenger().make_manual("ex", "passenger", "tax", "passport", db)
        db.cursor.execute(f"SELECT * FROM passengers WHERE passengers_id = {p.oid}")
        self.assertNotEqual(db.cursor.fetchall(), [])  # is it empty?

    def test_load_passengers(self):
        passengers = db.load_all_passengers()
        self.assertGreater(len(passengers.values()), 0)

    def test_create_flight_trip(self):
        t = FlightTrip().make_manual(666, None, "destination", 666, "origin", db)
        db.cursor.execute(f"SELECT * FROM flight_trip WHERE flight_trip_id = {t.oid}")
        self.assertNotEqual(db.cursor.fetchall(), [])  # is it empty?

    def test_load_flight_trip(self):
        flights = db.load_all_flights()
        self.assertGreater(len(flights.values()), 0)

