from aircraft.aircraft import Aircraft

class Plane(Aircraft):
    def __init__(self):
        super().__init__()
        self.plane_model = "Plane model placeholder value"

    def __str__(self):
        return f"{self.oid} {self.flight} {self.flight_capacity} {self.aircraft_type}"

    def make_manual(self, flight, capacity, aircraft_type, db_wrapper):
        super().make_manual(flight, capacity, aircraft_type, db_wrapper)
        return self

    def save_and_regenerate_with_id(self, db_wrapper):
        super().save_and_regenerate_with_id(db_wrapper)
        p = Plane().make_from_db(self.get_max_id(db_wrapper), self.flight, self.flight_capacity, "plane")
        return p
