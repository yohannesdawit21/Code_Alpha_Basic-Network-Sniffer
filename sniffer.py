#!/usr/bin/env python3
"""Basic packet sniffer for CodeAlpha Task 1."""

from __future__ import annotations

import argparse
from datetime import datetime

from scapy.all import IP, TCP, UDP, Raw, sniff  # type: ignore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Basic network sniffer")
    parser.add_argument("--iface", default=None, help="Network interface (example: eth0)")
    parser.add_argument("--count", type=int, default=20, help="Packet count (0 = continuous)")
    parser.add_argument("--host", default=None, help="Capture only traffic to/from host")
    parser.add_argument(
        "--proto",
        default=None,
        choices=["tcp", "udp", "icmp"],
        help="Capture only a specific protocol",
    )
    return parser.parse_args()


def build_filter(host: str | None, proto: str | None) -> str | None:
    filters: list[str] = []
    if host:
        filters.append(f"host {host}")
    if proto:
        filters.append(proto)
    return " and ".join(filters) if filters else None


def safe_payload(packet) -> str:
    if Raw not in packet:
        return ""
    raw_data = bytes(packet[Raw].load)
    preview = raw_data[:64]
    return preview.decode("utf-8", errors="replace").replace("\n", "\\n")


def packet_handler(packet) -> None:
    if IP not in packet:
        return

    timestamp = datetime.now().strftime("%H:%M:%S")
    ip_layer = packet[IP]
    src_ip = ip_layer.src
    dst_ip = ip_layer.dst
    proto = ip_layer.proto
    length = len(packet)

    src_port = "-"
    dst_port = "-"
    proto_name = f"IP({proto})"

    if TCP in packet:
        proto_name = "TCP"
        src_port = str(packet[TCP].sport)
        dst_port = str(packet[TCP].dport)
    elif UDP in packet:
        proto_name = "UDP"
        src_port = str(packet[UDP].sport)
        dst_port = str(packet[UDP].dport)
    elif proto == 1:
        proto_name = "ICMP"

    payload_preview = safe_payload(packet)

    print(
        f"[{timestamp}] {proto_name:<4} "
        f"{src_ip}:{src_port} -> {dst_ip}:{dst_port} "
        f"len={length} payload='{payload_preview}'"
    )


def main() -> None:
    args = parse_args()
    bpf_filter = build_filter(args.host, args.proto)

    print("Starting packet capture...")
    print(f"Interface : {args.iface or 'default'}")
    print(f"Count     : {'continuous' if args.count == 0 else args.count}")
    print(f"Filter    : {bpf_filter or 'none'}")

    sniff(
        iface=args.iface,
        filter=bpf_filter,
        prn=packet_handler,
        store=False,
        count=args.count,
    )


if __name__ == "__main__":
    main()
