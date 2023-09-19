#!/bin/bash

export $(cat .env | xargs)

# docker login
docker login devpos6th.kr.ncr.ntruss.com \
    -u $NCP_ACCESS_KEY  \
    -p $NCP_SECRET_KEY

# image pull
docker pull devpos6th.kr.ncr.ntruss.com/trackmission:latest

# docker run
docker run -p 8000:8000 -d \
    --env-file .env \
    --name trackmission \
    devpos6th.kr.ncr.ntruss.com/trackmission:latest
