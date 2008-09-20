import csv
import datetime
from dateutil import tz

one_meter_per_second_in_miles_per_hour = 2.23693629

class InstaMapperPosition():
    """A class to take a single InstaMapper string and return in a more usable format."""

    def make_timestamp(self):
        self.timestamp = datetime.datetime.utcfromtimestamp(self.timestamp_raw)
        self.timestamp = self.timestamp.replace(tzinfo=tz.gettz('UTC'))

    def make_miles_per_hour(self):
        self.speed_miles_per_hour = self.speed_meters_per_second * one_meter_per_second_in_miles_per_hour

    def __init__(self, value):
        reader = csv.reader([value,], quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            if row:
                if not row[0] == 'InstaMapper API v1.00':
                    self.device_key = row[0]
                    self.device_label = row[1]
                    self.timestamp_raw = float(row[2])
                    self.make_timestamp()
                    self.latitude = row[3]
                    self.longitude = row[4]
                    self.altitude_meters = row[5]
                    self.speed_meters_per_second = float(row[6])
                    self.make_miles_per_hour()
                    self.heading = row[7]

def _test():
    pass

if __name__ == '__main__':
    _test()
