from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory database
users = [
    {"id": 1, "name": "Alice", "age": 25},
    {"id": 2, "name": "Bob", "age": 30},
]

# Retrieve all users (GET)
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# Retrieve a single user by ID (GET)
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user is None:
        abort(404)  # Not Found
    return jsonify(user), 200

# Create a new user (POST)
@app.route('/users', methods=['POST'])
def create_user():
    if not request.json or not 'name' in request.json:
        abort(400)  # Bad Request
    new_user = {
        'id': users[-1]['id'] + 1 if users else 1,
        'name': request.json['name'],
        'age': request.json.get('age', 0)
    }
    users.append(new_user)
    return jsonify(new_user), 201  # Created

# Update an existing user (PUT)
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user is None:
        abort(404)  # Not Found
    if not request.json:
        abort(400)  # Bad Request
    user['name'] = request.json.get('name', user['name'])
    user['age'] = request.json.get('age', user['age'])
    return jsonify(user), 200  # OK

# Delete a user (DELETE)
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [user for user in users if user['id'] != user_id]
    return '', 204  # No Content

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)

