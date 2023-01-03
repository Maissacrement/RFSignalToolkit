FROM ubuntu:20.04

COPY . /app
WORKDIR /app

RUN apt update && DEBIAN_FRONTEND=noninteractive apt install --fix-missing recode vim cython python3 python3-pip cython libpcap-dev curl vim tshark bsdmainutils xxd uuid-runtime translate-shell geoip-bin geoip-database -y
RUN pip3 install Cython && pip3 install -r ./requirement.txt;\
    chmod +x ./packetExtractor/logger.sh