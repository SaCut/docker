from abstract_db_record import AbstractDbObject


class Aircraft(AbstractDbObject):

    def __init__(self):
        super().__init__(None, "aircraft")
        self.flight = False  # temp value
        self.flight_capacity = None
        self.aircraft_type = None

    def __str__(self):
        return f"{self.oid} {self.flight} {self.flight_capacity} {self.aircraft_type}"

    def save_and_regenerate_with_id(self, db_wrapper):
        flying = int(self.flight)
        print(flying)

        db_wrapper.cursor.execute(
            f"INSERT INTO aircraft "
            + f"VALUES ({flying}, {self.flight_capacity}, '{self.aircraft_type}');")

        db_wrapper.connection.commit()

        self.oid = self.get_max_id(db_wrapper)
        return self

    def make_from_db(self, oid, flight, capacity, aircraft_type):
        self.oid = oid
        self.flight = flight
        self.flight_capacity = capacity
        self.aircraft_type = aircraft_type
        return self

    def make_manual(self, flight, capacity, aircraft_type, db_wrapper):
        # make a place holder aircraft
        self.make_from_db(None, flight, capacity, aircraft_type)

        # save it and regenerate it
        return self.save_and_regenerate_with_id(db_wrapper)

    def delete_from_db(self, db_wrapper):
        super().delete_from_db(db_wrapper)
        db_wrapper.cursor.execute(f"UPDATE flight_trip SET {self.table}_id = Null WHERE {self.table}_id = {self.oid}")
        db_wrapper.connection.commit()

    def fly(self):
        pass

    def land(self):
        pass

    def fuel_up(self):
        pass
