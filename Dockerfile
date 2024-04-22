# use an official python runtime as a parent image
FROM python:3.12-bullseye

# set the working directory in the container
WORKDIR /app

# copy the current directory contents into the container at /app
COPY . /app

# install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

# make port 8080 available to the world outside this container
EXPOSE 8080

# env variables
ENV USER_NAME=cc2024
ENV PASSWORD=lapinamk
ENV JWT_SECRET=GLKKEGJI25LKJL16762TFqQWv1p5vssleFEL215161AGGgegEEAGQPQ

# run app.py when container launches
CMD ["python", "app.py"]
