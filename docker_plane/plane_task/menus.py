# To keep run.py cleaner - holds all the code related to displaying and handling menus
from people.passenger import Passenger
from people.staff import Staff
from aircraft.plane import Plane
from aircraft.helicopter import Helicopter
from flight_trip import FlightTrip


# This prints the main menu
def print_main_menu():
    print(f"\n1. Passengers\n"
          f"2. Flights\n"
          f"3. Aircraft\n"
          f"4. Staff\n"
          f"0. exit\n")
    pass


# This handles the input for the main menu
# it sets the flag variable for use in deciding what menu to display
def handle_main_menu(num):
    # These values are the same as the menu selection values
    if num == 0:
        return "exit"
    elif num == 1:
        return "passengers"
    elif num == 2:
        return "flights"
    elif num == 3:
        return "aircraft"
    elif num == 4:
        return "staff"


# Displays and handles the passengers menu
def passengers_menu(db_wrapper, passenger_dict, dict_flights):
    while True:
        print(f"\n1. Create passenger\n"
              f"2. List passengers not on any flight\n"
              f"3. List passengers on a flight\n"
              f"0. Go back\n")

        user_in = num_input("Please enter a number between 0 and 3\n", 3)
        if user_in == 0:
            break
        elif user_in == 1:
            # Creating passenger
            create_passenger(db_wrapper, passenger_dict)

        elif user_in == 2:
            list_passengers_not_in_flight(passenger_dict, dict_flights)
            # print("List the passengers not in a flight so assistant can add them")
            # for p in passenger_dict.values():
            #     print(p)

        elif user_in == 3:
            flight_no = int(input("Please enter a flight ID:\n"))
            get_passengers_on_flight(flight_no, dict_flights)


# Displays and handles the flights menu
def flights_menu(db_wrapper, flight_dict, passenger_dict):
    while True:
        print(f"\n1. Create Flight (Trip)\n"
              f"2. List Flights (Trip)\n"
              f"3. Sell Ticket\n"
              f"4. Breakdown flight info\n"
              f"0. Go back\n")

        user_in = num_input("Please enter a number between 0 and 4\n", 4)
        if user_in == 0:
            break
        elif user_in == 1:
            print("Creating a new Flight")

            # make a flight_trip and add it to the dict
            create_flight_trip(db_wrapper, flight_dict)

        elif user_in == 2:
            print("List of flights!")
            for f in flight_dict.values():
                print(f)

        elif user_in == 3:
            # sell the ticket
            sell_ticket(passenger_dict, flight_dict, db_wrapper)

        elif user_in == 4:
            breakdown_flight(flight_dict, db_wrapper)


# Prints the aircraft menu
def aircraft_menu(db_wrapper, aircraft_dict, flight_dict):
    # create aircraft, show aircrafts,
    while True:
        print(f"\n1. Create Aircraft\n"
              f"2. List Aircrafts\n"
              f"3. Assign Aircraft to Flight\n"
              f"0. Go back\n")

        user_in = num_input("Please enter a number between 0 and 3\n", 3)
        if user_in == 0:
            break
        elif user_in == 1:
            print("Creating Aircraft")
            create_aircraft(db_wrapper, aircraft_dict)
        elif user_in == 2:
            print("Listing Aircrafts")
            for aircraft in aircraft_dict.values():
                print(aircraft)
        elif user_in == 3:
            print("Assigning Aircraft to a flight")
            assign_aircraft(db_wrapper, aircraft_dict, flight_dict)


# Prints the staff menu (currently nothing to add)
def staff_menu(staff_dict, flight_dict, db_wrapper):
    while True:
        print(f"\n1. Create Staff\n"
              f"2. List Staff\n"
              f"3. Assign Flight to Staff\n"
              f"0. Go back\n")

        user_in = num_input("Please enter a number between 0 and 3\n", 3)
        if user_in == 0:
            break
        elif user_in == 1:
            print("Creating Staff")
            create_staff(staff_dict, db_wrapper)
        elif user_in == 2:
            print("Listing Staff")
            for staff in staff_dict.values():
                print(staff)
        elif user_in == 3:
            print("Assigning Flight to a staff")
            assign_staff(flight_dict, staff_dict, db_wrapper)


# Universal input manager, takes an input message and an end index and returns the number entered as an int
def num_input(input_msg, end_index):
    user_input = input(input_msg)
    while not user_input.isdigit() or int(user_input) > end_index:
        user_input = input(f"Please enter a number between 0 and {end_index}:\n")
    return int(user_input)


# Allows the user to enter text information, following the given prompt
# The user cannot leave the value blank by default
def text_input(input_msg, leave_blank=False):
    if leave_blank == True:
        exit_prompt = " Or enter 'done' to exit.\n"
    else:
        exit_prompt = " You must enter a value.\n"

    # user_input = input(input_msg)
    while True:
        user_input = input(input_msg + exit_prompt)  # ask the user for input

        # exit it without returning here
        if user_input == "done":
            break

        confirm_msg = "You entered: '" + user_input + "'. Do you wish to continue? (y/n)\n"

        user_conf = input(confirm_msg)

        if user_conf.lower() == "y" or user_conf.lower == "yes":
            if user_input == "" and leave_blank == False:
                continue  # don't let the user enter a blank value if leave_blank is false
            return user_input
        elif user_conf.lower == "done" and leave_blank == True:
            break  # exit it without returning here


def int_input(input_msg):
    while True:
        user_input = input(input_msg + "\n")

        if user_input.isdigit():
            return int(user_input)
        else:
            print("You must enter a number\n")


def breakdown_flight(flight_dict, db_wrapper):
    flight_id = int_input("Please enter the flight id:\n")
    while flight_id not in flight_dict.keys():
        flight_id = int_input("Please enter the flight id:\n")

    flight_dict[flight_id].breakdown_flight_info(db_wrapper)

def create_staff(staff_dict, db_wrapper):
    input_msg = "Enter the staff's "

    first_name = text_input(input_msg + "first name.")
    last_name = text_input(input_msg + "last name.")
    age = int_input(input_msg + "age.")

    s = Staff().make_manual(first_name, last_name, age, db_wrapper)
    staff_dict[s.oid] = s


def assign_staff(flight_dict, staff_dict, db_wrapper):
    staff_id = int_input("Please enter the staff id:\n")
    while staff_id not in staff_dict.keys():
        staff_id = int_input("Please enter the staff id:\n")

    flight_id = int_input("Please enter the flight id:\n")
    while flight_id not in flight_dict.keys():
        flight_id = int_input("Please enter the flight id:\n")

    staff_dict[staff_id].assign_flight(flight_dict[flight_id], db_wrapper)


# Creates and returns a new passenger object
def create_passenger(db_wrapper, passenger_dict):
    # oid(None), ticket_no, fname, lname, age, pass_no
    input_msg = "Enter the passenger's "

    first_name = text_input(input_msg + "first name.")
    last_name = text_input(input_msg + "last name.")
    age = int_input(input_msg + "age.")
    passport_no = text_input(input_msg + "passport number.")

    p = Passenger().make_manual(first_name, last_name, age, passport_no, db_wrapper)
    passenger_dict[p.oid] = p


# get passenger names and passport numbers from a certain flight
def get_passengers_on_flight(flight_no, flight_dict):
    try:
        print(f"Passengers on flight {flight_no}:")
        flight_passengers = flight_dict[flight_no].passenger_list
        for passenger in flight_passengers:
            print(f"{passenger.first_name} {passenger.last_name} - {passenger.passport_number}\n")
    except KeyError:
        print("Flight not found")


def create_flight_trip(db_wrapper, flight_dict):
    # price (determined by passenger age), aircraft, destination, duration, origin
    input_msg = "Enter the "

    price = 400  # temp value
    aircraft = None  # temp values
    destination = text_input(input_msg + "destination.")
    duration = 24  # temp values
    origin = text_input(input_msg + "flight origin.")

    t = FlightTrip().make_manual(price, aircraft, destination, duration, origin, db_wrapper)
    flight_dict[t.oid] = t


def create_aircraft(db_wrapper, aircraft_dict):
    input_msg = "Is this aircraft a:\n1. plane\n2. helicopter?\n"
    aircraft_type = int_input(input_msg)
    while aircraft_type != 1 and aircraft_type != 2:
        aircraft_type = int_input(input_msg)

    is_flying = False
    capacity = int_input("What is this aircrafts capacity?\n")

    if aircraft_type == 1:
        plane = Plane().make_manual(is_flying, capacity, "plane", db_wrapper)
        aircraft_dict[plane.oid] = plane
    else:
        heli = Helicopter().make_manual(is_flying, capacity, "heli", db_wrapper)
        aircraft_dict[heli.oid] = heli


def assign_aircraft(db_wrapper, aircraft_dict, flight_dict):
    flight_id = int_input("Please enter the flight id:\n")
    while flight_id not in flight_dict.keys():
        flight_id = int_input("Please enter the flight id:\n")

    aircraft_id = int_input("Please enter the aircraft id:\n")
    while aircraft_id not in aircraft_dict.keys():
        aircraft_id = int_input("Please enter the aircraft id:\n")

    flight_dict[flight_id].assign_aircraft(aircraft_dict[aircraft_id], db_wrapper)


def sell_ticket(passenger_dict, flight_dict, db_wrapper):
    # test with passenger id = and

    pass_id_msg = "Enter passenger oid\n"
    flight_id_msg = "Enter flight oid\n"

    passenger_id = int_input(pass_id_msg)
    while passenger_id not in passenger_dict.keys():
        passenger_id = int_input(pass_id_msg)

    flight_id = int_input(flight_id_msg)
    while flight_id not in flight_dict.keys():
        flight_id = int_input(flight_id_msg)

    flight = flight_dict[flight_id]
    print(flight.aircraft)
    if flight.aircraft is not None:
        # If the amount of passengers taking up seats is equal to or less than the capacity of the plane assigned
        if flight.get_seated_passenger_count(db_wrapper) < flight.aircraft.flight_capacity:
            db_wrapper.create_ticket_and_add(passenger_dict[passenger_id], flight)
        else:
            print("Sorry that flight is full")
    else:
        print("Please assign an aircraft to this flight first!")

# this is just to get functionality - it won't look nice
def list_passengers_not_in_flight(passenger_dict, flight_dict):
    # create a list of passengers in a flight
    # return the passengers that are *not* in that list
    passengers_in_flight = []
    for flight in flight_dict.values():
        for passenger in passenger_dict.values():
            if passenger in flight.passenger_list:
                passengers_in_flight.append(passenger)

    for passenger in passenger_dict.values():
        if passenger not in passengers_in_flight:
            print(passenger)