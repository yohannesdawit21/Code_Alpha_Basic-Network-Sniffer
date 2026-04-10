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

## Django UI

Run the web interface:

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

If packet capture permission errors appear in the UI, run Django with elevated privileges:

```bash
sudo .venv/bin/python manage.py runserver
```

Alternative (safer than sudo for daily use):

```bash
sudo setcap cap_net_raw,cap_net_admin=eip .venv/bin/python
```

### Deployment checklist

1. Set production environment variables:

```bash
export DEBUG=False
export SECRET_KEY='replace-with-a-long-random-secret-key'
export ALLOWED_HOSTS='your-domain.com,127.0.0.1'
```

2. (Optional but recommended behind HTTPS proxy) keep secure defaults:

```bash
export SECURE_SSL_REDIRECT=True
export SECURE_HSTS_SECONDS=31536000
```

3. Run Django deploy checks:

```bash
.venv/bin/python manage.py check --deploy
```

4. Collect static files:

```bash
.venv/bin/python manage.py collectstatic --noinput
```

5. Start service (example):

```bash
sudo .venv/bin/python manage.py runserver 0.0.0.0:8000
```

For real internet deployment, use a production server stack (Gunicorn + Nginx) instead of Django runserver.

### How to use the website (step by step)

1. Start the server:

```bash
python manage.py runserver
```

If you get packet permission errors, use:

```bash
sudo .venv/bin/python manage.py runserver
```

2. Open the UI in your browser:

```text
http://127.0.0.1:8000/
```

3. Fill the capture form:

- Network Interface:
	- Leave blank to use default interface, or enter active one like `wlan0`, `eth0`, `enp3s0`.
	- To find yours: `ip -br a` and choose interface that is `UP`.
- Packet Count:
	- Number of packets to capture (try `50` for testing).
- Host Filter:
	- Optional. Enter one IP or hostname, such as `8.8.8.8` or `google.com`.
- Protocol:
	- Choose `Any`, `TCP`, `UDP`, or `ICMP`.
- Timeout (seconds):
	- Maximum wait time for packets (try `10` to `20`).

4. Click **Start Capture**.

5. While capture runs, generate traffic in another terminal:

```bash
ping 8.8.8.8
```

6. Read results in the table:

- Time
- Protocol
- Source
- Destination
- Length
- Payload Preview

### Quick test profile

Use these values for a reliable first test:

- Network Interface: blank (or your active interface)
- Packet Count: `50`
- Host Filter: blank
- Protocol: `ICMP`
- Timeout: `15`

Then run `ping 8.8.8.8` in another terminal and capture again.

### If no packets are captured

- Ensure server was started with proper permissions.
- Try a specific interface from `ip -br a`.
- Remove Host Filter to avoid over-filtering.
- Increase Packet Count and Timeout.
- Generate traffic during capture (ping/curl/browser activity).

Optional filters:

```bash
sudo .venv/bin/python sniffer.py --iface eth0 --count 50 --host 8.8.8.8
sudo .venv/bin/python sniffer.py --iface eth0 --count 0 --proto tcp
```

Notes:

- `--count 0` means continuous sniffing.
- You may need root privileges for packet capture.
- Use in a legal/authorized environment only.
