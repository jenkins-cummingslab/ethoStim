export DISPLAY=:0.0
cd /home/pi/ethoStim/individualtesting
d=$(date --date='TZ="US/Central" Fri July 1 11:05:00 2016' +%s); python trial.py -f Layla -ps 5.png -ts 10 -d 8 -s 2 -fs right -x female -p 50 -sp gambusia -sl 367 -r 1 -cs R -fd -c -m $d