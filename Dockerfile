# set base image (host OS)
FROM python:3.9

# set the working directory in the container
WORKDIR /code

# copy the content of the local src directory to the working directory
COPY . /code

# install dependencies
RUN pip install aiogram requests


# command to run on container start
CMD [ "python", "./main.py" ]