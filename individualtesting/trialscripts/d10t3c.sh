export DISPLAY=:0.0
cd /home/pi/ethoStim/individualtesting
d=$(date --date='TZ="US/Central" Sun July 3 13:05:00 2016' +%s); python trial.py -f Layla -ps 7.png -ts 14 -d 10 -s 3 -fs none -x female -p 50 -sp gambusia -sl 367 -r 1 -cs R -c -m $d