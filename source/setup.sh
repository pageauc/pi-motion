#!/bin/bash
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
