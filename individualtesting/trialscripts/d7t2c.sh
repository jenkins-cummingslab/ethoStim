export DISPLAY=:0.0
cd /home/pi/ethoStim/individualtesting
d=$(date --date='TZ="US/Central" May 24 11:05:00 2016' +%s); python trial.py -f Second -ps 12.png -ts 8  -d 7 -s 2 -fs none -x female -p 67 -sp gambusia -sl 367 -r 1 -c -m $d
