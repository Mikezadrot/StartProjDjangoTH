from django.db import models


# Create your models here.


# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


#
# class Test_table(models.Model):
#     id = models.IntegerField(primary_key=True, unique=True)
#     name = models.CharField(max_length=20)
#     name_c = models.ForeignKey("Contacts", on_delete=models.DO_NOTHING)
# #
#
#
# class Manager(models.Model):
#     id = models.IntegerField(primary_key=True, unique=True)
#     # is_employer = models.ForeignKey('Employer', on_delete=models.CASCADE)
#     name = models.CharField(max_length=20)
#
#
# class Leads(models.Model):
#     id = models.IntegerField(primary_key=True, unique=True)
#     # name_lead = models.ForeignKey('Contacts', on_delete=models.DO_NOTHING)
#     name = models.CharField(max_length=20)
#
#     def __str__(self):
#         return str(self.name)
#
#
# class Account(models.Model):
#     id = models.UUIDField(primary_key=True)
#     name = models.CharField(max_length=255, blank=True, null=True)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     usrpartnertypeid = models.ForeignKey('Partnertype', models.DO_NOTHING, db_column='usrpartnertypeid', blank=True,
#                                          null=True)
#     usragencythatgiveusemployerid = models.UUIDField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'account'


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
        # managed = False
        db_table = 'contacts'
    def __str__(self):
        return str(self.name)




# class Employee(models.Model):
#     id = models.UUIDField(primary_key=True)
#     name = models.CharField(max_length=255, blank=True, null=True)
#     fulljobtitle = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'employee'


# class Partnertype(models.Model):
#     id = models.UUIDField(primary_key=True)
#     name = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'partnertype'


# class Profession(models.Model):
#     id = models.UUIDField(primary_key=True)
#     name = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'profession'


class Tested(models.Model):
    # id = models.IntegerField(primary_key=True, unique=True)
    uuid_id = models.UUIDField(blank=True, null=True)
    name_cont = models.CharField(max_length=255)
    phone_cont = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name_cont)

    class Meta:
        db_table = 'testapp_tested'

    @classmethod
    def transfer(cls):
        contacts = Contacts.objects.all()
        new_obj = []
        for contact in contacts:
            new_tested = cls(uuid_id=contact.id, name_cont=contact.name, phone_cont=contact.mobilephone)

            new_obj.append(new_tested)

        cls.objects.bulk_create(new_obj)

class Worker(models.Model):

    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=20)
    name_manager = models.ForeignKey("Manager", on_delete=models.DO_NOTHING)


    def __str__(self):
        return str(self.name)

class Manager(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)


class Boss(models.Model):
    id = models.IntegerField(primary_key= True, unique=True)
    name = models.CharField(max_length=20)
