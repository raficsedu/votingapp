# pull official base image
FROM python:3

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# set work directory
WORKDIR /votingapp

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /votingapp/
RUN pip install -r requirements.txt

# copy project
COPY . /votingapp/