# pimotion.py_2.3
##### Raspberry Pi Python Motion Capture and google drive syncing using gdrive
##### For an updated version of this program see pi-timolo 
here https://github.com/pageauc/pi-timolo

**Version 2.3 release notes**
20-Jul-2015 - removed non functional grive and replaced with gdrive

**Version 2.2 release notes**
25-Nov-2014 - recompiled grive due to a binutils version problem.
also updated setup.sh to include additional libraries and created new pimotion.tar

**Version 2.1 release notes**
22-Sep-2014 - Changed pimotion.py with an option to use the
picamera python module to take large photo rather than raspistill

### Quick Setup

(assumes raspberry pi with RPI camera module installed and tested running updated raspbian
operating system installed on min 8gb SD card with expanded file system)
Note: If you are using an older raspbian build or previous Picamera python module,
and images are black or have problems then update Raspberry PI firmware per optional
firmware update command below.

From a (putty) SSH login or rpi console desktop terminal execute the following
commands to upgrade to latest firmware. This should resolve any picamera issues.
Also it is advised you use at least an 8 GB SD card with file system
expanded using

    sudo raspi-config

 Update Raspbian

    sudo apt-get update
    sudo apt-get upgrade

(Optional) Update RPI firmware (optional: run if you are using older RPI
firmware and having problems with python picamera module errors or image quality issues)  

	sudo rpi-update

Hard boot to update firmware

    sudo shutdown -h now


Unplug and restart your Raspberry Pi.
Login and install pimotion.py

    cd ~
    mkdir picam
    cd ./picam
    wget https://raw.github.com/pageauc/pi-motion-grive/master/pimotion.tar
    tar -pxvf pimotion.tar
    sudo ./setup.sh
    sudo python ./pimotion.py

Verify motion (per screen log entries) then ctrl-c to exit pimotion.py
Edit pimotion.py file using nano editor to change any desired settings per comments. ctrl-x y to Save

    nano pimotion.py

Test edit changes.

    sudo ./pimotion.py 

### Program Description

This is a python picamara module application for a Raspberry PI with a RPI camera
module. It is designed for Motion Detection projects.
I use mine for headless security cameras using the makedailymovie.sh to a remote NAS.
and also syncing to my google drive using gdrive.
File names can be by Number Sequence or by Date/Time Naming.  
Motion files can be uploaded to your web based google drive using 
github program called gdrive (compiled binary included).
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

### Background History

I have been working on a headless internet capable security camera using two types of
security camera cases. One is a small fake plastic security cam case
from Amazon.  Model A or B fits inside with wifi only.

http://www.amazon.com/gp/product/B004D8NZ52/ref=oh_details_o01_s00_i00?ie=UTF8&psc=1

Here is a larger aluminium camera case that I have a model B installed in.  
This one has room for a usb power supply etc.

http://www.amazon.com/Monoprice-108431-Outdoor-Camera-Switchable/dp/B007VDTTTM/ref=sr_1_72?ie=UTF8&qid=1393884556&sr=8-72&keywords=fake+security+camera

After some work I now have the Raspberry Pi security camera's working
efficiently from a software point of view. The current configuration uses
the pimotion.py script to save files to a number sequence or a date-time
sequence. I also added some code to optionally put date/time information
directly on the photo images. This is convenient to see the exact time stamp
that the photo was taken. 
Using number sequencing allows limiting the number of files that need to
get synchronized to my google drive. 
It was too much to manage all the dated files and clean up google drive.  
This method restricts the number of motion files that need to get updated
via the sync.sh. It is suggested you set up a crontab for sync.sh script.
  
The pimotion.tar file is a complete setup including instructions.
To automate the camera operation, I have setup pimotion.py to run from
a /etc/init.d/pimotion.sh bash script by copying /etc/init.d/skeleton file
to pimotion.sh script (sample included).

### Prerequisites

You must have a raspberry pi model A, A+, B, B+ or B-2 with the latest raspbian build
and a pi camera module installed and working. There are several tutorials
showing how to do this so it is not covered here. This assumes you know 
how to cut and paste into nano or similar text editor on the pi using
ssh (putty). You also need an operational internet connection via wifi
or wired connection. Wifi needs to be setup to work on boot with no desktop in
order for the camera to sync unattended with your google drive.  
I have written the pimotion python script and bash sync scripts to make it
somewhat independent of the folder names etc. This minimizes hard coding
folder names in the scripts. If you run the script manually from the
command line then settings and activity information can be enabled to display.

### Setup init.d to run pimotion on boot

To auto launch pimotion.py on boot-up of raspberry pi
Note there is a copy of the init.d pimotion.sh in the tar file so you should
be able to copy if instead of the skeleton file method below if you wish 
eg in the pimotion folder execute the following then skip to edit 
/etc/init.d/pimotion.sh using nano.

    cd ~
    cd picam
    sudo cp pimotion.sh /etc/init.d

Check permissions for the /etc/init.d/pimotion.sh to make sure it is executable  
if required change permissions for pimotion.sh using chmod command 
 
    ls -al /etc/init.d/pimotion.sh
    cd /etc/init.d
    sudo chmod +x pimotion.sh
    sudo nano pimotion.sh
   
Change appropriate entries to point to your pimotion.py script and save
the file using ctrl-x.  If you copied downloaded sample script and have not
changed the pimotion folder name then no editing step above should be required.
Initialize the /etc/init.d/pimotion.sh script so it executes on boot.

    sudo update-rc.d pimotion.sh defaults
    cd ~

Reboot RPI and test operation by triggering motion and checking images are
successfully saved to your motion folder.  
Trouble shoot problems as required.

### Setup gdrive sync

gdrive is included with the pimotion.tar file but you can
optionally install gdrive binary from source perform the following.

    cd /tmp
    wget https://github.com/odeke-em/drive/releases/download/v0.2.2-arm-binary/drive-arm-binary
    chmod +x drive-arm-binary
    sudo cp drive-arm-binary /usr/local/bin/gdrive
    cd ~
    gdrive version

Setup gdrive security for secure access to your google drive.
Note: This assumes you have a google drive with a google account eg gmail
and you are using a SSH terminal session logged into your Raspberry Pi computer.
for additional details see https://github.com/odeke-em/drive
From a windows PC that has the Chrome browser installed and logged into your google account eg gmail.

    cd ~
    cd picam
    sudo gdrive init
    
- command above will display a long url in the RPI SSH session.
- in SSH window use mouse left button to highlight the url (do NOT press enter)
- On the PC Chrome Browser window open a new tab and right click in the top url box
- Make sure you are logged into your google account eg gmail
- Right mouse click in the new tab url box and select paste and go
- This will display a google message to confirm access
- After you Accept a security code box will be displayed
- Use left mouse to highlight security code then right click and copy
- Return to RPI SSH session and right click gdrive init prompt to paste security code
- Press enter to accept code. If OK no errors will be displayed. 
A hidden .gd subfolder will be created in the picam folder.
.gd contains gdrive security files. For syncing purposes the picam folder
will be considered as root.

To see the hidden files and folders

    cd ~
    ls -al

To list gdrive help type gdrive command with no parameters

    gdrive 

to confirm access to your google drive perform the following. 
This should display the contents of your google drive root folder.

    sudo gdrive ls

If you have multiple cameras syncing to google drive
it is advised to change the motion folder name to something unique.  You will
also need to change the config.py motionDir= setting and sync.sh accordingly.
     
Verify the config.py has the motion setting

    createLockFile = True

The pimotion.sync file will then be created when motion images are created.
Check if a pimotion.sync file exists in the picam folder otherwise run

    sudo ./pimotion.py
     
and activate motion to create images and a new pimotion.sync file.
Run sync.sh script to test google drive syncing with specified local folder
default is /home/pi/picam/motion. To run sync.sh executed the following

    sudo ./sync.sh
 
The sync.sh script will perform the following
- Checks if gdrive sync is already running.
- Runs gdrive only if it is not already running and Kills gdrive processes
if it has been running too long. default is > 600 seconds or 10 minutes.
change the sync.sh script if you need a different time to kill time period.
- Looks for pimotion.sync file created by pimotion.py indicating there are new files to sync
otherwise it exits without attempting to resolve google drive files with specified local folder.
- If a pimotion.sync file exists it runs a gdrive push to sync local folder
with the specified google drive subfolder
- Reports if sync was successful or errors were encountered 

Suggest you run this script from a crontab every 5 minutes or so.  
Add appropriate line to crontab using command

    sudo crontab -e

Add example crontab entry per below then save and exit nano using ctrl-x y

    */5 * * * * /home/pi/picam/sync.sh >/dev/nul

### Utilities

There are several other utilities included with pi-timolo 

- h2mp4.sh  This is a simple script to convert h264 video files to mp4 format using 
MP4Box that is downloaded an installed as part of gpac library during setup.sh
- makemovie.py  creates avi movie from all jpg files in specified folder see
code for details
- makedailymovie.sh  creates avi movie with a unique date/time file name this
 is designed to be run from a crontab
- sync.sh  uses gdrive to push sync local files with google drive. 
see description above for details.
- mvleavelast.sh  Just a short script to copy all files except the latest
in case file is still open
    
Good Luck
Claude Pageau 
