
ARG PYTORCH="2.0.1"
ARG CUDA="11.7"
ARG CUDNN="8"

FROM pytorch/pytorch:${PYTORCH}-cuda${CUDA}-cudnn${CUDNN}-devel

# INIT OF FIX FOR GPG KEY -- Hopefully they will fix this soon
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
# END OF FIX FOR GPG KEY

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# apt and apt-get update
RUN apt-get update && apt update && apt upgrade -y && apt-get clean
# apt and apt-get installations
RUN apt install -y vim git unzip 
#    && apt-get install -y libosmesa6-dev build-essential libgl1-mesa-dev libglu1-mesa-dev freeglut3-dev

# Install dependencies from requirements.txt
COPY requirements.txt .
# RUN . /opt/conda/etc/profile.d/conda.sh \
#     && conda activate main \
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
#CMD ["pip", "install", "--no-cache-dir", "-r", "src/requirements.txt"]

# Install python 3.9
RUN apt-get update && apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get update && apt-get install -y python3.9 python3-pip 

# Install spotlight
# RUN . /opt/conda/etc/profile.d/conda.sh \
#     && conda activate main \
#     && conda install -c maciejkula -c pytorch spotlight
RUN git clone https://github.com/maciejkula/spotlight.git \
    && cd spotlight \
    && python3 setup.py build \
    && python3 setup.py install

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

WORKDIR /home/${USER_NAME}

# ENV CONDA_DIR /opt/conda
# ENV PATH $CONDA_DIR/bin:$PATH

# Create conda environment with python 3.6 and pytorch
# RUN  conda create -n main python=3.9 \
# 	&& . /opt/conda/etc/profile.d/conda.sh \
#     && conda activate main \
#     && conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia 

# RUN . /opt/conda/etc/profile.d/conda.sh \
#     && conda activate main \
#     && pip install streamlit==1.10
# #spotlight
# RUN . /opt/conda/etc/profile.d/conda.sh \
#     && conda activate main \
#     && pip install scikit-learn
# RUN . /opt/conda/etc/profile.d/conda.sh \
#     && conda activate main \
#     && pip install uvicorn
# RUN . /opt/conda/etc/profile.d/conda.sh \
#     && conda activate main \
#     && pip install httpx
# RUN . /opt/conda/etc/profile.d/conda.sh \
#     && conda activate main \
#     && pip install starlette
# RUN . /opt/conda/etc/profile.d/conda.sh \
#     && conda activate main \
#     && pip install pandas
# RUN . /opt/conda/etc/profile.d/conda.sh \
#     && conda activate main \
#     && pip install chardet
# RUN . /opt/conda/etc/profile.d/conda.sh \
#     && conda activate main \
#     && pip install urllib3
# RUN . /opt/conda/etc/profile.d/conda.sh \
#     && conda activate main \
#     && pip install h5py

# Install other dependencies
RUN sudo apt-get update && sudo apt update && sudo apt upgrade -y && sudo apt-get clean
RUN sudo apt update \
	&& sudo apt-get install -y tmux wget
RUN sudo DEBIAN_FRONTEND=noninteractive apt-get install libglib2.0-0 ffmpeg libsm6 libxext6 -y
RUN echo "export CUDA_HOME=/usr/local/cuda-11.7 && export PATH='/usr/local/cuda-11.7/bin:$PATH' && export CPATH='/usr/local/cuda-11.7/include:$CPATH' && export LD_LIBRARY_PATH='$LD_LIBRARY_PATH:/usr/local/cuda-11.7/lib64/'" > ~/.bashrc
RUN sudo apt-get install qt5-default -y

# Set the working directory in the container
ENV PROJECT_PATH=/home/${USER_NAME}/falcon_ml
WORKDIR $PROJECT_PATH