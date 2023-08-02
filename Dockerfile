FROM nvidia/cuda:11.3.1-base-ubuntu18.04

ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND noninteractive
ENV MPLLOCALFREETYPE 1


# https://github.com/NVIDIA/nvidia-docker/issues/1009#issuecomment-1181312052
RUN  rm /etc/apt/sources.list.d/cuda.list
RUN apt-get update --fix-missing && apt-get install -y \
    build-essential \
    git \
    wget \
    vim \
    curl \
    zip \
    zlib1g-dev \
    unzip \
    pkg-config \
    libgl-dev \
    libblas-dev \
    liblapack-dev \
    python3-tk \
    python3-wheel \
    graphviz \
    libhdf5-dev \
    python3.8 \
    python3.8-dev \
    python3.8-distutils \
    swig \
    apt-transport-https \
    lsb-release \
    libpng-dev \
    ca-certificates &&\
    # obtain latest of nodejs
    curl --insecure -sL https://deb.nodesource.com/setup_12.x | bash - &&\
    apt install -y nodejs &&\
    apt-get clean &&\
    ln -s /usr/bin/python3.8 /usr/local/bin/python &&\
    ln -s /usr/bin/python3.8 /usr/local/bin/python3 &&\
    curl --insecure https://bootstrap.pypa.io/get-pip.py -o get-pip.py &&\
    python3 get-pip.py &&\
    rm get-pip.py &&\
    # best practice to keep the Docker image lean
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN wget https://github.com/baudm/parseq/releases/download/v1.0.0/parseq-bb5792a6.pt --no-check-certificate

RUN mkdir -p /root/.cache/torch/hub/checkpoints && cp parseq-bb5792a6.pt /root/.cache/torch/hub/checkpoints/parseq-bb5792a6.pt

WORKDIR app/


COPY requirements.txt .

RUN  pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 8000
ENV FLASK_APP main.py

EXPOSE 8000

#CMD ["python", "main.py"]
CMD ["flask", "run", "--host", "0.0.0.0"]
