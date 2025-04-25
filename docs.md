# 
## Creation
[DeepSpeech](https://github.com/mozilla/DeepSpeech)
[deepspeech docs](https://deepspeech.readthedocs.io/en/r0.9/?badge=latest)

### Initial docker setup
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

### Sitting up deep speech
``` dockerfile
# python deep speech package install
RUN virtualenv -p python3 $HOME/deep-venv \
    && source $HOME/deep-venv/bin/activate \
    && pip3 install deepspeech
```

### Setting up models needed for the actual speech processing

We are going to pout them in the virtual environment for now as it it kind of
like the root for the project, so might as well be in one place.

``` dockerfile
RUN cd /$HOME/deep-venv && curl -LO https://github.com/mozilla/DeepSpeech/releases/download/latest/deepspeech-0.9.3-models.pbmm
RUN cd /$HOME/deep-venv && curl -LO https://github.com/mozilla/DeepSpeech/releases/download/latest/deepspeech-0.9.3-models.scorer
```
For setting up the deepspeech model that would be enough.

### Architecture
The drive for this solution is for it to be as simple as possible. Simplicity
should be the end goal for every process.

The Interface that the deep speech model has provides a simple API for
processing streams, that are an array(stream) of numpy.Int16 data.

- The deepspeech library is wrapped with a web server to take in numpy.Int16 data. 
    - There is a session management for that http server, so as to send the proper
    response to the proper client.

- Client is a python(ideally) console application that takes in data from a file or stdin,
  serializes it to the correct format and sends it to the server. When it
  receives a result it uses stdout and stderr to communicate that result.
  - That client is also made of 2 parts, just to expose the communication to
    the server as a interface, so it can be easily integrated into other python
    applications. The second part is just a thin wrapper around it to facilitate
    interaction with the shell. 
  - Client is responsible for data serialization. Converting audio files to
    proper format shouldn't be done on the server.

With the above design decisions the design should be as composable as possible
the way it is described. Any application can be made to connect to the server.
Client communicates through established ways of interprocess communication.
The client application can be embedded easily in multiple ways. The contract
between the server and the client can also be reverse engineered.

Reading from device microphone would just making the console application read
from the device microphone. Not that much different from 'processing a normal
file' case. A systemd service(or any other init system of choice) can be made to
set up the proper permissions. And the existence of a microphone on the host
device, is not required. Which also makes the server simpler-ish.

Multiple file types supported.








