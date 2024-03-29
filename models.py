# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Bookmark(models.Model):
    bookmark_student = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)
    bookmark_marker = models.ForeignKey('Marker', models.DO_NOTHING)
    createtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bookmark'
        unique_together = (('bookmark_student', 'bookmark_marker'),)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    content = models.TextField(blank=True, null=True)
    comment_marker = models.ForeignKey('Marker', models.DO_NOTHING, blank=True, null=True)
    comment_student = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    createtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'


class CommentLike(models.Model):
    cl_comment = models.OneToOneField(Comment, models.DO_NOTHING, primary_key=True)
    cl_student = models.ForeignKey('User', models.DO_NOTHING)
    islike = models.IntegerField(db_column='isLike', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment_like'
        unique_together = (('cl_comment', 'cl_student'),)


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    eventname = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    starttime = models.DateTimeField(blank=True, null=True)
    endtime = models.DateTimeField(blank=True, null=True)
    polygon = models.TextField(blank=True, null=True)
    student = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    createtime = models.DateTimeField(blank=True, null=True)
    enable = models.IntegerField(blank=True, null=True)
    event_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event'


class EventBookmark(models.Model):
    event_bookmark_event = models.OneToOneField(Event, models.DO_NOTHING, primary_key=True)
    event_bookmark_student = models.ForeignKey('User', models.DO_NOTHING)
    createtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_bookmark'
        unique_together = (('event_bookmark_event', 'event_bookmark_student'),)


class EventLike(models.Model):
    event_like_event = models.OneToOneField(Event, models.DO_NOTHING, primary_key=True)
    event_like_student = models.ForeignKey('User', models.DO_NOTHING)
    createtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_like'
        unique_together = (('event_like_event', 'event_like_student'),)


class EventUrl(models.Model):
    event_url = models.OneToOneField(Event, models.DO_NOTHING, primary_key=True)
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_url'


class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    marker = models.ForeignKey('Marker', models.DO_NOTHING)
    link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'image'


class ImageEvent(models.Model):
    image_id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, models.DO_NOTHING)
    link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'image_event'


class Marker(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    place = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=45, blank=True, null=True)
    enable = models.IntegerField(blank=True, null=True)
    createtime = models.DateTimeField(blank=True, null=True)
    created_user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'marker'


class MarkerLike(models.Model):
    markerlike_student = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)
    markerlike_marker = models.ForeignKey(Marker, models.DO_NOTHING)
    createtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'marker_like'
        unique_together = (('markerlike_student', 'markerlike_marker'),)


class Permission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    permission_student = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    createtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permission'


class PermissionMarker(models.Model):
    pm_permission = models.OneToOneField(Permission, models.DO_NOTHING, primary_key=True)
    pm_maker = models.ForeignKey(Marker, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permission_marker'


class ReportEvent(models.Model):
    report_event_id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, models.DO_NOTHING)
    reason = models.CharField(max_length=255, blank=True, null=True)
    details = models.CharField(max_length=450, blank=True, null=True)
    created_user = models.ForeignKey('User', models.DO_NOTHING, db_column='created_user')
    created_time = models.DateTimeField(blank=True, null=True)
    enable = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report_event'


class ReportMarker(models.Model):
    report_marker_id = models.AutoField(primary_key=True)
    id = models.ForeignKey(Marker, models.DO_NOTHING, db_column='id')
    reason = models.CharField(max_length=255, blank=True, null=True)
    details = models.CharField(max_length=450, blank=True, null=True)
    created_user = models.ForeignKey('User', models.DO_NOTHING, db_column='created_user')
    created_time = models.DateTimeField(blank=True, null=True)
    enable = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report_marker'


class User(models.Model):
    student_id = models.IntegerField(primary_key=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=1280, blank=True, null=True)
    faculty = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
