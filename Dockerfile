FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:02ab-main

RUN apt-get install -y curl

RUN apt-get update -y &&\
    apt-get install -y autoconf samtools &&\
    apt-get -y install picard-tools

COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN python3 -m pip install --upgrade latch
WORKDIR /root