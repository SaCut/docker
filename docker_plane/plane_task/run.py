import menus
from db_wrapper import DbWrapper
from login import Login
from people.passenger import Passenger

# These dictionaries will eventually contain Passenger and Flight objects
dict_passengers = {}  # Key passenger_id: val Passenger()
dict_flights = {}  # Key flight_id: val FlightTrip()
dict_aircraft = {}  # Key aircraft_id: val Plane() or Helicopter()
dict_staff = {}  # Key staff_id: Staff()

# Lists all flights with important information
def list_flight_info():
    pass


# This is the running code
if __name__ == "__main__":
    # run login method
    login_object = Login()
    if login_object.attempt_login():
        pass
    else:
        raise Exception("Failed login attempt. Contact your neighbourhood coder.")


    # This decides which menu to display
    flag = "main"

    # Essential db loading code
    db_wrapper = DbWrapper()
    dict_passengers = db_wrapper.load_all_passengers()
    dict_flights = db_wrapper.load_all_flights(dict_passengers)
    dict_aircraft = db_wrapper.load_all_aircraft()
    dict_staff = db_wrapper.load_all_staff()

    while flag != "exit":
        db = DbWrapper()
        if flag == "main":  # If main then we are on the main menu
            menus.print_main_menu()
            user_in = menus.num_input("Please select an option between 0 and 4:\n", 4)
            flag = menus.handle_main_menu(user_in)
        elif flag == "passengers":  # passengers menu
            menus.passengers_menu(db, dict_passengers, dict_flights)
            flag = "main"
        elif flag == "flights":  # flights menu
            menus.flights_menu(db, dict_flights, dict_passengers)
            flag = "main"
        elif flag == "aircraft":  # aircraft menu
            menus.aircraft_menu(db, dict_aircraft, dict_flights)
            flag = "main"
        elif flag == "staff":  # staff menu
            menus.staff_menu(dict_staff, dict_flights, db_wrapper)
            flag = "main"

    db_wrapper.connection.close()
