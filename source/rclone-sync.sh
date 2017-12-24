#!/bin/bash
progName=$(basename -- "$0")
echo "$progName ver 1.1  written by Claude Pageau"

# Customize rclone sync variables Below
# ---------------------------------------
rcloneName="gdmedia"
syncRoot="/home/pi/pi-motion"
localSyncDir="images"
remoteSyncDir="pi-motion/images"
# ---------------------------------------

# Display Users Settings
echo "
---------- SETTINGS -------------
rcloneName   : $rcloneName
syncRoot     : $syncRoot
localSyncDir : $localSyncDir
remoteSyncDir: $remoteSyncDir
---------------------------------"
if pidof -o %PPID -x "$progName"; then
    echo "WARN  - $progName Already Running. Only One Allowed."
else
    echo "cd $syncRoot"
    cd "$syncRoot"
    echo "/usr/bin/rclone sync -v $localSyncDir $rcloneName:$remoteSyncDir"
    echo "One Moment Please ..."
    /usr/bin/rclone sync -v $localSyncDir $rcloneName:$remoteSyncDir
fi
echo "$progName Bye ..."

