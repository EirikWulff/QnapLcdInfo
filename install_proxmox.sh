#!/bin/bash

#root check
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi
path="/opt/lcdInfo"
mkdir -p ${path}
cp -f * ${path}/
python -m venv ${path}

cd ${path}
source ${path}/bin/activate
python -m pip install -r requirements.txt
chmod +x lcdInfo.py


# Setup service
sed -i -e "s|/usr/local/bin/lcdInfo/lcdInfo.py|$path/bin/python $path/lcdInfo.py|g"
# cat <<EOF > lcdInfo.service
# [Unit]
# Description=Qnap LCD Info Service
# After=syslog.target

# [Install]
# WantedBy=multi-user.target

# [Service]
# Type=simple
# Restart=on-failure
# EOF
# echo "ExecStart=${path}/bin/python ${path}/lcdInfo.py" >> lcdInfo.service
# Install service
mv systemd/lcdinfo.service /etc/systemd/system/
systemctl enable lcdinfo.service
systemctl start lcdinfo.service 