// Function to handle user signup
function signUp() {
    var userData = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        first_name: document.getElementById('first_name').value,
        last_name: document.getElementById('last_name').value,
        phone_number: document.getElementById('phone_number').value,
        country: document.getElementById('country').value
    };

    // Send a POST request to the /signup endpoint
    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData) // Convert data to JSON string
    })
    .then(response => response.json())
    .then(data => {
        // Handle response from the server
        console.log(data.message);
        // Redirect or show success message
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
// Function to handle user login
function login() {
    var userData = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };

    // Send a POST request to the /login endpoint with JSON data
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'  // Specify JSON content type
        },
        body: JSON.stringify(userData)  // Convert userData object to JSON string
    })
    .then(response => response.json())
    .then(data => {
        // Handle response from the server
        console.log(data.message);
        // Redirect or show success message
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
// Function to search destinations
function searchDestinations() {
    var location = document.getElementById('location').value;
    var destinationType = document.getElementById('destination_type').value;

    // Send a GET request to the /search/destinations endpoint with query parameters
    fetch(`/search/destinations?location=${location}&destination_type=${destinationType}`)
    .then(response => response.json())
    .then(data => {
        // Handle response from the server
        console.log(data.destinations);
        // Display search results on the frontend
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to filter activities
function filterActivities(category) {
    // Send a GET request to the /filter/activities endpoint with category as a query parameter
    fetch(`/filter/activities?category=${category}`)
    .then(response => response.json())
    .then(data => {
        // Handle response from the server
        console.log(data.activities);
        // Display filtered activities on the frontend
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to get recommendations
function getRecommendations(userId = null) {
    var url = '/recommendations';
    if (userId) {
        url += `?user_id=${userId}`;
    }

    // Send a GET request to the /recommendations endpoint
    fetch(url)
    .then(response => response.json())
    .then(data => {
        // Handle response from the server
        console.log(data.recommended_destinations);
        // Display recommendations on the frontend
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to handle bookings
function handleBookings(userId, destinationId = null, activityId = null) {
    var bookingData = { user_id: userId };
    if (destinationId) {
        bookingData.destination_id = destinationId;
    }
    if (activityId) {
        bookingData.activity_id = activityId;
    }

    // Send a POST request to the /bookings endpoint
    fetch('/bookings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(bookingData)
    })
    .then(response => response.json())
    .then(data => {
        // Handle response from the server
        console.log(data.message);
        // Show success message or handle accordingly
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to submit review for a destination
function submitDestinationReview() {
    var reviewData = {
        user_id: 123, // Replace with actual user ID
        destination_id: 456, // Replace with actual destination ID
        rating: 4, // Replace with user's rating
        review_text: 'Great destination!' // Replace with user's review
    };

    // Send a POST request to the /submit_review/destination endpoint
    fetch('/submit_review/destination', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(reviewData)
    })
    .then(response => response.json())
    .then(data => {
        // Handle response from the server
        console.log(data.message);
        // Show success message or handle accordingly
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to submit review for an activity
function submitActivityReview() {
    var reviewData = {
        user_id: 123, // Replace with actual user ID
        activity_id: 789, // Replace with actual activity ID
        rating: 5, // Replace with user's rating
        review_text: 'Awesome activity!' // Replace with user's review
    };

    // Send a POST request to the /submit_review/activity endpoint
    fetch('/submit_review/activity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(reviewData)
    })
    .then(response => response.json())
    .then(data => {
        // Handle response from the server
        console.log(data.message);
        // Show success message or handle accordingly
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
