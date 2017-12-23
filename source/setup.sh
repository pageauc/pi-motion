#!/bin/bash
# $0 ver 1.2 written by Claude Pageau

install_Dir="pi-motion"

cd ~
mkdir -p $install_Dir
cd install_Dir

installFiles=("Readme.md" "pimotion.py" "pimotion.sh" "pi-timolo.sh" \
"makeMovie.sh" "mvleavelast.sh" "makedailymovie.sh" "h2mp4.sh" "sync.sh")

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

echo "Download and Install and pi-motion dependencies. One Moment Please ......."
sudo apt-get install -y python-picamera python3-picamera gpac python-imaging 

echo "Installing rclone"
curl -L https://raw.github.com/pageauc/rclone4pi/master/rclone-install.sh | bash

chmod +x *py
chmod +x *sh

echo "
                   INSTRUCTIONS
                   
Make sure pi-camera is connected and enabled in raspi-config

To Run run command below in a logged in console session

cd $install_Dir
./pimotion.py

"


=======
echo "    Downloading and Installing pimotion dependencies."
echo "    One Moment Please ......."
sudo apt-get install -y python-picamera  python-imaging mencoder dos2unix gpac python-pyexiv2
sudo chmod +x gdrive
sudo cp gdrive /usr/local/bin
echo "    Install complete."
echo "    Edit the pimotion.py variables to suit your needs per comments"
echo "nano pimotion.py"
echo "    Run pimotion.py with command below to Test.  See Readme.md"
echo "    for additional instructions"
echo "sudo ./pimotion.py"
echo "See Readme.md for setting up gdrive security token"

