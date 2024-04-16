# Use an official lightweight Python image.
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

# Copy just the requirements.txt file initially
COPY requirements.txt ./

# Copy the WHL directory containing Python wheel (.whl) files
COPY whl ./whl

# Install any needed packages specified in requirements.txt, including those in the WHL directory
RUN pip3 install --no-cache-dir -r requirements.txt --find-links ./whl

# Copy the rest of your application's source code
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define the command to run your app using gunicorn
ENTRYPOINT ["gunicorn", "-c", "gunicorn.conf.py", "api.app:app"]
