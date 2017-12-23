#!/bin/bash
# $0 ver 1.2 written by Claude Pageau

install_Dir="pi-motion"

cd ~
mkdir -p $install_Dir
cd $install_Dir

installFiles=("Readme.md" "pimotion.py" "pimotion.sh" \
"makemovie.sh" "mvleavelast.sh" "makedailymovie.sh" "h2mp4.sh" "sync.sh")

for fname in "${installFiles[@]}" ; do
    wget_output=$(wget -O $fname -q --show-progress https://raw.github.com/pageauc/pi-motion/master/source/$fname)
    if [ $? -ne 0 ]; then
        wget_output=$(wget -O $fname -q https://raw.github.com/pageauc/pi-motion/master/source/plugins/$fname)
        if [ $? -ne 0 ]; then
            echo "ERROR - $fname wget Download Failed. Possible Cause Internet Problem."
        else
            wget -O $fname https://raw.github.com/pageauc/pi-motion/master/source/$fname
        fi
    fi
done

echo "Installing rclone"
curl -L https://raw.github.com/pageauc/rclone4pi/master/rclone-install.sh | bash

chmod +x *py
chmod +x *sh

dos2unix *sh
dos2unix *py

echo "    Downloading and Installing pimotion dependencies.  Wait ..."
sudo apt-get install -y python-picamera python3-picamera python-imaging dos2unix gpac python-pyexiv2

echo "
                   INSTRUCTIONS
                   
Make sure pi-camera is connected and enabled in raspi-config

To Run run command below in a logged in console session

cd $install_Dir
./pimotion.py

"