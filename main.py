from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'your_secret_key_here'  # Replace with a secret key for session management
db = SQLAlchemy(app)
CORS(app)  # Enable CORS for all routes

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Define routes for authentication, user management, and logout

@app.route('/users/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid username or password"}), 401

    # Set user_id in session for session management
    session['user_id'] = user.id

    return jsonify({"message": "Login successful"})

@app.route('/users/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')

    if not username or not password or not first_name or not last_name:
        return jsonify({"message": "All fields are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, first_name=first_name, last_name=last_name)

    with app.app_context():
        db.session.add(new_user)
        db.session.commit()

    return jsonify({"message": "Registration successful"}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append(basic_details(user))
    return jsonify(user_list)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(basic_details(user))
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        data = request.get_json()
        if 'password' in data:
            del data['password']  # Do not update password directly

        for key, value in data.items():
            setattr(user, key, value)

        with app.app_context():
            db.session.commit()

        logging.info(f"User with ID {user_id} updated successfully")

        return jsonify({"message": "User updated successfully"})

    except Exception as e:
        logging.error(f"Error updating user with ID {user_id}: {str(e)}")
        return jsonify({"message": "An error occurred while updating the user"}), 500


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"message": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        
        logging.info(f"User with ID {user_id} deleted successfully")

        return jsonify({"message": "User deleted successfully"})

    except Exception as e:
        logging.error(f"Error deleting user with ID {user_id}: {str(e)}")
        return jsonify({"message": "An error occurred while deleting the user"}), 500


# Logout route to clear session data
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logout successful"})

# Helper function to return basic user details
def basic_details(user):
    return {
        "id": user.id,
        "username": user.username,
        "firstName": user.first_name,
        "lastName": user.last_name
    }

if __name__ == '__main__':
    app.run(debug=True)
