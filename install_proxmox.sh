#!/bin/bash

#root check
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

apt update -q && apt install -yq python3-pip python3-venv

path="/opt/lcdInfo"
mkdir -p ${path}
cp -rf * ${path}/
python -m venv ${path}

cd ${path}
source ${path}/bin/activate
python -m pip install -r requirements.txt
chmod +x lcdInfo.py


# Setup service
sed -i -e "s|/usr/local/bin/lcdInfo/lcdInfo.py|$path/bin/python $path/lcdInfo.py|g" ${path}/systemd/lcdinfo.service

cp ${path}/systemd/lcdinfo.service /etc/systemd/system/
systemctl enable lcdinfo.service
systemctl start lcdinfo.service 