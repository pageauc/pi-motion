#!/usr/bin/python

# pimotion 2.3  Updated 20-Jul-2015
# original script by brainflakes, improved by pageauc, peewee2 and Kesthal
# www.raspberrypi.org/phpBB3/viewtopic.php?f=43&t=45235


pymotion_version = "2.4"
print "Initializing %s ...." % ( pymotion_version )
# If this option is set to True then picamera will be used instead of shelling to OS to run raspistill
use_picamera = True

import picamera
from fractions import Fraction

import StringIO
import subprocess
import os
import time
import shutil
import datetime
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

###########  Motion detection settings:
# find the path of the of this python script and set some global variables
mypath=os.path.abspath(__file__)
baseDir=mypath[0:mypath.rfind("/")+1]
baseFileName=mypath[mypath.rfind("/")+1:mypath.rfind(".")]
progname = os.path.basename(__file__) + "_" + pymotion_version

starttime = datetime.datetime.now()
# rightnow =  "%04d%02d%02d-%02d:%02d:%02d" % (starttime.year, starttime.month, starttime.day, starttime.hour, starttime.minute, starttime.second)

# Threshold - how much a pixel has to change by to be marked as "changed"
threshold = 50
# Sensitivity - how many changed pixels before capturing an image, needs to be higher if noisy view
sensitivity = 25

# ForceCapture - whether to force an image to be captured every forceCaptureTime seconds, values True or False
forceCapture = True
forceCaptureTime = 60 * 60 # Once an hour

# filepath - location of folder to save photos
filepath = baseDir + "images"
if not os.path.isdir(filepath):
  print "%s Photo Storage folder not found." % (progname)
  print "%s - creating photo storage folder %s " % (progname, filepath)
  os.makedirs(filepath)

# filenamePrefix - string that prefixes the file name for easier identification of files.  A dash will be added at end as part of formating.
filenamePrefix = "rpi-cam2"

# Lock File is used to indicate photos are added
createLockFile=True
lockfilepath = baseDir + baseFileName + ".sync"

# Use filename sequence numbering instead of date and time
numsequence = True
countpath =  baseDir + baseFileName + ".dat"
startCount = 1000
maxPhotos = 500
# Overlay image name, date and time on bottom of images
showDateOnImage = True
# takes consistently exposed photos that are better for timelapse (daylight only)
bestPhoto = False

# diskSpaceToReserve - Delete oldest images to avoid filling disk. How much byte to keep free on disk.
mbToReserve = 200
diskSpaceToReserve = mbToReserve * 1024 * 1024 # Keep 200 mb free on disk

# cameraSettings - "" = no extra settings; "-hf" = Set horizontal flip of image; "-vf" = Set vertical flip; "-hf -vf" = both horizontal and vertical flip
cameraSettings = ""
picameraVFlip = False

# settings of the full size photos to save
saveWidth   = 1296
saveHeight  = 972
saveQuality = 15 # Set jpeg quality (0 to 100)

# Special Settings for low lighting between the hours specified 24 h time
lowLight = True
dayLight_start = 5       # 6am
dayLight_end = 20        # 10pm

# Test-Image settings
testWidth = 100
testHeight = 75

# this is the default setting, if the whole image should be scanned for changed pixel
testAreaCount = 1
testBorders = [ [[1,testWidth],[1,testHeight]] ]  # [ [[start pixel on left side,end pixel on right side],[start pixel on top side,stop pixel on bottom side]] ]
# testBorders are NOT zero-based, the first pixel is 1 and the last pixel is testWith or testHeight

# with "testBorders", you can define areas, where the script should scan for changed pixel
# for example, if your picture looks like this:
#
#     ....XXXX
#     ........
#     ........
#
# "." is a street or a house, "X" are trees which move arround like crazy when the wind is blowing
# because of the wind in the trees, there will be taken photos all the time. to prevent this, your setting might look like this:

# testAreaCount = 2
# testBorders = [ [[1,50],[1,75]], [[51,100],[26,75]] ] # area y=1 to 25 not scanned in x=51 to 100

# even more complex example
# testAreaCount = 4
# testBorders = [ [[1,39],[1,75]], [[40,67],[43,75]], [[68,85],[48,75]], [[86,100],[41,75]] ]

# in debug mode, a file debug.bmp is written to disk with marked changed pixel an with marked border of scan-area
# debug mode should only be turned on while testing the parameters above
debugMode = False # False or True

# Capture a small test image (for motion detection)
def captureTestImage(settings, width, height):
    command = "raspistill %s -w %s -h %s -t 200 -e bmp -n -o -" % (settings, width, height)
    imageData = StringIO.StringIO()
    imageData.write(subprocess.check_output(command, shell=True))
    imageData.seek(0)
    im = Image.open(imageData)
    buffer = im.load()
    imageData.close()
    return im, buffer

# Save a full size image to disk
def saveImage(settings, width, height, quality, diskSpaceToReserve):
    keepDiskSpaceFree(diskSpaceToReserve)
    rightnow = datetime.datetime.now()

    if numsequence:
        filename = filepath + "/" + filenamePrefix + "-" + fileCount + ".jpg"
        imageTagName = filenamePrefix + "-" + fileCount + "   %04d%02d%02d-%02d:%02d:%02d" % (rightnow.year, rightnow.month, rightnow.day, rightnow.hour, rightnow.minute, rightnow.second)
    else:
        filename = filepath + "/" + filenamePrefix + "-%04d%02d%02d-%02d%02d%02d.jpg" % (rightnow.year, rightnow.month, rightnow.day, rightnow.hour, rightnow.minute, rightnow.second)
        imageTagName = filenamePrefix + "-" + "%04d%02d%02d-%02d:%02d:%0ds" % (rightnow.year, rightnow.month, rightnow.day, rightnow.hour, rightnow.minute, rightnow.second)

    #  Use picamera python module otherwise shell to os and use raspistill
    if use_picamera:
      if lowLight:
        if ((rightnow.hour >= dayLight_start) and (rightnow.hour <= dayLight_end)):
           lowLight_night = False
        else:
           lowLight_night = True

      # Use picamera python module to take image rather than raspistill
      if lowLight_night:
        # Low Light (night time) conditions
        with picamera.PiCamera() as camera:
           camera.vflip = picameraVFlip
           camera.resolution = (width, height)
           # Set a framerate of 1/6fps, then set shutter
           # speed to 6s and ISO to 800
           camera.framerate = Fraction(1, 6)
           camera.shutter_speed = 6000000
           camera.exposure_mode = 'off'
           camera.iso = 800
           # Give the camera a good long time to measure AWB
           # (you may wish to use fixed AWB instead)
           time.sleep( 10 )
           # Finally, capture an image with a 6s exposure. Due
           # to mode switching on the still port, this will take
           # longer than 6 seconds
           camera.capture(filename)
      else:
        # Normal Daylight conditions
        with picamera.PiCamera() as camera:
           camera.vflip = picameraVFlip
           camera.resolution = (width, height)
           # bestPhoto takes a consistent images but slower. Best for timelapse processing.
           if bestPhoto:
             camera.framerate = 30
             # Give the camera's auto-exposure and auto-white-balance algorithms
             # some time to measure the scene and determine appropriate values
             camera.iso = 200
             time.sleep( 2 )
             # Now fix the values
             camera.shutter_speed = camera.exposure_speed
             camera.exposure_mode = 'off'
             g = camera.awb_gains
             camera.awb_mode = 'off'
             camera.awb_gains = g
             camera.capture(filename)
           else:
             camera.capture(filename)
    else:
      subprocess.call("raspistill %s -w %s -h %s -t 200 -e jpg -q %s -n -o %s" % (settings, width, height, quality, filename), shell=True)

    if showDateOnImage:
      writeDateToImage(filename,imageTagName)
      print "%s - %s saved %s" % (progname, imageTagName, filename)
      imageNow= filepath + "/" + filenamePrefix + "_current.jpg"
      shutil.copy(filename,imageNow)

# Keep free space above given level
def keepDiskSpaceFree(bytesToReserve):
    if (getFreeSpace() < bytesToReserve):
        for filename in sorted(os.listdir(filepath + "/")):
            if filename.startswith(filenamePrefix) and filename.endswith(".jpg"):
                os.remove(filepath + "/" + filename)
                print "%s - Deleted %s/%s to avoid filling disk" % (progname,filepath,filename)
                if (getFreeSpace() > bytesToReserve):
                    return

# Write Date to Image
def writeDateToImage(imagename,datetoprint):
    FOREGROUND = (255, 255, 255)
    TEXT = datetoprint
    font_path = '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf'
    font = ImageFont.truetype(font_path, 24, encoding='unic')
    text = TEXT.decode('utf-8')
    img = Image.open(imagename)
    draw = ImageDraw.Draw(img)
    # draw.text((x, y),"Sample Text",(r,g,b))

    draw.text((500, 930),text,FOREGROUND,font=font)
    img.save(imagename)
    return

# Get available disk space
def getFreeSpace():
    st = os.statvfs(filepath + "/")
    du = st.f_bavail * st.f_frsize
    return du

# Get first image
image1, buffer1 = captureTestImage(cameraSettings, testWidth, testHeight)

# Reset last capture time
lastCapture = time.time()

if numsequence:
    if not os.path.exists(countpath):
        print "%s - Creating New Counter File %s Counter=%i" % (progname, countpath,startCount)
        open(countpath, 'w').close()
        f = open(countpath, 'w+')
        f.write(str(startCount))
        f.close()

    with open(countpath, 'r') as f:
        writeCount = f.read()
        f.closed
    currentCount = int(writeCount) + 1
    if (currentCount > startCount + maxPhotos):
        currentCount = startCount


print "---------------------------------- Settings -----------------------------------------"
print "    Motion .... Sensitivity=%i Threshold=%i Cam-Settings= %s ForceCapture=%s every %i seconds"  % (sensitivity, threshold, cameraSettings, forceCapture, forceCaptureTime)
print "    Image ..... W=%i H=%i Quality=%i DateOnImage=%s Prefix=%s Path=%s" % (saveWidth, saveHeight, saveQuality, showDateOnImage, filenamePrefix, filepath)
if numsequence:
  print "    Numbering . On=%s Start=%s Max=%i path=%s Counter=%i" % (numsequence, startCount, maxPhotos, countpath, currentCount)
else:
  print "    Numbering . On=%s  Image Number Sequence is Off" % (numsequence)
print "    Sync File . On=%s Path=%s" % (createLockFile, lockfilepath)
print "    DiskSpace . Reserved=%i mb" % (mbToReserve)
print "    Debug ..... On=%s Path=%s/debug.bmp" % (debugMode, filepath)
print "-------------------------------------------------------------------------------------"
starttime = datetime.datetime.now()
rightnow = "%04d%02d%02d-%02d:%02d:%02d" % (starttime.year, starttime.month, starttime.day, starttime.hour, starttime.minute, starttime.second)
print "%s - Waiting for First Motion %s ........" % (progname, rightnow)

# Start main motion capture loop
while (True):
  try:
    # Get comparison image
    image2, buffer2 = captureTestImage(cameraSettings, testWidth, testHeight)

    # Count changed pixels
    changedPixels = 0
    takePicture = False

    if (debugMode): # in debug mode, save a bitmap-file with marked changed pixels and with visible testarea-borders
        debugimage = Image.new("RGB",(testWidth, testHeight))
        debugim = debugimage.load()

    for z in xrange(0, testAreaCount): # = xrange(0,1) with default-values = z will only have the value of 0 = only one scan-area = whole picture
        for x in xrange(testBorders[z][0][0]-1, testBorders[z][0][1]): # = xrange(0,100) with default-values
            for y in xrange(testBorders[z][1][0]-1, testBorders[z][1][1]):   # = xrange(0,75) with default-values; testBorders are NOT zero-based, buffer1[x,y] are zero-based (0,0 is top left of image, testWidth-1,testHeight-1 is botton right)
                if (debugMode):
                    debugim[x,y] = buffer2[x,y]
                    if ((x == testBorders[z][0][0]-1) or (x == testBorders[z][0][1]-1) or (y == testBorders[z][1][0]-1) or (y == testBorders[z][1][1]-1)):
                        # print "Border %s %s" % (x,y)
                        debugim[x,y] = (0, 0, 255) # in debug mode, mark all border pixel to blue
                # Just check green channel as it's the highest quality channel
                pixdiff = abs(buffer1[x,y][1] - buffer2[x,y][1])
                if pixdiff > threshold:
                    changedPixels += 1
                    if (debugMode):
                        debugim[x,y] = (0, 255, 0) # in debug mode, mark all changed pixel to green
                # Save an image if pixels changed
                if (changedPixels > sensitivity):
                    takePicture = True # will shoot the photo later
                if ((debugMode == False) and (changedPixels > sensitivity)):
                    break  # break the y loop
            if ((debugMode == False) and (changedPixels > sensitivity)):
                break  # break the x loop
        if ((debugMode == False) and (changedPixels > sensitivity)):
            break  # break the z loop

    if (debugMode):
        debugimage.save(filepath + "/debug.bmp") # save debug image as bmp
        print "%s - Saved Debug to %s/debug.bmp  Changed Pixel=%i" % (progname, filepath, changedPixels)
    # else:
    #     print "%s changed pixel" % changedPixels

    # Check force capture
    if forceCapture:
        if time.time() - lastCapture > forceCaptureTime:
            takePicture = True

    if takePicture:
        lastCapture = time.time()
        if numsequence:
            fileCount = str(currentCount)
        saveImage(cameraSettings, saveWidth, saveHeight, saveQuality, diskSpaceToReserve)
        # increment image counter and reset to start if max reached
        if numsequence:
            currentCount += 1
            if (currentCount > startCount + maxPhotos):
                currentCount = startCount
            writeCount = str(currentCount)
            # write current photo counter to file
            if not os.path.exists(countpath):
                print "%s - Creating %s" % (progname,countpath)
                open(countpath, 'w').close()
            f = open(countpath, 'w+')
            f.write(str(writeCount))
            f.close()
        # write a lock file so sync script knows when there are files to process for gdrive
        if createLockFile:
            if not os.path.exists(lockfilepath):
                print "%s - Creating %s" % (progname, lockfilepath)
                open(lockfilepath, 'w').close()
            f = open(lockfilepath, 'w+')
            f.write("Photos available to sync with gdrive using sync shell script")
            f.close()

    # Swap comparison buffers
    image1  = image2
    buffer1 = buffer2
  finally:
    with picamera.PiCamera() as camera:
      camera.close()
