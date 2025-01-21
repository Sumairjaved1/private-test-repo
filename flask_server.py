from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import logging
import uuid
from datetime import timedelta
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)

# In-memory data store (for demonstration purposes)
data_store = {}

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Application configuration
app.secret_key = os.urandom(24)  # Change this to a secure key in production
app.permanent_session_lifetime = timedelta(minutes=30)  # Set session expiration time

# Dummy user credentials
USER_CREDENTIALS = {
    'admin': generate_password_hash('admin'),
    'user': generate_password_hash('user')
}

# Helper functions
def is_logged_in():
    """Check if the user is logged in."""
    return 'username' in session

# Routes

@app.route('/')
def home():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('index.html', title="Home")

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
            return render_template('login.html', error='Invalid username or password', title="Login")

    return render_template('login.html', title="Login")

@app.route('/view_items')
def view_items():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('view_items.html', items=data_store, title="View Items")

@app.route('/item/<item_id>', methods=['GET'])
def get_item(item_id):
    """Get item by ID."""
    item = data_store.get(item_id)
    if item:
        return jsonify({item_id: item}), 200
    return jsonify({"error": f"Item with ID {item_id} not found"}), 404

@app.route('/item/<item_id>/update', methods=['GET', 'POST'])
def update_item(item_id):
    """Update item by ID."""
    if request.method == 'POST':
        value = request.form.get('value')
        if not value:
            return jsonify({"error": "Missing 'value' in request data"}), 400
        if item_id not in data_store:
            return jsonify({"error": f"Item with ID {item_id} not found"}), 404
        data_store[item_id] = value
        return redirect(url_for('view_items'))

    item_value = data_store.get(item_id)
    if not item_value:
        return jsonify({"error": f"Item with ID {item_id} not found"}), 404
    return render_template('update_item.html', item_id=item_id, item_value=item_value, title="Update Item")

@app.route('/item/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete item by ID."""
    if item_id in data_store:
        del data_store[item_id]
        return jsonify({"message": f"Item with ID {item_id} deleted"}), 200
    return jsonify({"error": f"Item with ID {item_id} not found"}), 404

@app.route('/item/create', methods=['GET', 'POST'])
def create_item():
    """Create a new item."""
    if not is_logged_in():
        return redirect(url_for('login'))

    if request.method == 'POST':
        item_id = request.form.get('id')
        item_value = request.form.get('value')

        if not item_id or not item_value:
            return render_template('create_item.html', error="Both ID and Value are required", title="Create Item")

        if item_id in data_store:
            return render_template('create_item.html', error=f"Item with ID {item_id} already exists", title="Create Item")

        data_store[item_id] = item_value
        return redirect(url_for('view_items'))

    return render_template('create_item.html', title="Create Item")

@app.route('/logout', methods=['POST'])
def logout():
    """Logout the user and clear the session."""
    session.clear()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="Page Not Found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"Internal server error: {e}")
    return render_template('500.html', title="Server Error"), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
