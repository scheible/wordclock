#!/bin/sh
# installer script for uhrthree
# run this script as root or with sudo

echo "updating package sources"
apt-get update

echo "install binary packages"
apt-get install -y hostapd dnsmasq python3.7-venv nginx python3-pip

echo "unmasking hostapd daemon"
systemctl unmask hostapd

echo "stopping hostapd daemon"
systemctl stop hostapd

echo "disabling hostapd daemon"
systemctl disable hostapd

echo "stopping dnsmasq"
systemctl stop dnsmasq

echo "disabling dnsmasq daemon"
systemctl disable dnsmasq

echo "overwriting AP settings"
cp ../ap_config/dhcpcd.conf /etc/dhcpcd.conf
cp ../ap_config/hostapd.conf /etc/hostapd/hostapd.conf
cp ../ap_config/dnsmasq.conf /etc/dnsmasq.conf

echo "copying nginx configuration file"
cp wordclock /etc/nginx/sites-available/
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/wordclock /etc/nginx/sites-enabled/wordclock

echo "restarting nginx"
systemctl restart nginx


echo "making AP scripts executable"
chmod +x /opt/wordclock/shared/start_ap.sh
chmod +x /opt/wordclock/shared/stop_ap.sh

echo "creating python virtual environment"
python3 -m venv /opt/wordclock/env

echo "installing python modules into virtual env"
/opt/wordclock/env/bin/python -m pip install flask
/opt/wordclock/env/bin/python -m pip install zmq
/opt/wordclock/env/bin/python -m pip install gunicorn


echo "creating gunicorn service"
cp wordclockweb.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable wordclockweb.service
systemctl start wordclockweb.service

echo "modify access rights on wpa_supplicant and etc/localtime"
chmod o+w /etc
chmod o+w /etc/localtime
chmod o+w /etc/wpa_supplicant/wpa_supplicant.conf