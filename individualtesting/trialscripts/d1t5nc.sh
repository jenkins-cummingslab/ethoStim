export DISPLAY=:0.0
cd /home/pi/ethoStim/individualtesting
d=$(date --date='TZ="US/Central" Sun September 18 17:05:00 2016' +%s); python trial.py -f Lynn -ps 0.png -ts 0 -d 1 -s 5 -fs both -x female -p 0 -sp gambusia -sl TBD -r 6 -cs B -fd -m $d
