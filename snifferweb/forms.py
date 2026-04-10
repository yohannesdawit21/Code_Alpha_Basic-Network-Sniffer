from django import forms


class CaptureForm(forms.Form):
    iface = forms.CharField(required=False, label="Network Interface", initial="eth0")
    count = forms.IntegerField(min_value=1, max_value=200, initial=20, label="Packet Count")
    host = forms.CharField(required=False, label="Host Filter")
    proto = forms.ChoiceField(
        required=False,
        choices=[("", "Any"), ("tcp", "TCP"), ("udp", "UDP"), ("icmp", "ICMP")],
        label="Protocol",
    )
    timeout = forms.IntegerField(min_value=1, max_value=30, initial=8, label="Timeout (seconds)")
