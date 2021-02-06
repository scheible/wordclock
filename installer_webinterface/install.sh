#!/bin/sh
# installer script for uhrthree
# run this script as root or with sudo

echo "updating package sources"
apt-get update

echo "install binary packages"
apt-get install -y hostapd dnsmasq python3.7-venv nginx

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
cp uhrthreeweb /etc/nginx/sites-available/
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/uhrthreeweb /etc/nginx/sites-enabled/uhrthreeweb

echo "creating application directory"
mkdir /opt/uhrthree

echo "installing AP scripts"
cp ../ap_config/change_dhcpcd_config.py /etc/uhrthree/
cp ../ap_config/start_ap.sh /etc/uhrthree/
cp ../ap_config/stop_ap.sh /etc/uhrthree/
chmod +x /etc/uhrthree/start_ap.sh
chmod +x /etc/uhrthree/sstop_ap.sh

echo "creating python virtual environment"
python3 -m venv /opt/uhrthree/env

echo "installing python modules into virtual env"
/opt/uhrthree/env/bin/python -m pip install flask
/opt/uhrthree/env/bin/python -m pip install zmq
/opt/uhrthree/env/bin/python -m pip install gunicorn

echo "installing python modules"
cp -r ../modules/uhrthree /opt/uhrthree/env/lib/python3.7/site-packages

echo "installing web application files"
cp ../web_application/webinterface.py /opt/uhrthree/webinterface.py
cp ../web_application/wsgi.py /opt/uhrthree/wsgi.py

echo "creating gunicorn service"
cp uhrthreeweb.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable uhrthreeweb.service
systemctl start uhrthreeweb.service

echo "modify access rights on wpa_supplicant and etc/localtime"
chmod o+w /etc
chmod o+w /etc/localtime
chmod o+w /etc/wpa_supplicant/