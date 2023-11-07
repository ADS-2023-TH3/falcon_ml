# Build the Docker image with $ docker build --no-cache -t app-dev-image .
# Run the docker image with $ docker run -it --name app-dev -p 4000:80 -v C:\Users\leob3\OneDrive\Desktop\Agile_Project\falcon_ml\src:/app app-dev-image 

# Use an official Python runtime as a parent image
FROM python:3.9

# Set up a volume to mount the local 'app/' folder into the container
VOLUME ["/falcon_ml/src"]

# Set the working directory in the container
WORKDIR /falcon_ml

# Expose the port your application will run on 
EXPOSE 80

# Install any additional dependencies you might need for development
#RUN apt-get update && apt-get install -y 

# Install dependencies from requirements.txt
RUN pip install --upgrade pip
CMD ["pip", "install", "--no-cache-dir", "-r", "src/requirements.txt"]