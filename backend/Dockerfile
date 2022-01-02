FROM ubuntu

COPY ./requirement.txt ./requirement.txt
COPY ./core /app

RUN apt update && apt install python3 python3-pip cython libpcap-dev curl -y &&\
    pip3 install -r ./requirement.txt

ENTRYPOINT [ "/bin/bash" ]