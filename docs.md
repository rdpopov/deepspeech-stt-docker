# Creation
[DeepSpeech](https://github.com/mozilla/DeepSpeech)
[deepspeech docs](https://deepspeech.readthedocs.io/en/r0.9/?badge=latest)

## Initial docker setup
We build a debian docker image with. We use an older version of debian as
default python version is 3.7 and deepspeech needs 3.7-3.9 

``` dockerfile
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
```

## Sitting up deep speech
``` dockerfile
# python deep speech package install
RUN virtualenv -p python3 $HOME/deep-venv \
    && source $HOME/deep-venv/bin/activate \
    && pip3 install deepspeech
```

## Setting up models needed for the actual speech processing

We are going to pout them in the virtual environment for now as it it kind of
like the root for the project, so might as well be in one place.

``` dockerfile
RUN cd /$HOME/deep-venv && curl -LO https://github.com/mozilla/DeepSpeech/releases/download/latest/deepspeech-0.9.3-models.pbmm
RUN cd /$HOME/deep-venv && curl -LO https://github.com/mozilla/DeepSpeech/releases/download/latest/deepspeech-0.9.3-models.scorer
```

