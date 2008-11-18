import urllib2
from django.conf import settings
from django.contrib.auth.models import User
from locationtracking.models import PositionReport, PositionReportSource
from locationtracking.instamapper import InstaMapperPosition

MAXIMUM_POSITIONS = 100

def import_positions(user, api_key):
    SOURCE_URL = 'http://www.instamapper.com/api?action=getPositions&key=%s&num=%s' % (api_key, MAXIMUM_POSITIONS)

    if getattr(settings, 'INSTAMAPPER_SOURCE_NAME', False):
        source_list = PositionReportSource.objects.filter(name=settings.INSTAMAPPER_SOURCE_NAME)
        if source_list:
            source = source_list[0]
        else:
            print('You do not have a %s source defined in your database.' % settings.INSTAMAPPER_SOURCE_NAME)
    else:
        print('You forgot to set INSTAMAPPER_SOURCE_NAME in your settings file.')

    request = urllib2.Request(SOURCE_URL, None, {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})
    response = urllib2.urlopen(request)
    html = response.read()

    html_broken = html.split('\n')
    for line in html_broken:
        if line != 'InstaMapper API v1.00' and line != '':
            position = InstaMapperPosition(line)

            dupe_list = PositionReport.objects.filter(timestamp_received__exact=position.timestamp, source__exact=source, user__exact=user)
            if not dupe_list:
                report = PositionReport()
                report.user = user
                report.timestamp_received = position.timestamp
                report.latitude = position.latitude
                report.longitude = position.longitude
                report.heading = position.heading
                report.speed = position.speed_miles_per_hour
                report.altitude = position.altitude
                report.source = source
                report.active = True
                report.should_tumble = False
                report.save()


def main():
    if getattr(settings, 'INSTAMAPPER_USER', False):
        user = User.objects.filter(username__exact=settings.INSTAMAPPER_USER)[0]

        if getattr(settings, 'INSTAMAPPER_API_KEY', False):
            import_positions(user, settings.INSTAMAPPER_API_KEY)
        else:
            print('You forgot to set INSTAMAPPER_API_KEY in your settings file.')
    else:
        print('You forgot to set INSTAMAPPER_USER in your settings file.')

if __name__ == '__main__':
    main()
