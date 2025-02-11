# Use an official Python runtime as a parent image
FROM python:3.7

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

RUN pip install -r requirements.txt