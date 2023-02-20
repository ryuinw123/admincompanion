from django.db import models
from api.managers import AndroidDatabaseManager
    
# Create your models here.



class Admin(models.Model):
    username = models.CharField(primary_key=True, max_length=255)
    password = models.CharField(max_length=255)

    objects = AndroidDatabaseManager()

    class Meta:
        managed = False
        db_table = 'admin'


class Bookmark(models.Model):
    bookmark_student = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)
    bookmark_marker = models.ForeignKey('Marker', models.DO_NOTHING)
    createtime = models.DateTimeField(blank=True, null=True)

    objects = AndroidDatabaseManager()

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

    objects = AndroidDatabaseManager()

    class Meta:
        managed = False
        db_table = 'comment'


class CommentLike(models.Model):
    cl_comment = models.OneToOneField(Comment, models.DO_NOTHING, primary_key=True)
    cl_student = models.ForeignKey('User', models.DO_NOTHING)
    islike = models.IntegerField(db_column='isLike', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(blank=True, null=True)

    objects = AndroidDatabaseManager()

    class Meta:
        managed = False
        db_table = 'comment_like'
        unique_together = (('cl_comment', 'cl_student'),)


class Emergency(models.Model):
    contact_id = models.AutoField(primary_key=True)
    contact_number = models.CharField(max_length=45, blank=True, null=True)
    contact_name = models.CharField(max_length=45, blank=True, null=True)
    contact_admin_username = models.ForeignKey(Admin, models.DO_NOTHING, db_column='contact_admin_username', blank=True, null=True)
    createdtime = models.DateTimeField(blank=True, null=True)

    objects = AndroidDatabaseManager()

    class Meta:
        managed = False
        db_table = 'emergency'


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

    objects = AndroidDatabaseManager()

    class Meta:
        managed = False
        db_table = 'event'





class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    marker = models.ForeignKey('Marker', models.DO_NOTHING)
    link = models.TextField(blank=True, null=True)

    objects = AndroidDatabaseManager()

    class Meta:
        managed = False
        db_table = 'image'



class Issue(models.Model):
    issue_id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    imageurl = models.TextField(blank=True, null=True)
    createtime = models.DateTimeField(blank=True, null=True)
    issue_user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    issue_marker = models.ForeignKey('Marker', models.DO_NOTHING, blank=True, null=True)
    issue_approve_admin_username = models.ForeignKey(Admin, models.DO_NOTHING, db_column='issue_approve_admin_username',related_name='issue_approve_admin_username', blank=True, null=True)
    issue_broadcast_admin_username = models.ForeignKey(Admin, models.DO_NOTHING, db_column ='issue_broadcast_admin_username',related_name='issue_broadcast_admin_username', blank=True, null=True)
    broadcasttime = models.DateTimeField(blank=True, null=True)
    approvetime = models.DateTimeField(blank=True, null=True)

    objects = AndroidDatabaseManager()

    class Meta:
        managed = False
        db_table = 'issue'

    
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

    objects = AndroidDatabaseManager()

    class Meta:
        managed = False
        db_table = 'marker'


class MarkerLike(models.Model):
    markerlike_student = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)
    markerlike_marker = models.ForeignKey(Marker, models.DO_NOTHING)
    createtime = models.DateTimeField(blank=True, null=True)

    objects = AndroidDatabaseManager()

    class Meta:
        managed = False
        db_table = 'marker_like'
        unique_together = (('markerlike_student', 'markerlike_marker'),)


class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    header = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    imageurl = models.TextField(blank=True, null=True)
    createdtime = models.DateTimeField(blank=True, null=True)
    n_created_admin_username = models.ForeignKey(Admin, models.DO_NOTHING, db_column='n_created_admin_username',related_name='n_created_admin_username', blank=True, null=True)
    n_broadcast_admin_username = models.ForeignKey(Admin, models.DO_NOTHING, db_column="n_broadcast_admin_username",related_name ='n_broadcast_admin_username', blank=True, null=True)
    broadcasttime = models.DateTimeField(blank=True, null=True)

    objects = AndroidDatabaseManager()

    class Meta:
        managed = False
        db_table = 'news'



class Permission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    permission_student = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    createtime = models.DateTimeField(blank=True, null=True)

    objects = AndroidDatabaseManager()

    class Meta:
        managed = False
        db_table = 'permission'


class PermissionMarker(models.Model):
    pm_permission = models.OneToOneField(Permission, models.DO_NOTHING, primary_key=True)
    pm_maker = models.ForeignKey(Marker, models.DO_NOTHING, blank=True, null=True)

    objects = AndroidDatabaseManager()

    class Meta:
        managed = False
        db_table = 'permission_marker'


class User(models.Model):
    student_id = models.IntegerField(primary_key=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=1280, blank=True, null=True)
    faculty = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    objects = AndroidDatabaseManager()

    class Meta:
        managed = False
        db_table = 'user'