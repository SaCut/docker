import pyodbc
from people.passenger import Passenger
from flight_trip import FlightTrip
from aircraft.aircraft import Aircraft
from aircraft.plane import Plane
from aircraft.helicopter import Helicopter
from people.staff import Staff


class DbWrapper:

    # Opens a file called server_info.cfg and pulls connection info from there
    def __init__(self):
        try:
            file_lines = open("server_info.cfg", "r").readlines()
            self.ip = file_lines[0].strip("\n")
            self.uname = file_lines[1].strip("\n")
            self.password = file_lines[2].strip("\n")
            self.db_name = file_lines[3].strip("\n")

            self.connection = pyodbc.connect('DRIVER={FreeTDS}; ' +
                f'SERVER={self.ip}; PORT=1433; DATABASE={self.db_name}; ' +
                f'UID={self.uname}; PWD{self.password}; TDS_VERSION=8.0')

            self.cursor = self.connection.cursor()
        except FileNotFoundError as err:
            print(err)
            print(f"server_info.config not found!")
            exit(1)

    """ Passenger Functions"""
    # Will be used to pull information from the database
    def load_all_passengers(self):
        dict_passengers = {}
        self.cursor.execute("SELECT * FROM passengers")
        temp_passenger_list = self.cursor.fetchall()

    # Generate passenger objects
        for val in temp_passenger_list:
            passenger = Passenger()
            passenger.make_from_db(val[0], val[1], val[2], val[3], val[4], self)
            dict_passengers[val[0]] = passenger

        return dict_passengers

    """ Flight functions """
    # Get all passengers on a flight using flight_order
    def get_flight_passengers(self, flight_id, passenger_list):
        self.cursor.execute(f"SELECT DISTINCT passengers_id FROM tickets t "
                            f"JOIN flight_order f ON t.ticket_number = f.ticket_number "
                            f"WHERE f.flight_trip_id = {flight_id}")
        flight_passengers = []
        for entry in self.cursor.fetchall():
            flight_passengers.append(passenger_list[entry[0]])

        return flight_passengers

    # Load all FlightTrip objects
    def load_all_flights(self, passenger_dict):
        flight_dict = {}
        self.cursor.execute("SELECT * FROM flight_trip")
        temp_flight_list = self.cursor.fetchall()
        for val in temp_flight_list:
            flight = FlightTrip()
            flight.make_from_db(val[0], val[1], val[2], val[3], val[4], val[5], self.get_flight_passengers(val[0], passenger_dict))
            flight_dict[val[0]] = flight

        return flight_dict

    # add a single flight order to the flight_order table
    def create_ticket_and_add(self, passenger, flight):
        # get the ticket type we will use based on the age of the passenger and get the discount applied
        type = "adult"
        if int(passenger.age) < 2:
            type = "infant"
        elif int(passenger.age) < 12:
            type = "child"

        self.cursor.execute(f"SELECT discount FROM ticket_types WHERE ticket_type = '{type}'")
        discount = float(self.cursor.fetchone()[0])

        # get discounted ticket price
        price = int(flight.ticket_price) * discount

        # make a new ticket for the flight
        self.cursor.execute(f"INSERT INTO flight_order VALUES ('{type}', {price}, {flight.oid})")
        self.connection.commit()

        # Get the ticket number
        self.cursor.execute(f"SELECT MAX(ticket_number) FROM flight_order")
        uid = self.cursor.fetchone()[0]

        # Assign the passenger to the ticket in the db
        self.cursor.execute(f"INSERT INTO tickets VALUES ({passenger.oid}, {uid})")
        self.connection.commit()

        # Add the ticket to the passenger ticket list
        passenger.tickets.append(uid)

        # add the passenger to the flight object
        flight.passenger_list.append(passenger)

    def load_all_aircraft(self):
        dict_aircraft = {}
        self.cursor.execute("SELECT * FROM aircraft")
        temp_passenger_list = self.cursor.fetchall()

        # Generate passenger objects
        for val in temp_passenger_list:
            aircraft = None
            if val[3] == "plane":
                aircraft = Plane().make_from_db(val[0], val[1], val[2], val[3])
            elif val[3] == "heli":
                aircraft = Helicopter().make_from_db(val[0], val[1], val[2], val[3])
            dict_aircraft[val[0]] = aircraft

        return dict_aircraft

    def load_all_staff(self):
        dict_staff = {}
        self.cursor.execute("SELECT * FROM staff")
        temp_passenger_list = self.cursor.fetchall()

        # Generate passenger objects
        for val in temp_passenger_list:
            if val[4] == "Null":
                staff = Staff().make_from_db(val[0], val[1], val[2], val[3], None)
                dict_staff[val[0]] = staff
            else:
                staff = Staff().make_from_db(val[0], val[1], val[2], val[3], val[4])
                dict_staff[val[0]] = staff

        return dict_staff

    def load_passenger_tickets(self, oid):
        try:
            self.cursor.execute(f"SELECT ticket_number FROM tickets WHERE passengers_id = {oid}")
            temp_ticket_list = self.cursor.fetchall()
            return temp_ticket_list
        except:
            return []

