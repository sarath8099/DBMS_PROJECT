from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import String
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import urllib.parse

db_username = 'root'
db_password = 'MSrao@2002'
db_host = 'localhost'  
db_port = '3306'  
db_name = 'tourism_recommender'  


encoded_password = urllib.parse.quote_plus(db_password)
db_uri = f"mysql://{db_username}:{encoded_password}@{db_host}:{db_port}/{db_name}"

app = Flask(__name__, template_folder='TEMPLETS',static_folder='static')


app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


with app.app_context():
    try:
        # Try to establish a connection
        db.engine.connect()
        print("Connected to MySQL database successfully")
    except Exception as e:
        print("Error connecting to the database:", e)




print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])
print("Connected to MySQL database successfully")
print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])


@app.route('/')
def landing_page():
    return render_template('index.html')

@app.route('/signup')
def show_signup():
    return render_template('signup.html')

@app.route('/login')
def show_login():
    return render_template('login.html')
@app.route('/submit_review')
def show_submit_review():
    return render_template('submit_review.html')





class users(db.Model):
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    FirstName = db.Column(db.String(255))
    LastName = db.Column(db.String(255))
    Username = db.Column(db.String(255), unique=True, nullable=False)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    PhoneNumber = db.Column(db.String(20))
    Country = db.Column(db.String(45))

    def set_password(self, password):
        self.Password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Password, password)

class userpreference(db.Model):
    PreferenceID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    DestinationType = db.Column(db.String(255))
    TravelDuration = db.Column(db.String(45))


class user_interest(db.Model):
    UserInterestID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    ActivityID = db.Column(db.Integer)
    IsFavorite = db.Column(db.Boolean)


class travelhistory(db.Model):
    TravelID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    DestinationID = db.Column(db.Integer)
    TravelDate = db.Column(db.Date)


class rating(db.Model):
    RatingID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    DestinationID = db.Column(db.Integer)
    Rating = db.Column(db.Integer)
    Review = db.Column(db.Text)
    Timestamp = db.Column(db.TIMESTAMP)


class destinations_activities(db.Model):
    DestinationActivityID = db.Column(db.Integer, primary_key=True)
    DestinationID = db.Column(db.Integer, db.ForeignKey('destination.DestinationID'))
    ActivityID = db.Column(db.Integer, db.ForeignKey('activity.ActivityID'))
    Duration = db.Column(db.String(45))


class destinations(db.Model):
    DestinationID = db.Column(db.Integer, primary_key=True)
    DestinationName = db.Column(db.String(255))
    Location = db.Column(db.String(255))
    Description = db.Column(db.Text)
    Type = db.Column(db.String(255))
    NumRatings = db.Column(db.Integer)
    PhoneNumber = db.Column(db.String(20))
    Email = db.Column(db.String(255))


class activities(db.Model):
    ActivityID = db.Column(db.Integer, primary_key=True)
    ActivityName = db.Column(db.String(45))
    Description = db.Column(db.Text)
    Category = db.Column(db.String(255))
    Duration = db.Column(db.String(45))


    def set_password(self, password):
        self.Password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Password, password)



@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone_number = data.get('phone_number')
    country = data.get('country')

    if not username or not email or not password:
        return jsonify({'message': 'Username, email, and password are required'}), 400

    if users.query.filter_by(Username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    # Check if email is already registered
    if users.query.filter_by(Email=email).first():
        return jsonify({'message': 'Email already registered'}), 400

    # Create a new User object and insert into the database
    new_user = users(Username=username, Email=email, FirstName=first_name, LastName=last_name, PhoneNumber=phone_number, Country=country)
    new_user.set_password(password)  # Hash and set the password
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully', 'user_id': new_user.UserID}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = users.query.filter_by(Email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid email or password'}), 401

    # Here you can generate a JWT token for authentication if needed

    return jsonify({'message': 'Login successful'}), 200



@app.route('/search/destinations', methods=['GET'])
def search_destinations():
    # Retrieve search criteria from query parameters
    location = request.args.get('location')
    destination_type = request.args.get('destination_type')

    # Perform database query to search for destinations based on criteria
    if location:
        # Search by location
        destinations = destinations.query.filter(destinations.Location.ilike(f'%{location}%')).all()
    elif destination_type:
        # Search by destination type
        destinations = destinations.query.filter(destinations.Type.ilike(f'%{destination_type}%')).all()
    else:
        # No criteria specified, return all destinations
        destinations = destinations.query.all()

    # Serialize the results to JSON
    result = []
    for destination in destinations:
        result.append({
            'DestinationID': destination.DestinationID,
            'DestinationName': destination.DestinationName,
            'Location': destination.Location,
            'Description': destination.Description,
            'Type': destination.Type,
            'NumRatings': destination.NumRatings,
            'PhoneNumber': destination.PhoneNumber,
            'Email': destination.Email
        })

    # Return the search results
    return jsonify({'destinations': result})


@app.route('/filter/activities', methods=['GET'])
def filter_activities():
    category = request.args.get('category')
    if category:
        activities = activities.query.filter(activities.Category == category).all()
    else:
        activities = activities.query.all()

    # Serialize the activities into JSON format
    result = []
    for activity in activities:
        result.append({
            'ActivityID': activity.ActivityID,
            'ActivityName': activity.ActivityName,
            'Description': activity.Description,
            'Category': activity.Category,
            'Duration': activity.Duration
        })

    # Return the filtered activities
    return jsonify({'activities': result})


@app.route('/destinations/<int:destination_id>', methods=['GET'])
def get_destination_details(destination_id):
    
    destination = destinations.query.get(destination_id)
    if not destination:
        return jsonify({'message': 'Destination not found'}), 404

    # Fetch activities associated with the destination
    destination_activities = destinations_activities.query.filter_by(DestinationID=destination_id).all()
    activities = []
    for da in destination_activities:
        activity = activities.query.get(da.ActivityID)
        if activity:
            activities.append({
                'ActivityID': activity.ActivityID,
                'ActivityName': activity.ActivityName,
                'Description': activity.Description,
                'Category': activity.Category,
                'Duration': activity.Duration
            })

    # Serialize the destination details into JSON format
    destination_details = {
        'DestinationID': destination.DestinationID,
        'DestinationName': destination.DestinationName,
        'Location': destination.Location,
        'Description': destination.Description,
        'Type': destination.Type,
        'NumRatings': destination.NumRatings,
        'PhoneNumber': destination.PhoneNumber,
        'Email': destination.Email,
        'Activities': activities
    }

    return jsonify(destination_details)

@app.route('/activities/<int:activity_id>', methods=['GET'])
def get_activity_details(activity_id):
    # Fetch details of a specific activity including user ratings and reviews from the database
    activity = activities.query.get(activity_id)
    if not activity:
        return jsonify({'message': 'Activity not found'}), 404

    # Fetch user ratings and reviews for the activity
    ratings = rating.query.filter_by(ActivityID=activity_id).all()
    reviews = []
    for rating in ratings:
        reviews.append({
            'UserID': rating.UserID,
            'Rating': rating.Rating,
            'Review': rating.Review,
            'Timestamp': rating.Timestamp
        })

    # Serialize activity details and reviews into JSON format
    activity_details = {
        'ActivityID': activity.ActivityID,
        'ActivityName': activity.ActivityName,
        'Description': activity.Description,
        'Category': activity.Category,
        'Duration': activity.Duration,
        'Reviews': reviews
    }

    return jsonify(activity_details)

from flask import jsonify, request

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    # Check if user_id is present in the request
    user_id = request.args.get('user_id')

    if user_id:
        
        user_favorite_activities = user_interest.query.filter_by(UserID=user_id, IsFavorite=True).all()
        favorite_activity_ids = [interest.ActivityID for interest in user_favorite_activities]

        # Example: Fetch top-rated destinations based on user ratings
        top_rated_destinations = db.session.query(
            destinations,
            func.avg(rating.Rating).label('average_rating')
        ).join(
            travelhistory, destinations.DestinationID == travelhistory.DestinationID
        ).join(
            rating, destinations.DestinationID == rating.DestinationID
        ).filter(
            travelhistory.UserID == user_id
        ).group_by(
            destinations.DestinationID
        ).order_by(
            func.avg(rating.Rating).desc()
        ).limit(5).all()

        # Combine recommendations from favorite activities and top-rated destinations
        recommended_destinations = []
        for destination, average_rating in top_rated_destinations:
            recommended_destinations.append({
                'DestinationID': destination.DestinationID,
                'DestinationName': destination.DestinationName,
                'Location': destination.Location,
                'Description': destination.Description,
                'Type': destination.Type,
                'NumRatings': destination.NumRatings,
                'PhoneNumber': destination.PhoneNumber,
                'Email': destination.Email,
                'AverageRating': average_rating
            })

        return jsonify({'recommended_destinations': recommended_destinations})
    else:
        # User ID is not present, return generic recommendations
        # Example: Return a list of popular destinations
        popular_destinations = destinations.query.order_by(destinations.NumRatings.desc()).limit(5).all()

        recommended_destinations = []
        for destination in popular_destinations:
            recommended_destinations.append({
                'DestinationID': destination.DestinationID,
                'DestinationName': destination.DestinationName,
                'Location': destination.Location,
                'Description': destination.Description,
                'Type': destination.Type,
                'NumRatings': destination.NumRatings,
                'PhoneNumber': destination.PhoneNumber,
                'Email': destination.Email
            })

        return jsonify({'recommended_destinations': recommended_destinations})


@app.route('/bookings', methods=['POST'])
def handle_bookings():
    data = request.json
    user_id = data.get('user_id')
    destination_id = data.get('destination_id')
    activity_id = data.get('activity_id')
    # You might also get additional booking information such as dates, quantities, etc. from the request

    if not user_id:
        return jsonify({'error': 'User ID is required for booking'}), 400

    if not destination_id and not activity_id:
        return jsonify({'error': 'Either Destination ID or Activity ID is required for booking'}), 400

    # Perform database operations to record the booking
    try:
        # Insert the booking details into the bookings table
        query = """
        INSERT INTO bookings (user_id, destination_id, activity_id)
        VALUES (:user_id, :destination_id, :activity_id)
        """
        db.session.execute(query, {'user_id': user_id, 'destination_id': destination_id, 'activity_id': activity_id})
        db.session.commit()

        # For demonstration, just returning a confirmation message
        return jsonify({'message': 'Booking confirmed for User ID {}'.format(user_id)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500





@app.route('/submit_review/destination', methods=['POST'])
def submit_destination_review():
    data = request.json
    user_id = data.get('user_id')
    destination_id = data.get('destination_id')
    rating = data.get('rating')
    review_text = data.get('review_text')

    if not destination_id or not rating:
        return jsonify({'error': 'Destination ID and rating are required'}), 400

    if user_id:
        # Check if the user exists
        existing_user = users.query.get(user_id)
        if not existing_user:
            return jsonify({'error': 'User does not exist'}), 404

    # Check if the user has already reviewed the destination
    existing_review = db.session.query(db.exists().where((db.text("UserID=:user_id AND DestinationID=:destination_id")).bindparams(user_id=user_id, destination_id=destination_id))).scalar()

    # If the user has already reviewed the destination, update the existing review
    if existing_review:
        query = """
        UPDATE reviews
        SET Rating = :rating, ReviewText = :review_text
        WHERE UserID = :user_id AND DestinationID = :destination_id
        """
    else:
        # Otherwise, insert a new review
        query = """
        INSERT INTO reviews (UserID, DestinationID, Rating, ReviewText)
        VALUES (:user_id, :destination_id, :rating, :review_text)
        """

    try:
        db.session.execute(query, {'user_id': user_id, 'destination_id': destination_id, 'rating': rating, 'review_text': review_text})
        db.session.commit()
        return jsonify({'message': 'Review submitted for destination!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500



@app.route('/submit_review/activity', methods=['POST'])
def submit_activity_review():
    # Handle review submissions for activities
    # Allow users to submit reviews and ratings for activities
    # Return confirmation or error messages

    # Extract review data from the request
    data = request.json
    user_id = data.get('user_id')  # Assuming user ID is provided in the request data
    activity_id = data.get('activity_id')
    rating = data.get('rating')
    review_text = data.get('review_text')

    # Check if all required fields are present
    if not user_id or not activity_id or not rating:
        return jsonify({'error': 'User ID, activity ID, and rating are required'}), 400

    # Check if the user exists
    existing_user = users.query.get(user_id)

    # If the user does not exist, create a new user
    if not existing_user:
        # Assuming user details are provided in the request (e.g., username, email)
        new_user = users(**data.get('user_details'))
        db.session.add(new_user)
        db.session.commit()
        user_id = new_user.id  # Update user ID to the newly created user's ID

    # Execute SQL query to insert the review into the database
    query = """
    INSERT INTO activity_reviews (UserID, ActivityID, Rating, ReviewText)
    VALUES (:user_id, :activity_id, :rating, :review_text)
    """
    try:
        db.session.execute(query, {'user_id': user_id, 'activity_id': activity_id, 'rating': rating, 'review_text': review_text})
        db.session.commit()
        return jsonify({'message': 'Review submitted for activity!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
