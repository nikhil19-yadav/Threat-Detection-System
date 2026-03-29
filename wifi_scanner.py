import subprocess

def scan_wifi():
    output = subprocess.check_output("netsh wlan show networks mode=bssid", shell=True).decode()

    networks = []
    lines = output.split("\n")

    current = {}

    for line in lines:
        line = line.strip()

        if line.startswith("SSID"):
            if current:
                networks.append(current)
                current = {}
            current["ssid"] = line.split(":")[1].strip()

        elif "Signal" in line:
            signal = line.split(":")[1].strip().replace("%", "")
            current["signal"] = int(signal)

    if current:
        networks.append(current)

    return networks