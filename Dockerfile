# image that you are going to inherit your dockerfile from.
# With Docker, we can build images on top of other images. The benefit is that we can find an image that has all the things we need to get started
# and then build on top of it.
# we can find the list of images on https://hub.docker.com
# there are tags for images. 

FROM python:3.7-alpine

# This is optional but useful to know who is maintaining the docker image
MAINTAINER Pritish Jadhav

# Setting PYTHONUNBUFFERED environment variable. 
# Tells python to run in unbuffered mode which is recommended while running python in a docker containers.
# This doesnt allow python to buffer the output. It just prints the output directly and this avoids some complications while running docker 
# image with python application. 
ENV PYTHONUNBUFFERED 1

# tells docker to copy the requirements.txt file from the directory adjacent to Dockerfile to the docker image.
COPY ./requirements.txt /requirements.txt

# Install dependencies.
RUN pip install -r /requirements.txt

# make a directory to store our application src code.
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# create a user for running the docker image
# -D indicates that the user is allowed to run applications only and not for creating directories.
RUN adduser -D user

# switch to the user. 
# If we dont create a user, the docker image will run using root and that may compromise security.
USER user

# running the docker image
# docker build .