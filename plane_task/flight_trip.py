from abstract_db_record import AbstractDbObject


class FlightTrip (AbstractDbObject):
    def __init__(self):
        super().__init__(None, "flight_trip")
        self.ticket_price = None
        self.aircraft = None
        self.duration = None
        self.destination = None
        self.origin = None
        self.passenger_list = None

    def __str__(self):
        return f"{self.oid} {self.ticket_price} {self.aircraft} {self.destination} {self.duration} {self.origin}"

    def make_from_db(self, flight_id, ticket_price, aircraft, destination, duration, origin, passenger_list):
        self.oid = flight_id
        self.ticket_price = ticket_price
        self.aircraft = aircraft
        self.duration = duration
        self.destination = destination
        self.origin = origin
        self.passenger_list = passenger_list
        return self

    def __save_and_regenerate_with_id(self, db_wrapper):
        ticket_price = self.ticket_price
        aircraft = self.aircraft
        destination = self.destination
        duration = self.duration
        origin = self.origin

        if aircraft is not None:
            db_wrapper.cursor.execute(
                f"INSERT INTO {self.table} "
                + f"VALUES ({ticket_price}, {aircraft}, '{destination}', {duration}, '{origin}');")
        else:
            db_wrapper.cursor.execute(
                f"INSERT INTO {self.table} "
                + f"VALUES ({ticket_price}, Null, '{destination}', {duration}, '{origin}');")

        db_wrapper.connection.commit()

        # delete the passenger list
        try:
            db_wrapper.cursor.execute(f"DELETE FROM flight_order WHERE {self.table}_id = {self.oid}")
            db_wrapper.connection.commit()
        except Exception:
            print("ouch")

        # generate the passenger list
        for passenger in self.passenger_list:
            db_wrapper.add_single_flight_order(passenger, self)

        flt = FlightTrip().make_from_db(self.get_max_id(db_wrapper), ticket_price, aircraft, destination, duration, origin, self.passenger_list)
        return flt

    def delete_from_db(self, db_wrapper):
        super().delete_from_db(db_wrapper)
        db_wrapper.cursor.execute(f"DELETE FROM flight_orders WHERE {self.table}_id = {self.oid}")
        db_wrapper.connection.commit()

    def make_manual(self, ticket_price, aircraft_id, destination, duration, origin, db_wrapper):
        # make a place holder passenger
        self.make_from_db(None, ticket_price, aircraft_id, destination, duration, origin, [])

        # generate the real one
        return self.__save_and_regenerate_with_id(db_wrapper)

    def assign_aircraft(self, aircraft, db_wrapper):
        db_wrapper.cursor.execute(f"UPDATE {self.table} "
                                  f"SET aircraft_id = {aircraft.oid} "
                                  f"WHERE {self.table}_id = {self.oid}")
        self.aircraft = aircraft

    def get_seated_passenger_count(self, db_wrapper):
        return self.get_adult_passengers(db_wrapper) + self.get_child_passengers(db_wrapper)

    def get_adult_passengers(self, db_wrapper):
        db_wrapper.cursor.execute(f"SELECT COUNT(*) FROM flight_order "
                                  f"WHERE ticket_type in ('adult') "
                                  f"AND flight_trip_id = {self.oid}")
        return db_wrapper.cursor.fetchone()[0]

    def get_child_passengers(self, db_wrapper):
        db_wrapper.cursor.execute(f"SELECT COUNT(*) FROM flight_order "
                                  f"WHERE ticket_type in ('child') "
                                  f"AND flight_trip_id = {self.oid}")
        return db_wrapper.cursor.fetchone()[0]

    def get_infant_passengers(self, db_wrapper):
        db_wrapper.cursor.execute(f"SELECT COUNT(*) FROM flight_order "
                                  f"WHERE ticket_type in ('infant') "
                                  f"AND flight_trip_id = {self.oid}")
        return db_wrapper.cursor.fetchone()[0]

    def get_staff_assigned(self, db_wrapper):
        db_wrapper.cursor.execute(f"SELECT COUNT(*) FROM staff WHERE flight_trip_id = {self.oid}")
        return db_wrapper.cursor.fetchone()[0]

    def breakdown_flight_info(self, db_wrapper):
        adult = self.get_adult_passengers(db_wrapper)
        child = self.get_child_passengers(db_wrapper)
        infant = self.get_infant_passengers(db_wrapper)
        total = adult + child + infant
        print(f"total passengers: {total}\n"
              f"adults: {adult}\n"
              f"children: {child}\n"
              f"infant: {infant}\n")

        staff = self.get_staff_assigned(db_wrapper)
        print(f"\nStaff assigned: {staff}\n")

        print(f"aircraft: {self.aircraft}")
