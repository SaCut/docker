# Plane Project containerisation with docker
- Creating the image with `docker build --tag savcut/plane_task:v1.0 .`
- Launching the image with `docker run -d -p 5000:5000 savcut/plane_task`

## To Run
### [run.py](run.py)
Command line interface program

### [app.py](app.py)
Flask based GUI program

### [login.py](login.py)
When run this enables you to create a new username and password

## Files and Functionality
### [abstract_db_record.py](abstract_db_record.py)
The base/parent class for all database objects.

### [app.py](app.py)
This handles which web pages should be served to the user. The web app is run from here.

### [db_wrapper.py](db_wrapper.py)
Manages the connection between the SQL database and Python code. Saving and loading to and from the database is handled here.

### [flight_trip.py](flight_trip.py)
An object. Each instance contains information about a flight, hence the name.

### [login.py](login.py)
Handles the staff login.

### [menus.py](menus.py)
Holds all the code used for displaying and handling the menus used in `run.py`. Created solely to keep `run.py` neat.

### [run.py](run.py)
This is the 'main' part of the programme from the user's perspective. This is where they interact with the UI (graphical or otherwise) to create and manage passengers, flights, and aircrafts.

### [test_plane_project.py](test_plane_project.py)
The unit tests are run from this file.

### [aircraft](./aircraft)
A package for all the aircraft classes.

[aircraft.py](./aircraft/aircraft.py) -
The parent class for all the aircraft classes.

[helicopter.py](./aircraft/helicopter.py) -
A child of `Aircraft`. It currently inherits all its properties.

[plane.py](./aircraft/plane.py) -
A child of `Aircraft`. It currently inherits all its properties and also extends them with the variable `plane_model`.

### [people](./people)
A package for all people classes.

[passenger.py](./people/passenger.py) -
A child of the `Person` class, specifically for passengers.

[people.py](./people/people.py) -
Holds the `Person` class. It's the parent for all people classes.

[staff.py](./people/staff.py) -
A child of the `Person` class, specifically for staff members.

### [static](./static)
A folder containing JS and CSS files.

[flight.css](./static/flight.css) -
The styling for the web UI lives here.

### [templates](./templates)
Holds the html files.

[aircraft_info.html](./templates/aircraft_info.html) -
The user can view an individual aircraft's info here.

[aircraft_new.html](./templates/aircraft_new.html) - 
The page for adding new aircrafts.

[aircraft.html](./templates/aircraft.html) -
Lists all the aircraft objects.

---

[base.html](./templates/base.html) -
The template for displaying the site navigation.

---

[flight_info.html](./templates/flight_info.html) - 
The user can view an individual flight's info here.

[flight_new.html](./templates/flight_new.html) -
The page for adding new flights.

[flight.html](./templates/flight.html) -
Displays flight information.

---

[home.html](./templates/home.html) - 
The home page for the web UI.

[login.html](./templates/login.html) -
Displays the login form.  

---

[passenger_info.html](./templates/passenger_info.html) -
The user can view an individual passenger's info here.

[passenger_new.html](./templates/passenger_new.html) -
The page for adding new passengers.

[passengers.html](./templates/passengers.html) -
Where the user can view all the passengers.

---

[staff_info.html](./templates/staff_info.html) -
The user can view an individual staff member's info here.

[staff_new.html](./templates/staff_new.html) - 
The page for adding new staff objects.

[staff.html](./templates/staff.html) - 
Displays all the staff objects in a list.