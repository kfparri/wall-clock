sudo service ntp stop
sudo ntpdate -s -u -b pool.ntp.org
sudo sevice ntp start

cd /home/pi/source/wall-clock

git pull

cd wall-clock

# update the splash screen 
sudo mv /usr/share/plymouth/themes/pix/splash.png /usr/share/plymouth/themes/pix/splash.png.bak
sudo cp splash.png /usr/share/plymouth/themes/pix/splash.png

python piClock.py