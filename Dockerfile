FROM python:3-alpine

RUN apt-get update && apt-get install -y --no-install-recommends --quiet \
        build-essential \
        curl \
        libfreetype6-dev \
        libhdf5-serial-dev \
        libpng12-dev \
        libzmq3-dev \
        pkg-config \
        rsync \
        software-properties-common \
        unzip \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD main.py /
ADD requirements.txt /
ADD VERSION /

RUN pip install -r requirements.txt
RUN rm requirements.txt

RUN pip --no-cache-dir install \
    https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.11.0-cp36-cp36m-linux_x86_64.whl

CMD [ "python", "./main.py" ]
