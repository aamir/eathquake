from aggregator import Place, LatLong
from data import Data

__author__ = 'aamir'

class Model:
    def __init__(self, days):
        self.days = days
        self.data_layer = Data(self.days)
        self.raw_data = []

    def get_data(self):
        self.raw_data = self.data_layer.get()


# Abstraction for just getting Place Data uses Model get_data
class PlaceData(Model):
    def __init__(self, days):
        Model.__init__(self, days)

    def get_data(self):
        self.raw_data = self.data_layer.get()
        # now return back place related stuff
        places_map = {}
        for d in self.raw_data:
            place = d['place']
            if "of" not in place:
                place = place.strip()
            else:
                place = place.split("of")[1].strip()

            if place not in places_map:
                places_map[place] = Place(place)

            places_map.get(place).add_magnitude(d['mag'])

        sorted_data = sorted(places_map.values(), key=lambda place: place.total_energy, reverse=True)
        return sorted_data


class LatLongData(Model):
    def __init__(self, days):
        Model.__init__(self, days)

    def get_data(self):
        self.raw_data = self.data_layer.get()
        # now return back latlong related stuff
        latlong_map = {}
        for d in self.raw_data:
            lon = 10 * round(d['lon']/10)
            lat = 10 * round(d['lat']/10)

            if (lat, lon) not in latlong_map:
                latlong_map[(lat, lon)] = LatLong(lat, lon)

            latlong_map.get((lat, lon)).add_magnitude(d['mag'])

        sorted_data = sorted(latlong_map.values(), key=lambda latlong: latlong.total_energy, reverse=True)
        return sorted_data

