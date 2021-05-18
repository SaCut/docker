from people.people import Person


class Staff(Person):
    def __init__(self):
        super().__init__(None, "staff")
        self.flight_assign = None

    def __str__(self):
        return f"{self.oid} {self.first_name} {self.last_name} {self.age} {self.flight_assign}"

    def make_from_db(self, oid, first_name, last_name, age, flight_assign):
        super().init_person_data(oid, first_name, last_name, age)
        self.flight_assign = flight_assign
        return self

    def __save_and_regenerate_with_id(self, db_wrapper):
        first_name = self.first_name
        last_name = self.last_name
        age = self.age
        flight_assign = self.flight_assign

        if self.flight_assign is None:
            flight_assign = "Null"

        db_wrapper.cursor.execute(
            f"INSERT INTO {self.table} "
            + f"VALUES ('{first_name}', '{last_name}', {age}, {flight_assign});")

        db_wrapper.connection.commit()

        # Update the dictionary so that this is always correct
        staff = Staff().make_from_db(self.get_max_id(db_wrapper), first_name, last_name, age, flight_assign)

        return staff

    def make_manual(self, first_name, last_name, age, db_wrapper):
        # make a place holder passenger
        self.make_from_db(None, first_name, last_name, age, None)

        # save it and regenerate it
        return self.__save_and_regenerate_with_id(db_wrapper)

    def assign_flight(self, flight_trip, db_wrapper):
        db_wrapper.cursor.execute(f"UPDATE {self.table} "
                                  f"SET flight_trip_id = {flight_trip.oid} "
                                  f"WHERE {self.table}_id = {self.oid}")
        self.flight_assign = flight_trip.oid
