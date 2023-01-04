# INSTALL

## Package

pip:
```bash
cd backend
pip install -r requirements.txt 
```

ubuntu:
```bash
apt install recode vim cython python3 python3-pip cython libpcap-dev curl vim tshark bsdmainutils xxd uuid-runtime translate-shell geoip-bin geoip-database make
```

## Docker 

```bash
make radio  (Docker + Make)
```

# TEST

## API endpoint "0.0.0.0:5000"

### RUN server

```bash
python app.py
```

### Unit

execute curl:

```bash
chmod +x ./unit
./unit
```

### Endpoints

/magnet:

body -> json:

[{"createdAtNs":6266926915594,"magnet":"[0.12, -52.379997, 199.08, 30.96, -18.48, 192.9]","initialTime":6239985773844,"result":-39366.797,"coordinates":"[0.0, 0.0, 0.0]"},]

```yaml
createdAtNs: Date.timestamp
magnet: [ * Magnet<x, y, z>, * Iron<x, y, z> ] # Double 3-axis array (original magnet, iron magnet)
result: float # proximity EM sensor using Lorrentz
coordinate: Magnet<x, y, z> - Magnet<x1, y2, z3> # will be removed
```


