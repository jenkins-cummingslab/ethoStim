export DISPLAY=:0.0
cd /home/pi/ethoStim/individualtesting
d=$(date --date='TZ="US/Central" May 23 9:05:00 2016' +%s); python trial.py -f Second -ps 14.png -ts 7 -d 6 -s 1 -fs none -x female -p 50 -sp gambusia -sl 367 -r 1 -m $d