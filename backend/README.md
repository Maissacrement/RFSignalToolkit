# Radio sniffer

## Welcom in Radio Sniffer Backend Tool

### How to curl

```bash
./backend/unit
```


### How to install

```bash
apt install python3 python3-pip cython libpcap-dev curl
pip3 install Cython
pip3 install -r requirement.txt
```

### How to run

Docker
```bash
make radio  (Docker + Make)
```

Python
```bash
python3 app.py
```

### Presentation

The main api will receive the information from the phone or other sour sdr and convert it to hexadecimal format. This is a standard used to observe files stored in memory.

![My animated logo](./asset/architect.drawio.png)

The Analysis class will group all our mathematical functions applied to signal processing.
So let's say we are going to focus on the quantization of this signal in CAN

![My animated logo](./asset/Diagramme.drawio.png)

## Magnet receive frame

![My animated logo](./asset/index.jpeg)