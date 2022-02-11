FROM ubuntu

COPY ./requirement.txt ./requirement.txt
COPY . /app
WORKDIR /app

RUN apt update && DEBIAN_FRONTEND=noninteractive apt install cython python3 python3-pip cython libpcap-dev curl tshark bsdmainutils xxd uuid-runtime -y &&\
    chmod +x ./packetExtractor/logger.sh;./packetExtractor/logger.sh &&\
    pip3 install Cython && pip3 install -r ./requirement.txt

ENTRYPOINT [ "python3", "app.py" ]