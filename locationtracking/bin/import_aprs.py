import datetime
from dateutil import tz
from django.contrib.gis.geos import Point
from aprsworld_api.position.models import Position
from locationtracking.models import PositionReport, PositionReportSource

def retrieve_positions(callsign, user, since, source_name='APRSWorld'):
    source = PositionReportSource.objects.get_or_create(name=source_name)[0]

    positions = Position.objects.using('aprs').filter(source=callsign, packet_date__gte=since)

    for position in positions:
        packet_utc = position.packet_date.replace(tzinfo=tz.gettz('UTC'))
        
        report = PositionReport.objects.get_or_create(timestamp_received=packet_utc, source=source, user=user)[0]
        report.latitude = str(position.latitude)
        report.longitude = str(position.longitude)
        report.point = Point(position.longitude, position.latitude)
        report.heading = position.course
        # APRSworld stores speed in kph and altitude in m, but all the other APRS sites store in imperial units
        if position.speed:
            report.speed = position.speed * 0.621371192
        if position.altitude:
            report.altitude = position.altitude * 3.2808399
        report.save()

if __name__ == '__main__':
    """You should copy this code into your own APRS importer somewhere - then the
    callsign / user / positionreportsource can be changed if you want, and future
    changes to this file won't overwrite your modifications."""

    import datetime
    from django.contrib.auth.models import User

    callsign = 'N0CALL'
    user = User.objects.get(username='user')

    try:
        last_position = PositionReport.objects.filter(user=user, source=PositionReportSource.objects.get_or_create(name='APRSWorld')[0]).order_by('-timestamp_received')[0]
        retrieve_positions(callsign, user, last_position.timestamp_received) # ask for anything after the last one we have
    except IndexError:
        retrieve_positions(callsign, user, datetime.datetime(2001, 1, 1)) # way in the past if nothing for that source was found
