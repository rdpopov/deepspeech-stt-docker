from debian:buster
# initial updates and setup
RUN apt update && apt upgrade --yes && apt install bash curl sudo locales --yes 
RUN dpkg-reconfigure tzdata
RUN ln -sf /bin/bash /bin/sh
# Python and python accessories
RUN apt install --yes \ 
    python3 \
    portaudio19-dev \
    python3-pip \
    virtualenv


# python deep speech package install
RUN virtualenv -p python3 $HOME/deep-venv \
    && source $HOME/deep-venv/bin/activate \
    && pip3 install deepspeech

RUN cd /$HOME/deep-venv && curl -LO https://github.com/mozilla/DeepSpeech/releases/download/latest/deepspeech-0.9.3-models.pbmm
RUN cd /$HOME/deep-venv && curl -LO https://github.com/mozilla/DeepSpeech/releases/download/latest/deepspeech-0.9.3-models.scorer

