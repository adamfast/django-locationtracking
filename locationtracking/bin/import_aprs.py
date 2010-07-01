from dateutil import tz
from django.contrib.gis.geos import Point
from aprsworld_api.position.models import Position
from locationtracking.models import PositionReport, PositionReportSource

def retrieve_positions(callsign, user, since):
    source = PositionReportSource.objects.get_or_create(name='APRSWorld')[0]

    positions = Position.objects.using('aprs').filter(source=callsign, packet_date__gte=since)

    for position in positions:
        packet_utc = position.packet_date.replace(tzinfo=tz.gettz('UTC'))
        
        report = PositionReport.objects.get_or_create(timestamp_received=packet_utc, source=source, user=user)[0]
        report.latitude = str(position.latitude)
        report.longitude = str(position.longitude)
        report.point = Point(position.longitude, position.latitude)
        report.heading = position.course
        report.speed = position.speed
        report.altitude = position.altitude
        report.save()

if __name__ == '__main__':
    import datetime
    from django.contrib.auth.models import User

    callsign = 'N0CALL'
    user = User.objects.get(username='user')

    last_position = PositionReport.objects.filter(user=user, source=PositionReportSource.objects.get_or_create(name='APRSWorld')[0]).order_by('-timestamp_received')[:1]

    retrieve_positions(callsign, user, last_position.timestamp_received) # ask for anything after the last one we have
