#!/bin/sh
cd $(dirname $0)
python3 change_dhcpcd_config.py dhcp
dhcpcd -k wlan0
systemctl stop dnsmasq
systemctl stop hostapd 
dhcpcd -n wlan0
systemctl start wpa_supplicant
wpa_cli -i wlan0 reconfigure
wpa_cli -i wlan0 select_network 0
