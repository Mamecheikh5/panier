# Use an official Python runtime as a parent image
FROM python:3.8.3-slim-buster

COPY . /app

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
#EXPOSE 80

#RUN chmod +x /app/docker-entrypoint.sh

# Run app.py when the container launches
CMD ["gunicorn", "main:app"]
#ENTRYPOINT ["./docker-compose.sh"]

