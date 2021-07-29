sudo service ntp stop
sudo ntpdate -s -u -b pool.ntp.org
sudo service ntp start

cd /home/pi/source/wall-clock

git pull

cd wall-clock

# update the splash screen 
# information for this was found here: https://www.raspberrypi.org/forums/viewtopic.php?t=197472
sudo mv /usr/share/plymouth/themes/pix/splash.png /usr/share/plymouth/themes/pix/splash.png.bak
sudo cp splash.png /usr/share/plymouth/themes/pix/splash.png

// make sure you install requests
//  pip install requests
python piClock.py