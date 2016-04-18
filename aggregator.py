__author__ = 'aamir'
import math
class Aggregator:
    def __init__(self):
        self.magnitude = []
        self.max_mag = 0
        self.count = 0
        self.total_energy = 0
        self.max_energy = 0

    def add_magnitude(self, magnitude):
        self.count += 1
        self.magnitude.append(magnitude)
        if self.max_mag < magnitude:
            self.max_mag = magnitude
        self.calculate_energy(magnitude)

    def calculate_energy(self, magnitude):
        if magnitude:
            temp = (10**magnitude)
            self.total_energy += temp
            if self.max_energy < temp:
                self.max_energy = temp


class Place(Aggregator):
    def __init__(self, place):
        self.place = place
        Aggregator.__init__(self)

    def __repr__(self):
        return self.place + "\t" + str(self.count) + "\t" + str(math.log10(self.total_energy/self.count))


class LatLong(Aggregator):
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        Aggregator.__init__(self)

    def __repr__(self):
        return "( " + str(self.lat) + str(self.lon) + " )" + "\t" + str(math.log10(self.total_energy/self.count))
