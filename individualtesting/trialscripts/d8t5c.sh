export DISPLAY=:0.0
cd /home/pi/ethoStim/individualtesting
d=$(date --date='TZ="US/Central" Fri July 1 17:05:00 2016' +%s); python trial.py -f Layla -ps 6.png -ts 12 -d 8 -s 5 -fs left -x female -p 50 -sp gambusia -sl 367 -r 1 -cs L -c -m $d