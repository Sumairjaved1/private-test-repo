from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import logging
import uuid
from datetime import timedelta
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# In-memory data store (for demonstration purposes)
data_store = {}


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
session.permanent = True

# Secret key for session management (change this to a secure key in production)
app.secret_key = os.urandom(24)

# Set session to expire after a certain time
app.permanent_session_lifetime = timedelta(minutes=30)  # Set session lifetime to 30 minutes

# Dummy credentials (hashed for demo purposes)
USER_CREDENTIALS = {
    'admin': generate_password_hash('admin'),
    'user': generate_password_hash('user')
}

if not item_id:
    return jsonify({"error": "Invalid item ID"}), 400

# Helper function to check session
def is_logged_in():
    return 'username' in session

# Home route
@app.route('/')
def home():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('index.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USER_CREDENTIALS and check_password_hash(USER_CREDENTIALS[username], password):
            session['username'] = username
            session['session_id'] = str(uuid.uuid4())
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

# View Items route
@app.route('/view_items')
def view_items():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('view_items.html', items=data_store)


# GET Item by ID route
@app.route('/item/<item_id>', methods=['GET'])
def get_item(item_id):
    item = data_store.get(item_id)
    if item:
        return jsonify({item_id: item}), 200
    else:
        return jsonify({"error": f"Item with ID {item_id} not found"}), 404

# Update Item by ID route
@app.route('/item/<item_id>/update', methods=['GET', 'POST'])
def update_item(item_id):
    if request.method == 'POST':
        value = request.form.get('value')  # Use form data for POST request
        if not value:
            return jsonify({"error": "Missing 'value' in request data"}), 400
        if item_id not in data_store:
            return jsonify({"error": f"Item with ID {item_id} not found"}), 404
        data_store[item_id] = value
        return redirect(url_for('view_items'))  # Redirect to view items after update

    # If it's GET request, render the update form
    item_value = data_store.get(item_id)
    if not item_value:
        return jsonify({"error": f"Item with ID {item_id} not found"}), 404
    return render_template('update_item.html', item_id=item_id, item_value=item_value)

# Delete Item route
@app.route('/item/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id in data_store:
        del data_store[item_id]
        return jsonify({"message": f"Item with ID {item_id} deleted"}), 200
    else:
        return jsonify({"error": f"Item with ID {item_id} not found"}), 404

# Logout route
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))
    
@app.route('/item/<item_id>', methods=['POST'])
def delete_item(item_id):
    if request.form.get('_method') == 'DELETE':
        if item_id in data_store:
            del data_store[item_id]
            return jsonify({"message": f"Item with ID {item_id} deleted"}), 200
        else:
            return jsonify({"error": f"Item with ID {item_id} not found"}), 404
    return jsonify({"error": "Invalid method"}), 405

# Create Item via GET method
@app.route('/item/create', methods=['GET', 'POST'])
def create_item_get():
    if not is_logged_in():
        return redirect(url_for('login'))

    if request.method == 'POST':
        item_id = request.form.get('id')
        item_value = request.form.get('value')

        if not item_id or not item_value:
            return render_template('create_item.html', error="Both ID and Value are required")

        if item_id in data_store:
            return render_template('create_item.html', error=f"Item with ID {item_id} already exists")

        data_store[item_id] = item_value
        return redirect(url_for('view_items'))

    return render_template('create_item.html')

# Custom error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"Internal server error: {e}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
