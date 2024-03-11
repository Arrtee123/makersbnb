import os
from flask import Flask, request, render_template, redirect, session
from flask_session import Session
from lib.user_repository import UserRepository
from lib.user import User
from lib.space_repository import SpaceRepository
from lib.space import Space
from lib.availability_repository import AvailabilityRepository
from lib.booking_repository import BookingRepository
from lib.user_booking_repository import UserBookingRepository
from lib.user_booking import UserBooking
from lib.database_connection import get_flask_database_connection

# Create a new Flask app
app = Flask(__name__)

app.secret_key = "i'm a magical cookie key"
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5000/index
@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def validate_login():
    if request.method == 'GET':
        return render_template('login.html')
    connection = get_flask_database_connection(app)
    repo = UserRepository(connection)
    name = request.form['name']
    password = request.form['password']
    user_id = repo.get_user_id(name)
    if repo.find(name, password):
        session['logged_in'] = True
        session['name'] = name
        return redirect("user/{}".format(user_id))
    return render_template("login.html")

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        connection = get_flask_database_connection(app)
        repo = UserRepository(connection)
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if not name or not email or not password:
            errors = "All fields are required."
            return render_template("sign_up.html", errors=errors)
        
        new_user = User(id=None, name=name, email=email, password=password)
        created_user = repo.create(new_user)

        if created_user:
            return redirect("/spaces", code=302)
        else:
            return render_template("sign_up.html")
        
    else:
        return render_template("sign_up.html")
        
#Commented out the below, as it's not for Minimum Viable Product. 
#AND.. I can't get it to play nice

# def check_user_exists():
#     connection = get_flask_database_connection(app)
#     repo = UserRepository(connection)
#     name = request.form['name']
#     email = request.form['email']
#     password = request.form['password']
#     if repo.find(name, email, password):
#         return render_template("sign_up.html")
#     return render_template("spaces.html")

@app.route('/spaces', methods=['GET'])
def get_spaces():
    connection = get_flask_database_connection(app)
    repo = SpaceRepository(connection)
    spaces = repo.all()
    return render_template("spaces.html", spaces=spaces)
    session['user_id'] = id



@app.route('/spaces/new', methods=['POST', 'GET'])
def create_space():
    if request.method == 'GET':
        return render_template("new_space.html")
    connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(connection)
    avail_repo = AvailabilityRepository(connection)
    name = request.form['name']
    price = request.form['price']
    description = request.form['description']
    user_id = request.form['user_id']
    availability_from = request.form['availability_from']
    availability_to = request.form['availability_to']
    space_repo.create(name, price, description, user_id)
    space = space_repo.all()[-1]
    avail_repo.create(availability_from, availability_to, space.id)
    return redirect("/spaces")

@app.route('/spaces/<int:id>', methods=['GET', 'POST'])
def get_individual_space(id):
    connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(connection)
    avail_repo = AvailabilityRepository(connection)
    booking_repo = BookingRepository(connection)
    if request.method == 'GET':
        space = space_repo.find(id)
        availabilities = avail_repo.find_space(id)
        return render_template("space_show.html", space=space, availabilities=availabilities, space_id=id)

    booking_from = request.form['booking_from']
    booking_to = request.form['booking_to']
    bookers_id = request.form['bookers_id']
    booking_repo.create(booking_from, booking_to, bookers_id, id)
    return redirect("/spaces")

@app.route('/user/<int:id>', methods=['GET', 'POST'])
def get_single_user(id):
        connection = get_flask_database_connection(app)
        user_repository = UserRepository(connection)
        space_repository = SpaceRepository(connection)
        booking_repository = BookingRepository(connection)
        user_booking_repository = UserBookingRepository(connection)

        userrequests = user_booking_repository.find_user_requests(id)

        if request.method == 'POST':  # Check for POST request (delete action)
            space_id = request.form.get('space_id')
            if space_id:  # Ensure space_id is present in form data
                # try:
                space_repository.delete(space_id)
                #     flash("Space deleted successfully!", "success")
                # except Exception as e:
                #     flash(f"Error deleting space: {e}", "error")
            booking_id = request.form.get('booking_id')
            if booking_id:
                booking_repository.accept_booking(booking_id)
                
        user = user_repository.user_details(id)
        spaces = space_repository.find_user_spaces(id)
        userbookings = user_booking_repository.find_user_bookings(id)
        
    
       
        session['user_id'] = id

        return render_template('user_homepage.html', user=user, spaces=spaces, userrequests=userrequests, userbookings=userbookings)


@app.route('/bookings', methods=['GET'])
def get_bookings_new():
    return render_template("bookings.html")


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
