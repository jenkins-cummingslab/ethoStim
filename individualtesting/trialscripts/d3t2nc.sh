export DISPLAY=:0.0
cd /home/pi/ethoStim/individualtesting
d=$(date --date='TZ="US/Central" May 20 11:05:00 2016' +%s); python trial.py -f Second -ps 6.png -ts 12 -d 3 -s 2 -fs right-x female -p 50 -sp gambusia -sl 367 -r 1  -m $d
