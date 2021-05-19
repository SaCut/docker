from flask import Flask, render_template, redirect, url_for, request
import login as lg
from db_wrapper import DbWrapper
from people.staff import Staff
from people.passenger import Passenger
from flight_trip import FlightTrip
from aircraft.plane import Plane
from aircraft.helicopter import Helicopter
app = Flask(__name__)

log = lg.Login()
global db_wrapper

global dict_passengers
global dict_flights
global dict_aircraft
global dict_staff


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if not log.is_username(request.form["username"]):  # check if username is NOT in database
            # print("1")
            error = "Invalid username.Please try again"
        
        else: # when username is in database

            # hash password
            psswd = log.hash_password(request.form["username"], request.form["password"])

            if not log.right_password(request.form["username"], request.form["password"]):
                # print("2")
                # print((type(request.form["username"]), request.form["password"]))
                error = "Invalid Password. Please try again."
            else:
                # print("3")
                return redirect(url_for("home"))

    return render_template("login.html", error=error)


@app.route("/home/")
def home():
    return render_template("home.html")


@app.route("/flight/")
def flight():
    return render_template("flight.html", len=len(dict_flights), dict_flights=dict_flights)


@app.route("/flight_info/<f_id>")
def flight_info(f_id):
    return render_template("flight_info.html", len=len(dict_flights[int(f_id)].passenger_list), f_id=int(f_id), dict_flights=dict_flights, db_wrapper=db_wrapper)


@app.route("/flight_passengers/<f_id>", methods=["GET", "POST"])
def flight_passengers(f_id):
    passenger_list = dict_flights[int(f_id)].passenger_list
    # print(passenger_list)
    return render_template("flight_passengers.html", len=len(passenger_list), passenger_list=passenger_list, f_id=f_id)

@app.route("/flight_new/", methods=["GET", "POST"])
def flight_new():
    if request.method == "POST":
        if len(dict_aircraft) == 0:
            return redirect(url_for("aircraft"))
        try:
            real_aircraft = dict_aircraft[int(request.form['aircraft'].split(" ")[0])]
            f = FlightTrip().make_manual(request.form["price"], None, request.form["destination"], request.form["duration"], request.form["origin"], db_wrapper)
            f.assign_aircraft(real_aircraft, db_wrapper)
            dict_flights[int(f.oid)] = f
            return redirect(url_for("flight"))
        except:
            return redirect(url_for("flight_new"))
    return render_template("flight_new.html", dict_aircraft=dict_aircraft)


@app.route("/passengers/")
def passengers():
    return render_template("passengers.html", len=len(dict_passengers), dict_passengers=dict_passengers)


@app.route("/passenger_info/<p_id>")
def passenger_info(p_id):
    return render_template("passenger_info.html", p_id=int(p_id), dict_passengers=dict_passengers, list_len=len(dict_passengers[int(p_id)].tickets))


@app.route("/passengers_new/", methods=["GET", "POST"])
def passengers_new():
    if request.method == "POST":
        try:
            p = Passenger().make_manual(request.form["firstname"], request.form["secondname"], request.form["age"], request.form["passport"], db_wrapper)
            dict_passengers[p.oid] = p
            return redirect(url_for("passengers"))
        except:
            return redirect(url_for("passengers_new"))
    return render_template("passengers_new.html")


@app.route("/passenger_sell_ticket/<p_id>", methods=["GET", "POST"])
def passenger_sell_ticket(p_id):

    if request.method == "POST":
        flight = dict_flights[int(request.form["flight"].split(" ")[0])]

        a_id = flight.aircraft

        if type(a_id) == Plane or type(a_id) == Helicopter:
            a_id = a_id.oid

        if flight.aircraft is not None:

            # If the amount of passengers taking up seats is equal to or less than the capacity of the plane assigned
            if flight.get_seated_passenger_count(db_wrapper) < dict_aircraft[a_id].flight_capacity:
                db_wrapper.create_ticket_and_add(dict_passengers[int(p_id)], flight)
                return redirect(url_for("passengers"))
            else:
                return redirect(url_for("error"))
        else:
            return redirect(url_for("error"))


    return render_template("passenger_sell_ticket.html", p_id=p_id, dict_flights=dict_flights)


@app.route("/error/")
def error():
    return render_template("error.html")

@app.route("/aircraft/")
def aircraft():
    return render_template("aircraft.html", len=len(dict_aircraft), dict_aircraft=dict_aircraft)


@app.route("/aircraft_info/<a_id>")
def aircraft_info(a_id):
    return render_template("aircraft_info.html", a_id=int(a_id), dict_aircraft=dict_aircraft)


@app.route("/aircraft_new/", methods=["GET", "POST"])
def aircraft_new():
    if request.method == "POST":
        try:
            if request.form["type"] == "plane":
                a = Plane().make_manual(False, request.form["capacity"], request.form["type"], db_wrapper)
            else:
                a = Helicopter().make_manual(False, request.form["capacity"],  request.form["type"], db_wrapper)

            dict_aircraft[a.oid] = a
            return redirect(url_for("aircraft"))
        except:
            return redirect(url_for("aircraft_new"))
    return render_template("aircraft_new.html")


@app.route("/aircraft_assign_to_flight/<a_id>",  methods=["GET", "POST"])
def aircraft_assign_to_flight(a_id):
    if request.method == "POST":
        try:
            aircraft_flight = dict_flights[int(request.form["flight"].split(" ")[0])]
            aircraft_obj = dict_aircraft[int(a_id.split(" ")[0])]
            aircraft_flight.assign_aircraft(aircraft_obj, db_wrapper)
            return redirect(url_for("aircraft"))
        except:
            return redirect(url_for("aircraft"))

    return render_template("aircraft_assign_to_flight.html", a_id=a_id, dict_flights=dict_flights)


@app.route("/staff/")
def staff():
    return render_template("staff.html", len=len(dict_staff), dict_staff=dict_staff)


@app.route("/staff_info/<staff_id>")
def staff_info(staff_id):

    return render_template("staff_info.html", staff_id=int(staff_id.split(" ")[0]), dict_staff=dict_staff)


@app.route("/staff_new/", methods=["GET", "POST"])
def staff_new():
    if request.method == "POST":
        try:
            s = Staff().make_manual(request.form["firstname"], request.form["secondname"], request.form["age"], db_wrapper)
            dict_staff[s.oid] = s
            return redirect(url_for("staff"))
        except:
            return redirect(url_for("staff_new"))
    return render_template("staff_new.html")


@app.route("/staff_assign_to_plane/<staff_id>",  methods=["GET", "POST"])
def staff_assign_to_plane(staff_id):
    if request.method == "POST":
        try:
            staff_flight = dict_flights[int(request.form["flight"].split(" ")[0])]
            staff_obj = dict_staff[int(staff_id.split(" ")[0])]
            staff_obj.assign_flight(staff_flight, db_wrapper)
            return redirect(url_for("staff"))
        except:
            return redirect(url_for("staff"))

    return render_template("staff_assign_to_plane.html", staff_id=staff_id, dict_flights=dict_flights)


if __name__ == '__main__':
    # Essential db loading code
    db_wrapper = DbWrapper()
    dict_passengers = db_wrapper.load_all_passengers()
    dict_flights = db_wrapper.load_all_flights(dict_passengers)
    dict_aircraft = db_wrapper.load_all_aircraft()
    dict_staff = db_wrapper.load_all_staff()

    app.run(host='0.0.0.0', debug=True)
