from django.contrib.auth.models import User
from django.contrib.gis.db import models

class PositionReportSource(models.Model):
    name = models.CharField(max_length=64)
    display_on_maps = models.BooleanField(default=False)
    auto_import = models.BooleanField(default=True)
    auto_import_interval = models.IntegerField(null=True, blank=True)
    display_description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.name

class PositionReport(models.Model):
    timestamp_received = models.DateTimeField(null=True,blank=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
    heading = models.IntegerField(null=True, blank=True)
    altitude = models.IntegerField(null=True, blank=True)
    speed = models.IntegerField(null=True, blank=True)
    source = models.ForeignKey(PositionReportSource)
    quality = models.IntegerField('The receiver-generated "quality" of this particular report.', null=True, blank=True)
    satellites_visible = models.IntegerField('The number of satellites visible to the receiver', null=True, blank=True)
    hdop = models.CharField(max_length=10, null=True, blank=True)
    geoid_height_above_wgs84_meters = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    geoidal_seperation_meters = models.IntegerField(null=True, blank=True)
    time_since_dgps_update = models.CharField(max_length=10, null=True, blank=True)
    dgps_reference_station_id = models.CharField(max_length=10, null=True, blank=True)
    receiver_warning = models.NullBooleanField(null=True, blank=True)
    magnetic_variation = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    magnetic_variation_direction = models.CharField(max_length=1, null=True, blank=True)
    checksum_gpgga = models.CharField('$GPGGA Checksum', max_length=10, null=True, blank=True)
    checksum_gprmc = models.CharField('$GPRMC Checksum', max_length=10, null=True, blank=True)
    duration_seconds = models.IntegerField('Duration (seconds)', null=True, blank=True)
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    public = models.BooleanField(default=True)
    should_tumble = models.BooleanField(default=True)
    point = models.PointField(srid=4326, null=True, blank=True)

    objects = models.GeoManager()

    def get_bubble_text(self):
        bubble_text = 'Source: %s<br/>Received %s (Central)' % (self.source.name, self.timestamp_received)
        if self.speed != None and self.heading != None:
            bubble_text = '%s<br/>Compass Direction: %s degrees' % (bubble_text, self.heading)
        elif self.heading != None:
            bubble_text = '%s<br/>Compass Direction: %s degrees' % (bubble_text, self.speed, self.heading)
        if self.source.name == 'InstaMapper iPhone':
            bubble_text = '%s<br/>InstaMapper Available (Free) @ <a href=\'http://www.instamapper.com\'>instamapper.com</a>' % bubble_text
        return bubble_text

    def __unicode__(self):
        return u'Received %s, Lat/%s Lon/%s' % (self.timestamp_received, self.latitude, self.longitude)

class Location(models.Model):
    """A model for defining 'saved' positions of interest. The nearest_location templatetag will then attempt to find where you are (only looking within settings.)"""
    name = models.CharField(max_length=128)
    slug = models.SlugField()
    point = models.PointField(srid=4326)
    public = models.BooleanField()
# Future functionality
#    radius = models.IntegerField("The maximum distance (radius) a report can be from this location (in mi) before being considered 'there'")
#    poly = models.PolygonField() # for eventual growth - plan is that the point (with a circle drawn of radius self.radius) will be stored here, and the query will simplify to a position report's point IN location poly

    def __unicode__(self):
        return self.name

    objects = models.GeoManager()
