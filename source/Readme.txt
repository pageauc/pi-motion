                                 pimotion.py_2.1
       Raspberry Pi Python Motion Capture and google drive syncing using grive
       -----------------------------------------------------------------------

Introduction
------------
Security camera application using a Raspberry PI computer with a RPI camera module. 
Detects motion then names (number sequence or sequential) and saves images. Optionally
synchronizes images with your google drive using a precompiled (github) grive binary
requires security setup).

Important
---------
Note if you are using Picamera python module and images are black or have problems then
update Raspberry PI firmware per command below from ssh login or terminal execute the
following command to upgrade to latest firmware. This should resolve any picamera issues.

sudo rpi-update
sudo shutdown -h now
<<<<<<< HEAD

Unplug and restart your Raspberry Pi.
=======
>>>>>>> origin/master
          
Upgrade History
---------------
22-Sep-2014 - Version 2.1 of pymotion.py with an option to use the picamera python module
              to take large photo rather than raspistill
New Features
- Changed setup.sh so it installs python-imaging and python-picamera by default. 
  Note grive_setup.sh has been replaced
- Added option to use picamera to take large photo instead of shelling out to raspian
  to run raspistill. Note small image still uses raspistill. 
- Added lowLight picamera option to take low light photos during specified hours.
  This dramatically improves low light photos but don't use during bright light 
  conditions or photos will be washed out
- Added bestPhoto option to make Daylight photo more consistent
- Added makemovie.py to create a avi movie from contents of google_drive folder.
Fixes
- Fixed bug that crashes pimotion if numsequence is set to False caused by displaying
  initial settings information

Background
----------
I have been working on a grive capable security camera using two types of security camera cases.  
One is a small fake plastic security cam case from Amazon.  Model A or B fits inside with wifi only.
http://www.amazon.com/gp/product/B004D8NZ52/ref=oh_details_o01_s00_i00?ie=UTF8&psc=1
Here is a larger aluminum camera case that I have a model B installed in.  
This one has room for a usb power supply etc.
http://www.amazon.com/Monoprice-108431-Outdoor-Camera-Switchable/dp/B007VDTTTM/ref=sr_1_72?ie=UTF8&qid=1393884556&sr=8-72&keywords=fake+security+camera
I may do a youtube video on How To setup these cases with the raspberry pi computer
and camera module installed.

After some work I now have the Raspberry Pi security camera's working efficiently from
a software point of view. The current configuration uses a modified version of
pimotion.py script to save files to a number sequence instead of a date-time sequence. 
I also added some code (not mine) to optionally put date/time information directly on
the photo images. This is convenient to see the exact time stamp that the photo was taken. 
Using number sequencing allows limiting the number of files that need to get synchronized
to my google drive. 
It was too much to manage all the dated files and cleanup in google drive.  
This method restricts the number of motion files that need to get updated via grive.
Files are overwritten in Round robin fashion. If you need more history you can write a
routine to save google drive files from a synchronized PC folder to a dated archive folder
using a windows robocopy freefilesync or similar program through a batch file.
Synchronization uses a rpi compiled version of grive.  
This requires slightly modifying the source code to make it compatible with the RPI.
  
The tar file is a complete setup including a precompiled grive to reduce the effort
required to get this working. To automate the security camera operation, I have
setup pimotion.py to run from a /etc/init.d/pimotion.sh bash script by copying skeleton
file to pimotion.sh script (sample included).  Then modified to run your pimotion.py script
on boot. see later in post for more setup detail.

You must have a raspberry pi model A, B or B+ with the latest raspbian build and 
pi camera module installed and working. There are several tutorials showing how to do this
so it is not covered here. This assumes you know how to cut and paste into nano or similar
text editor on the pi using ssh (putty). You also need an operational internet connection
via wifi or wired connection. Wifi needs to be setup to work on boot with no desktop in
order for the camera to sync unattended with your google drive.  
I have written the pimotion python script and bash sync scripts to make it somewhat
independent of the folder names etc. This minimizes hard coding folder names in the scripts.  
If you run the script manually from the command line then settings and activity
information will be displayed. Just a little setup for pimotion.py  If you already
have a pimotion.py then mv existing file to another file name

Download and Setup Instructions
-------------------------------
Use putty to ssh into an internet connected raspberry pi and execute the following commands.  
Note change picam to a folder name of your choice if required.

cd ~
mkdir picam
cd ./picam
# Download pimotion.tar file from my github account from a logged in
# ssh using putty or desktop terminal session on your raspberry pi.
wget https://raw.github.com/pageauc/pi-motion-grive/master/pimotion.tar
# Extract tar files to current folder
tar -xvf pimotion.tar
# Install required grive libraries from the internet
sudo ./setup.sh 
# Note this will take a while so be patient

Change pimotion.py settings as required
---------------------------------------
pimotion.py is the modified pimotion.py script based on previous modified brainflakes script.  
I modified the script to allow the use of a number sequence to restrict the total number of files
that need to get sync'd to my google drive using grive.  Currently set to 500 images 
Please note this includes PIL imageFont and imageDraw python modules to optionally
put a date-time stamp on each photo.
Make sure you are in the correct folder containing pimotion.py

nano pimotion.py

Use nano editor to modify any pimotion.py script settings as required 
eg Threshold, Sensitivity, image prefix, numbering range, etc. See code comments for details.
I have the pimotion.py camera image settings set to flipped due to the camera module
mounting position in the fake security camera case. You may also want to change 
sensitivity and/or threshold as needed as well as the filename prefix etc.  
Ctrl-X to save and exit nano editor.

Details if you wish to compile grive yourself (Optional)
--------------------------------------------------------
You will need to download the tar file from the web link below and extract it on your
raspberry pi or compile a modified version of grive in order to sync files to your google drive
see instructions from url link below.  Compiling takes a little while and you must 
edit the specified /home/pi/grive/libgrive/src/drive/State.cc file per the web link below. 
If you have problems read the posts.  When you initialize grive with google I opened an
ssh session to the raspberry pi on my windows 7 PC and then cut and pasted the grive -a url 
to chrome browser while logged into google.  This takes you to a screen that returns a very
long security code.  I then cut and pasted this into the RPI session and everything worked
just fine.  I did not login to google on the pi.  I only needed the PC to be logged in and
paste the authentication code back to the pi from the PC.  I don't think you need a logged
in google account on the pi as the post mentions.  At any rate it worked for me and I had to 
try several times since I was trying to avoid having grive executable in the
google_drive folder.  By using the -p option and copying the grive hidden config files to 
the rpi google_drive folder I managed to get everything to work.   
http://raspberrywebserver.com/serveradmin/back-up-your-pi-to-your-google-drive.html
or this link might be even better
http://www.pihomeserver.fr/en/2013/08/15/raspberry-pi-home-server-synchroniser-le-raspberry-pi-avec-votre-google-drive/

Once compile is successful copy the grive executable to the folder that
pimotion.py and sync.sh are located

Optional Setup grive security to your google account
----------------------------------------------------
If you want to synchronize image files to your google drive then follow the instructions below
Note you must have a valid google account and google drive.
On a PC open a web browser eg chrome and login to your google account and check that you
have a google drive.
Important
---------
It is recommended that any documents you have be moved to a separate google drive folder
eg my_files.  This will prevent these files from getting sync'd back to the Raspberry PI.
You can also perform this operation from a RPI desktop terminal and web browser if you like.
Just make sure you are logged into google from ssh session or RPI desktop terminal session

cd ~
cd picam    # or name of folder you chose
sudo ./grive -a

This will display a web browser url.
You will need to highlight the displayed url on the RPI and paste into the PC or RPI
web browser URL bar. 
Note if you are using putty ssh then right click to paste RPI highlighted
url into the PC's web browser url bar 
The url will open a new web page and display a security hash token.  
Copy and paste this security token into grive via ssh session on rpi. 
if grive -a session hit enter to accept security token. grive will indicate if the
operation was successful

If you previously ran pimotion.py then a google_drive folder should already be created
under the picam folder (or whatever folder you picked)If it does not exist run 

./pimotion.py

to create google_drive or manually create using mkdir command if desired.

Once grive has been initialized successfully with the grive -a option then
copy the /home/pi/.grive and /home/pi/.grive_state files to the
/home/pi/picam/google_drive folder or your folder name per above code. 
This will allow grive to be executed from the /home/pi folder so it does not
have to be in the google_drive folder.

sudo cp ./.grive google_drive
sudo cp ./.grive_state google_drive
sudo ./sync.sh

You should see grive handshake with your google account and synchronize files both
ways between google and the RPI

Test pimotion.py and sync.sh together
-------------------------------------
To test you can launch pimotion.py from one ssh session and sync.sh from a
second ssh terminal session. 
Note: This can also be done from the RPI desktop using two terminal sessions.

First terminal session
----------------------
cd ~
cd picam  # or whatever folder name you used.
sudo ./pimotion.py

Second terminal session
-----------------------
From a second ssh terminal run sync.sh (make sure that motion was detected and files
are in the google_drive folder to sync).  
You should see a /home/pi/picam/sync.lock file.  This is created by pimotion.py when
motion photos were created.

cd ~
cd picam  # or whatever folder name you used.
sudo ./sync.sh

You should see files being synchronized in both directions.  This is normal.  
There are google drive apps for Apple, Android, Mac and PC.  Just do a search for
google drive in the appropriate app/play store This will allow you to access your
google drive on the web to view the raspberry pi motion capture security camera images
You can also download and install the google drive windows application to your PC.
Make sure you have a wifi or wired network connection to the internet that will start
when the RPI boots headless. see setup for crontab and init.d setup for further details
pymotion.py should start automatically and save images to the google_drive folder.
When the crontab is executed it will initiate a sync of images to your
google drive on the web.  
 
Note:
-----
I also setup a cronjob to reboot the rpi once a day but this may not be necessary for you.  
I did it since I intend to leave the rpi security camera run remotely and this gives
a chance for system to recover should there be a glitch.
Also if you have problems check permissions.  The init.d will run as root so the files
in the google_drive folder will be owned by root.  
Just check to make sure you run with sudo ./pimotion.sh and sudo ./sync.sh
if you are in terminal sessions. Once you know sync.sh is working OK you can automate
the sync by running it in as a cronjob.

Setup init.d script to auto launch pimotion.py on boot-up of raspberry pi
-------------------------------------------------------------------------
Note there is a copy of the init.d pimotion.sh in the tar file so you should be able
to copy if instead of the skeleton file method below if you wish  eg in the 
pimotion folder execute the following then skip to step 4

sudo cp pimotion.sh /etc/init.d

check permissions for the /etc/init.d/pimotion.sh to make sure it is executable  
if required change permissions for pimotion.sh using chmod command 

ls -al /etc/init.d/pimotion.sh

cd /etc/init.d
chmod +x pimotion.sh
sudo nano pimotion.sh   
# change appropriate entries to point to your pimotion.py script and save the file ctrl-x
sudo update-rc.d pimotion.sh defaults
cd ~

Optional  (Only if you have setup grive security)
Create a crontab to automate syncronization to google_drive from the RPI
------------------------------------------------------------------------
From an logged in ssh or terminal session

sudo crontab -e

Paste the following line into the crontab file nano editor and modify folder name
and frequency if required. currently executes every minute. 

*/1 * * * * /home/pi/picam/sync.sh >/dev/nul

ctrl-x to exit nano and save crontab file
This cron job will run once a minute.  You can change to suit your needs.  
If grive is already running or there are no files to process then the script simply exits. 
Also if grive has been running for more than 5 minutes it is killed.  
This can be changed in the script if you wish.

Reboot RPI and test operation by triggering motion and checking images are
successfully transmitted to your google_drive and optionally sync'd with your
google drive on the internet.  
Trouble shoot problems as required.

Good Luck
Claude Pageau 
