# Build the Docker image with $ docker build --no-cache -t app-dev-image .
# Run the docker image with $ docker run -it --name app-dev -p 4000:80 -v C:\Users\leob3\OneDrive\Desktop\Agile_Project\falcon_ml\src:/app app-dev-image 

# Build an ubuntu 22.04 image
FROM ubuntu:22.04

# Install python 3.9
RUN apt-get update && apt-get install -y python3.9 python3-pip

# ---------------- USER SETTING ------------------
# Add the current user to the image. Use 'id' command to find your own
ARG USER_NAME=user
ARG USER_ID=12345
ARG GROUP_NAME=falcon
ARG GROUP_ID=67890

# Update the system and install required packages
RUN apt-get update && apt-get install -y sudo

# Create a new group with the same GID as the host
RUN groupadd --gid $GROUP_ID $GROUP_NAME

# Create a new user with the same UID and GID as the host
RUN useradd --uid $USER_ID --gid $GROUP_ID --shell /bin/bash --create-home $USER_NAME

# don't require password with sudo, for convenience
# not the safest thing to do, but hopefully okay inside the container
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Add the new user to the sudo group
RUN usermod -aG sudo $USER_NAME

# Set the default user to the new user
USER $USER_NAME

# -------------- END USER SETTINGS --------------

# Expose the port your application will run on 
EXPOSE 80

# Install any additional dependencies you might need for development
RUN sudo apt-get update && sudo apt-get install git -y

# Install dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
#CMD ["pip", "install", "--no-cache-dir", "-r", "src/requirements.txt"]

# Set the working directory in the container
WORKDIR /home/user/falcon_ml/