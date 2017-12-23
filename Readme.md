# pimotion.py_2.4
#### Raspberry Pi Python Motion Detect with Rclone syncing to a Storage Service 
For an updated version of this program see my GitHub pi-timolo project
at https://github.com/pageauc/pi-timolo


### Prerequisites
Requires a raspberry pi with a RPI camera module installed and tested running with
updated raspbian operating system installed on min 8gb SD card with expanded file system

***Note:*** If you are using an older raspbian build or previous Picamera python module,
and images are black or have problems then update Raspberry PI firmware per
apt-get update and upgrade or optional firmware raspi-update command.

### Quick Setup
Step 1 Highlight curl command in code box below using mouse left button. Right click mouse in highlighted area and Copy.     
Step 2 On RPI putty SSH or terminal session right click, select paste then Enter to download and run script.

    curl -L https://raw.github.com/pageauc/pi-motion/master/source/setup.sh | bash

### To Update Raspbian

    sudo apt-get update
    sudo apt-get upgrade

### To Run

    ./pimotion.py    

### Program Description

This is a python picamara module application for a Raspberry PI with a RPI camera
module. It is designed for Motion Detection projects.
I use mine for headless security cameras using the makedailymovie.sh to a remote NAS.
and also syncing to my google drive using rclone.
File names can be by Number Sequence or by Date/Time Naming.  
Motion files can be uploaded to your web based google drive using 
github program called rclone (compiled binary included).
NOTE:
pimotion uses low light long exposure for night motion and/or time lapse images.
The program can detect motion during low light, although the long exposure times
can cause blurring of moving objects.

This application uses the picamera python module and requires recent
Raspberry PI Raspbian firmware and updates to work properly.
Here are some motion and time lapse sample YouTube videos.

https://www.youtube.com/playlist?list=PLLXJw_uJtQLa11A4qjVpn2D2T0pgfaSG0

If you are looking for a good web based RPI camera interactive interface, I 
would highly recommend applications mentioned in this forum post
https://www.raspberrypi.org/forums/viewtopic.php?p=780235#p780235
I also use the newer version of pimotion called pi-timolo
here https://github.com/pageauc/pi-timolo
   
Good Luck
Claude Pageau 
