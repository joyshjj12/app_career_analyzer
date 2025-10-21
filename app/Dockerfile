# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port the app runs on (Flask's default)
EXPOSE 5000

# Command to run the application using gunicorn (a production WSGI server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "300", "app:app"]