# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container (default port for Streamlit)
EXPOSE 8501

# Define command to run app
CMD ["streamlit", "run", "app.py"]
