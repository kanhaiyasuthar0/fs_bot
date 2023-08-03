# FROM node:18.16.1
# WORKDIR /app
# COPY package.json package.json
# COPY package-lock.json package-lock.json
# RUN npm install
# COPY . .
# CMD [ "npm", "start" ]

# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install -r requirements.txt

# Run your Python script when the container launches
CMD ["python3", "bot.py"]
