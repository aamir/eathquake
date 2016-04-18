__author__ = 'aamir'
import argparse
from model import LatLongData
from model import PlaceData

def get_latlong(days):
    latlong_data = LatLongData(int(days)).get_data()
    display(latlong_data)

def get_places(days):
    places_data = PlaceData(int(days)).get_data()
    display(places_data)

def display(data):
    i = 0
    print "REGION" + "\t" + "EARTHQUAKE_COUNT" + "\t" + "TOTAL MAGNITUDE"
    while i != 10:
        print data[i]
        i += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', help='Number of days back from the current time to consider. Defaults to 30', default=30)
    parser.add_argument('--region', help="Either 'latlong' or 'name', if latlong is specified, regions are defined"
                                              " according to block of latitude/longitude, if 'name' is specified, "
                                              "regions are defined according to place name.Defaults to 'name'", default="name")
    args = vars(parser.parse_args())

    if args['region'] == 'name':
        get_places(args['days'])
    if args['region'] == 'latlong':
        get_latlong(args['days'])


