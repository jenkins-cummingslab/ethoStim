export DISPLAY=:0.0
cd /home/pi/ethoStim/individualtesting
d=$(date --date='TZ="US/Central" Mon July 4 9:05:00 2016' +%s); python trial.py -f Layla -ps 8.png -ts 12 -d 11 -s 1 -fs none -x female -p 67 -sp gambusia -sl 367 -r 1 -cs R -c -m $d