import re
from django import template
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from locationtracking.models import PositionReport

register = template.Library()

class LatestPositionReportNode(template.Node):
    def __init__(self, user, var_name):
        user_obj = get_object_or_404(User, username__exact=user)
        self.user = user_obj
        self.var_name = var_name

    def render(self, context):
        try:
            report = PositionReport.objects.filter(user__exact=self.user).order_by('-timestamp_received')[0]
        except:
            report = None
        context[self.var_name] = report
        return ''

def get_latest_position(parser, token):
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
    return LatestPositionReportNode(user, var_name)
register.tag('get_latest_position', get_latest_position)
