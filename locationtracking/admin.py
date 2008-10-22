from django.contrib import admin
from models import PositionReport, PositionReportSource

class PositionReportSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_on_maps',)
    list_filter = ('display_on_maps',)

class PositionReportAdmin(admin.ModelAdmin):
    list_display = ('timestamp_received', 'user', 'source', 'latitude', 'longitude', 'altitude', 'speed', 'public', 'should_tumble', 'duration_seconds')
    list_filter = ('public', 'source',)
    fieldsets = (
        (None, {
            'fields': (
                'timestamp_received', 'latitude', 'longitude', 'heading', 'altitude', 'speed', 'source', 'user', 'active', 'public', 'should_tumble'
            )},
        ),
        ('Logger-only', {
            'fields': (
                'quality', 'satellites_visible', 'hdop', 'geoid_height_above_wgs84_meters', 'geoidal_seperation_meters', 'time_since_dgps_update',
                'dgps_reference_station_id', 'checksum_gpgga', 'checksum_gprmc', 'receiver_warning', 'magnetic_variation',
                'magnetic_variation_direction', 'duration_seconds',
            )},
        ),
    )


admin.site.register(PositionReportSource, PositionReportSourceAdmin)
admin.site.register(PositionReport, PositionReportAdmin)
