from south.db import db
from django.db import models
from locationtracking.models import *

class Migration:
    def forwards(self, orm):
        # Adding model 'PositionReportSource'
        db.create_table('locationtracking_positionreportsource', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=64)),
            ('display_on_maps', models.BooleanField(default=False)),
            ('auto_import', models.BooleanField(default=True)),
            ('auto_import_interval', models.IntegerField(null=True, blank=True)),
            ('display_description', models.TextField(null=True, blank=True)),
        ))
        db.send_create_signal('locationtracking', ['PositionReportSource'])

        # Adding model 'PositionReport'
        db.create_table('locationtracking_positionreport', (
            ('id', models.AutoField(primary_key=True)),
            ('timestamp_received', models.DateTimeField(null=True, blank=True)),
            ('latitude', models.DecimalField(null=True, max_digits=11, decimal_places=6, blank=True)),
            ('longitude', models.DecimalField(null=True, max_digits=11, decimal_places=6, blank=True)),
            ('heading', models.IntegerField(null=True, blank=True)),
            ('altitude', models.IntegerField(null=True, blank=True)),
            ('speed', models.IntegerField(null=True, blank=True)),
            ('source', models.ForeignKey(orm.PositionReportSource)),
            ('quality', models.IntegerField('The receiver-generated "quality" of this particular report.', null=True, blank=True)),
            ('satellites_visible', models.IntegerField('The number of satellites visible to the receiver', null=True, blank=True)),
            ('hdop', models.CharField(max_length=10, null=True, blank=True)),
            ('geoid_height_above_wgs84_meters', models.DecimalField(null=True, max_digits=10, decimal_places=3, blank=True)),
            ('geoidal_seperation_meters', models.IntegerField(null=True, blank=True)),
            ('time_since_dgps_update', models.CharField(max_length=10, null=True, blank=True)),
            ('dgps_reference_station_id', models.CharField(max_length=10, null=True, blank=True)),
            ('receiver_warning', models.NullBooleanField(null=True, blank=True)),
            ('magnetic_variation', models.DecimalField(null=True, max_digits=10, decimal_places=3, blank=True)),
            ('magnetic_variation_direction', models.CharField(max_length=1, null=True, blank=True)),
            ('checksum_gpgga', models.CharField('$GPGGA Checksum', max_length=10, null=True, blank=True)),
            ('checksum_gprmc', models.CharField('$GPRMC Checksum', max_length=10, null=True, blank=True)),
            ('duration_seconds', models.IntegerField('Duration (seconds)', null=True, blank=True)),
            ('user', models.ForeignKey(orm['auth.User'])),
            ('timestamp', models.DateTimeField(auto_now_add=True)),
            ('active', models.BooleanField(default=False)),
            ('public', models.BooleanField(default=True)),
            ('should_tumble', models.BooleanField(default=True)),
        ))
        db.send_create_signal('locationtracking', ['PositionReport'])

    def backwards(self, orm):
        # Deleting model 'PositionReportSource'
        db.delete_table('locationtracking_positionreportsource')

        # Deleting model 'PositionReport'
        db.delete_table('locationtracking_positionreport')

    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'locationtracking.positionreportsource': {
            'auto_import': ('models.BooleanField', [], {'default': 'True'}),
            'auto_import_interval': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'display_description': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'display_on_maps': ('models.BooleanField', [], {'default': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '64'})
        },
        'locationtracking.positionreport': {
            'active': ('models.BooleanField', [], {'default': 'False'}),
            'altitude': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'checksum_gpgga': ('models.CharField', ["'$GPGGA Checksum'"], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'checksum_gprmc': ('models.CharField', ["'$GPRMC Checksum'"], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'dgps_reference_station_id': ('models.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'duration_seconds': ('models.IntegerField', ["'Duration (seconds)'"], {'null': 'True', 'blank': 'True'}),
            'geoid_height_above_wgs84_meters': ('models.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'geoidal_seperation_meters': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hdop': ('models.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'heading': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('models.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6', 'blank': 'True'}),
            'longitude': ('models.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6', 'blank': 'True'}),
            'magnetic_variation': ('models.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'magnetic_variation_direction': ('models.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'public': ('models.BooleanField', [], {'default': 'True'}),
            'quality': ('models.IntegerField', ['\'The receiver-generated "quality" of this particular report.\''], {'null': 'True', 'blank': 'True'}),
            'receiver_warning': ('models.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'satellites_visible': ('models.IntegerField', ["'The number of satellites visible to the receiver'"], {'null': 'True', 'blank': 'True'}),
            'should_tumble': ('models.BooleanField', [], {'default': 'True'}),
            'source': ('models.ForeignKey', ["orm['locationtracking.PositionReportSource']"], {}),
            'speed': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'time_since_dgps_update': ('models.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'timestamp_received': ('models.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {})
        }
    }

    complete_apps = ['locationtracking']
