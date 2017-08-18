import json
import argparse
import sys
import os

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-sd","--startdate", help="Date to start scheduling trials, format is MM/DD.", required=True)
    ap.add_argument("-r", "--round",help="A number.", required=True)
    ap.add_argument("-hs", "--hsched", help="Which high schedule to use (e.g. H1, H2, H3)", required=True)
    ap.add_argument("-ls", "--lsched", help="Which low schedule to use (e.g. H1, H2, H3)", required=True)
    ap.add_argument("-h1", "--hfish1", help="1st Fish that will be assigned H schedule", required=True)
    ap.add_argument("-h2", "--hfish2", help="2nd Fish that will be assigned H schedule", required=True)
    ap.add_argument("-h3", "--hfish3", help="3rd Fish that will be assigned H schedule", required=True)
    ap.add_argument("-l1", "--lfish1", help="1st Fish that will be assigned L schedule", required=True)
    ap.add_argument("-l2", "--lfish2", help="2nd Fish that will be assigned L schedule", required=True)
    ap.add_argument("-l3", "--lfish3", help="3rd Fish that will be assigned L schedule", required=True)

    args = vars(ap.parse_args())

    a_dict = {"startDate": args["startdate"], "round": args["round"], "h_schedule": args["hsched"], "l_schedule": args["lsched"], "mapping": {"H": { "fish1" : args["hfish1"], "fish2": args["hfish2"], "fish3": args["hfish3"]}, "L": { "fish1" : args["lfish1"], "fish2": args["lfish2"], "fish3": args["lfish3"]}}}

    #print a_dict

    os.remove('top.json')

    with open('top.json', 'w') as f:
        json.dump(a_dict, f, sort_keys=True, indent=4, separators=(',', ': '))

    sys.exit(0)
