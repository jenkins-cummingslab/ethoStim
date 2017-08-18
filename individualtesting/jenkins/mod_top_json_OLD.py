import json
import argparse
import sys
import os

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-sd","--startdate", help="Date to start scheduling trials, format is MM/DD.", required=True)
    ap.add_argument("-r", "--round",help="A number.", required=True)
    ap.add_argument("-h1", "--h1fish", help="Fish that will be assigned H1 schedule", required=True)
    ap.add_argument("-h2", "--h2fish", help="Fish that will be assigned H2 schedule", required=True)
    ap.add_argument("-h3", "--h3fish", help="Fish that will be assigned H3 schedule", required=True)
    ap.add_argument("-l1", "--l1fish", help="Fish that will be assigned L1 schedule", required=True)
    ap.add_argument("-l2", "--l2fish", help="Fish that will be assigned L2 schedule", required=True)
    ap.add_argument("-l3", "--l3fish", help="Fish that will be assigned L3 schedule", required=True)

    args = vars(ap.parse_args())

    a_dict = {"startDate": args["startdate"], "round": args["round"], "mapping": {"H1": args["h1fish"], "H2": args["h2fish"], "H3": args["h3fish"], "L1": args["l1fish"], "L2": args["l2fish"], "L3": args["l3fish"],}}

    #print a_dict

    os.remove('top.json')

    with open('top.json', 'w') as f:
        json.dump(a_dict, f, sort_keys=True, indent=4, separators=(',', ': '))

    sys.exit(0)
