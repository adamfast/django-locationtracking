from datetime import datetime, timedelta
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import date as date_filter
from locationtracking.models import PositionReport

NON_DATE_REPORT_LIMIT = 25

def track(request, start_date=None, end_date=None):
    if (start_date and end_date) and (start_date != end_date):
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        position_list = PositionReport.objects.filter(timestamp_received__gt=start, timestamp_received__lt=end, source__display_on_maps=True).order_by('-timestamp_received')
        map_info_string = 'Showing the positions received from %s to %s' % (date_filter(start), date_filter(end))
    elif (start_date and not end_date) or ((start_date == end_date) and start_date):
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = start + timedelta(days=1)
        position_list = PositionReport.objects.filter(timestamp_received__gt=start, timestamp_received__lt=end, source__display_on_maps=True).order_by('-timestamp_received')
        map_info_string = 'Showing the positions received %s' % date_filter(start)
    else:
        position_list = PositionReport.objects.filter(source__display_on_maps=True).order_by('-timestamp_received')[:NON_DATE_REPORT_LIMIT]
        map_info_string = 'Showing the last %s positions received' % NON_DATE_REPORT_LIMIT

    return render_to_response('largemap.html',
    {
        'map_info': map_info_string,
        'positions': position_list,
        'google_maps_api_key': getattr(settings, 'GOOGLE_MAPS_KEY', 'not-set'),
    }, context_instance=RequestContext(request))
