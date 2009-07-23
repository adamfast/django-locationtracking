import re
from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.measure import D
from django.shortcuts import get_object_or_404
from django.template import resolve_variable, Variable

from locationtracking.models import Location

register = template.Library()

class NearestLocationNode(template.Node):
    def __init__(self, positionreport, var_name):
        self.positionreport = Variable(positionreport)
        self.var_name = var_name

    def render(self, context):
        report = self.positionreport.resolve(context)
        try:
            location = Location.objects.filter(point__distance_lte=(report.point, D(mi=settings.MAXIMUM_LOCATION_DISTANCE)), public=True).distance(report.point).order_by('distance')[0]
        except:
            location = None
        context[self.var_name] = location
        context['google_maps_api_key'] = getattr(settings, 'GOOGLE_MAPS_KEY', 'not-set')
        return ''

def get_location(parser, token):
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]

    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    user, var_name = m.groups()
    return NearestLocationNode(user, var_name)
register.tag('get_location', get_location)
