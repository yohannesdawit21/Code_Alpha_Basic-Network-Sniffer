from __future__ import annotations

from django.shortcuts import render

from .forms import CaptureForm
from sniffer import collect_packets


def index(request):
    packets = []
    error = ""
    info = ""

    if request.method == "POST":
        form = CaptureForm(request.POST)
        if form.is_valid():
            iface = form.cleaned_data["iface"] or None
            count = form.cleaned_data["count"]
            host = form.cleaned_data["host"] or None
            proto = form.cleaned_data["proto"] or None
            timeout = form.cleaned_data["timeout"]
            try:
                packets = collect_packets(
                    iface=iface,
                    count=count,
                    host=host,
                    proto=proto,
                    timeout=timeout,
                )
                if not packets:
                    info = (
                        "No packets captured. Try leaving interface blank, increase count/timeout, "
                        "and generate traffic (for example, ping a host)."
                    )
            except PermissionError:
                error = "Permission denied. Run Django with sudo or assign packet capture capabilities to Python."
            except Exception as exc:  # Broad catch to keep UI friendly.
                error = f"Capture failed: {exc}"
    else:
        form = CaptureForm()

    return render(
        request,
        "snifferweb/index.html",
        {
            "form": form,
            "packets": packets,
            "error": error,
            "info": info,
        },
    )
