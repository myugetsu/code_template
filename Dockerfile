# Use the official Python image with Alpine 3.18 as the base image
FROM python:3.10 as base

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn pymysql

# static folders
COPY app app
# COPY static static

COPY flask_new.py config.py .env boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP flask_new.py

EXPOSE 5000
FROM base as flask_new
CMD ["./boot.sh"]
