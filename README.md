# Task 1: Basic Network Sniffer

This task captures live packets and displays useful metadata:

- source and destination IP
- protocol
- source and destination ports (if TCP/UDP)
- packet length
- payload preview

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
sudo .venv/bin/python sniffer.py --iface eth0 --count 20
```

Optional filters:

```bash
sudo .venv/bin/python sniffer.py --iface eth0 --count 50 --host 8.8.8.8
sudo .venv/bin/python sniffer.py --iface eth0 --count 0 --proto tcp
```

Notes:

- `--count 0` means continuous sniffing.
- You may need root privileges for packet capture.
- Use in a legal/authorized environment only.
