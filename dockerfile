# Use a specific base image
FROM python:3.11-slim

# Create a non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Change ownership of the /app directory
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER 10001

# Expose the port (use the port you're running Flask on)
EXPOSE 8080

# Run the command to start your Flask app
CMD ["python", "app.py"]
