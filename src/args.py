import os
import argparse
import re

def get_SV_id(url:str):
    # get street view id from the url
    found = re.search(r'data=![a-zA-Z0-9]{3}![a-zA-Z0-9]{3}![a-zA-Z0-9]{3}![a-zA-Z0-9]{2}([^!]+)', url)
    return found.group(1) if found else None

def get_args():

    ap = argparse.ArgumentParser()

    ap.add_argument("--urls",
                    metavar="URLS", type=str, default=None,
                    help="Takes in a url or list of urls separated by a comma.")

    ap.add_argument("--from-file",
                    metavar="FILE", type=str, default=None,
                    help="Reads in a file of urls or street view ids separated by new lines. Lines starting with # will not be read in.")

    ap.add_argument("--street-view-ids",
                    metavar="IDS", type=str, default=None,
                    help="Takes in a street view id or list of street view ids separated by a comma.")

    ap.add_argument("--output-path",
                    metavar="ID", type=str, default=os.getcwd(),
                    help="The output path where images are downloaded.")

    ap.add_argument("--zoom",
                    metavar="VALUE", type=int, default=4,
                    help="The zoom level of the street view image. (default: 4)")

    ap.add_argument("--overwrite",
                    action='store_true', default=False,
                    help="Overwrite any previously created files.")

    ap.add_argument("--retry",
                    metavar="COUNT", type=int, default=5,
                    help="The amount of times to retry downloading. (default: 5)")

    args = vars(ap.parse_args())

    if not os.path.exists(args['output_path']):
        raise Exception(f"File path does not exist: {args['output_path']}")

    # only zoom levels from 1-5 are allowed
    if 5 < args['zoom'] < 0:
        raise Exception(f"Incorrect zoom size: {args['zoom']}, only sizes 1-5 are allowed.")

    SV_IDs = []

    # takes a comma seperated string of urls and converts them to a list of street view ids
    if args['urls']:
        for s in args["urls"].split(","):
            SV_id = get_SV_id(s.strip())
            if SV_id:
                SV_IDs.append(SV_id)
            else:
                print(f"Invalid URL: {s.strip()}")

    # takes a file and converts it to a list
    if args['from_file']:

        if not os.path.exists(args['from_file']):
            print(f"--from-file {args['from_file']} does not exist")

        with open(args['from_file'],'r') as f:
            for line in f:
                if line[0] != '#' and line.strip() != '':
                    SV_id = get_SV_id(line.strip())
                    if SV_id:
                        SV_IDs.append(SV_id)
                    else:
                        print(f"Invalid URL or Street View ID: {line.strip()}")

    # takes a comma seperated string of street view ids and converts them to a list of street view ids
    if args['street_view_ids']:
        for s in args["street-view-ids"].split(","):
            SV_IDs.append(s.strip())

    args['street-view-ids'] = SV_IDs

    return args