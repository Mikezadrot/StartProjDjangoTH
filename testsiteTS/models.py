# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Account(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    usrpartnertypeid = models.UUIDField(blank=True, null=True)
    usragencythatgiveusemployerid = models.UUIDField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account'


class Contacts(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    mobilephone = models.CharField(max_length=20, blank=True, null=True)
    usremployerlookupid = models.UUIDField(blank=True, null=True)
    usragencylookupid = models.UUIDField(blank=True, null=True)
    usremployeemanagerukraineid = models.UUIDField(blank=True, null=True)
    usremployeemanagereuropeid = models.UUIDField(blank=True, null=True)
    usrscrolllookupid = models.UUIDField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contacts'


class Employee(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    fulljobtitle = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee'


class Partnertype(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partnertype'


class Profession(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profession'
