# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Create a rootless user with UID 1000 and add to the system
RUN useradd -m -u 1000 tictactoe

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Change ownership of the application files to the rootless user
RUN chown -R tictactoe:tictactoe /app

# Install any needed packages (installing as root)
RUN pip install flask

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Switch to the rootless user and run the application
USER tictactoe

# Run app.py when the container launches
CMD ["python", "app.py"]
