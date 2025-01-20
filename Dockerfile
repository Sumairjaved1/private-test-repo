# Step 1: Use an official Python runtime as a base image
FROM python:3.12.3

# Step 2: Set the working directory inside the container
WORKDIR /usr/src/app

# Step 3: Copy the necessary files into the container
# Copy the requirements.txt first so dependencies can be installed
COPY requirements.txt .

# Install Python dependencies (e.g., Flask) using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy static files (CSS and JS) into the appropriate directory inside the container
COPY static/css/styles.css ./static/css/
COPY static/js/app.js ./static/js/

# Copy template HTML files into the templates directory inside the container
COPY templates/index.html ./templates/
COPY templates/login.html ./templates/
COPY templates/view_items.html ./templates/
COPY templates/update_item.html ./templates/

# Step 4: Copy the rest of the application code into the container
COPY . .

# Step 5: Expose the port the app runs on
EXPOSE 80

# Step 6: Define the command to run the Flask app when the container starts
CMD ["python", "flask_server.py"]
