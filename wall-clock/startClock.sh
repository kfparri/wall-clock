sudo ntpdate -u pool.ntp.org

cd /home/pi/source/wall-clock

git pull

cd wall-clock

python piClock.py