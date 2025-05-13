from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for reservations
reservations = []

# Reserve a seat
@app.route('/reserve', methods=['POST'])
def reserve():
    data = request.get_json()
    name = data.get('name')
    passenger_id = data.get('id')
    age = data.get('age')
    priority = data.get('priority', 0)

    # Check if the passenger ID already exists
    for reservation in reservations:
        if reservation['id'] == passenger_id:
            return jsonify({
                'message': 'Reservation failed! Passenger ID already exists.'
            }), 400

    # Create a new reservation
    reservation = {
        'name': name,
        'id': passenger_id,
        'age': age,
        'priority': priority
    }

    # Add reservation to in-memory storage
    reservations.append(reservation)

    return jsonify({
        'message': 'Reservation successful!',
        'reservation': reservation
    }), 201

# Cancel a reservation
@app.route('/cancel', methods=['POST'])
def cancel():
    data = request.get_json()
    pid = data.get('id')

    # Find and remove the reservation by ID
    reservation_to_remove = None
    for reservation in reservations:
        if reservation['id'] == pid:
            reservation_to_remove = reservation
            break

    if reservation_to_remove:
        reservations.remove(reservation_to_remove)
        return jsonify({
            'message': 'Reservation cancelled successfully!',
            'reservation': reservation_to_remove
        })
    else:
        return jsonify({
            'message': 'Reservation not found! Cancellation failed.'
        }), 404

# Get reservation status
@app.route('/status', methods=['GET'])
def status():
    if len(reservations) == 0:
        return jsonify({
            'message': 'No reservations found.'
        })
    return jsonify({
        'message': 'Current reservations:',
        'reservations': reservations
    })

if __name__ == '__main__':
    app.run(debug=True)
