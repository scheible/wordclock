#!/bin/sh
cd $(dirname $0)
python3 change_dhcpcd_config.py static
dhcpcd -k wlan0
wpa_cli -i wlan0 disconnect
systemctl stop wpa_supplicant
dhcpcd -n wlan0
systemctl start dnsmasq
systemctl start hostapd