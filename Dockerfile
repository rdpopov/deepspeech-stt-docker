from debian:buster
# initial updates and setup
RUN apt update && apt upgrade --yes && apt install bash curl sudo locales --yes 
RUN dpkg-reconfigure tzdata
RUN ln -sf /bin/bash /bin/sh
# Python and python accessories
RUN apt install --yes \ 
    python3 \
    python3-pip \
    virtualenv


# python deep speech package install
RUN virtualenv -p python3 $HOME/deep-venv \
    && source $HOME/deep-venv/bin/activate \
    && pip3 install deepspeech

RUN cd /$HOME/deep-venv && curl -LO https://github.com/mozilla/DeepSpeech/releases/download/latest/deepspeech-0.9.3-models.pbmm
RUN cd /$HOME/deep-venv && curl -LO https://github.com/mozilla/DeepSpeech/releases/download/latest/deepspeech-0.9.3-models.scorer

8dd4159668fe dc3606cb755d 79629b20526e 23be32d1c7b3 c96309805422 2e27547c5324 b0ec4cd98c7b 63103af7f4ed e577a174e87c c7f43e208599 
