sudo service ntp stop
sudo ntpdate -s -u -b pool.ntp.org
sudo sevice ntp start

cd /home/pi/source/wall-clock

git pull

cd wall-clock

python piClock.py