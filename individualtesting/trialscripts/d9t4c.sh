export DISPLAY=:0.0
cd /home/pi/ethoStim/individualtesting
d=$(date --date='TZ="US/Central" Sat July 2 15:05:00 2016' +%s); python trial.py -f Layla -ps 12.png -ts 6 -d 9 -s 4 -fs left -x female -p 50 -sp gambusia -sl 367 -r 1 -cs L -fd -c -m $d