# Use Railway's Python 2.7 environment as the base
FROM railwayapp/python:2.7

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Specify the command to run on container start
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]