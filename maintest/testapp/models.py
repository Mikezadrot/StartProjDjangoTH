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
        # managed = False
        db_table = 'contacts'
    def __str__(self):
        return str(self.name)


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


class TypeofPartner(models.Model):
    uuid = models.CharField(max_length=50, default=0)
    name = models.CharField(max_length=50, default=0)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'testapp_typeofpartner'


    @classmethod
    def transfer(cls):
        existing_uuid = cls.objects.values_list('uuid', flat=True)
        typ_par = Partnertype.objects.all()


        for type_par in typ_par:
            existing_type = cls.objects.filter(uuid=type_par.id).first()

            if existing_type:
                existing_type.uuid = type_par.id
                existing_type.name = type_par.name
                existing_type.save()
            else:
                new_type = cls(uuid=type_par.id, name=type_par.name)
                new_type.save()



class Profession(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profession'


class Tested(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
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

        existing_uuid_ids = cls.objects.values_list('uuid_id', flat=True)

        for contact in contacts:
            if contact.id not in existing_uuid_ids:
                new_tested = cls(uuid_id=contact.id, name_cont=contact.name, phone_cont=contact.mobilephone)

                new_obj.append(new_tested)

        cls.objects.bulk_create(new_obj)

class Worker(models.Model):

    # id = models.IntegerField(primary_key=True, unique=True)
    uuid_id = models.UUIDField(blank=True, null=True)
    name = models.CharField(max_length=40, default=0)
    mobilephone = models.CharField(max_length=20, default=0)
    uuid_employer = models.CharField(max_length=50, default=0)
    name_employer = models.CharField(max_length=50, default=0)
    uuid_agency = models.CharField(max_length=50, default=0)
    name_agency = models.CharField(max_length=50, default=0)
    uuid_UaManager = models.CharField(max_length=50, default=0)
    name_UaManager = models.CharField(max_length=50, default=0)
    uuid_EUManager = models.CharField(max_length=50, default=0)
    name_EUManager = models.CharField(max_length=50, default=0)

    def __str__(self):
        return str(self.name)
    class Meta:
        db_table = 'testapp_worker'

    @classmethod
    def transfer(cls):
        contacts = Contacts.objects.all()
        accounts = Account.objects.all()
        profession = Profession.objects.all()
        employee = Employee.objects.all()
        existing_uuid_ids = cls.objects.values_list('uuid_id', flat=True)
        new_obj = []
        par_cont = '00000000-0000-0000-0000-000000000000'

        for contact in contacts:
            if str(contact.usremployerlookupid) != par_cont:
                # Перевіряємо, чи існує запис з таким uuid_id
                existing_worker = cls.objects.filter(uuid_id=contact.id).first()

                if existing_worker:
                    # Якщо запис існує, оновлюємо його дані
                    existing_worker.name = contact.name
                    existing_worker.mobilephone = contact.mobilephone
                    existing_worker.uuid_employer = contact.usremployerlookupid
                    # existing_worker.uuid_agency = contact.usragencylookupid
                    if str(contact.usragencylookupid) != par_cont:
                        existing_worker.uuid_agency = contact.usragencylookupid

                    else:
                        existing_worker.uuid_agency = 0
                    existing_worker.save()
                else:
                    # Якщо запис не існує, створюємо новий
                    new_worker = cls(uuid_id=contact.id, name=contact.name, mobilephone=contact.mobilephone,
                                     uuid_employer=contact.usremployerlookupid, uuid_agency=contact.usragencylookupid)

                    if str(new_worker.uuid_agency) == par_cont:
                        new_worker.uuid_agency = 0
                    new_worker.save()



        # for contact in contacts:
        #     if contact.id not in existing_uuid_ids and str(contact.usremployerlookupid) != par_cont:
        #         new_tested = cls(uuid_id=contact.id, name=contact.name, mobilephone=contact.mobilephone, uuid_employer=contact.usremployerlookupid, uuid_agency=contact.usragencylookupid)
        #         new_obj.append(new_tested)
        #
        #
        #
        #
        # cls.objects.bulk_create(new_obj)



class Vacancy(models.Model):
    uuid_id = models.CharField(max_length=50, default=0)
    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'testapp_vacancy'

    @classmethod
    def transfer(cls):
        professions = Profession.objects.all()
        existing_uuid_ids = cls.objects.values_list('uuid_id', flat=True)

        for profession in professions:
            existing_profession = cls.objects.filter(uuid_id=profession.id).first()
            if existing_profession:
                existing_profession.uuid_id = profession.id
                existing_profession.name = profession.name
                existing_profession.save()
            else:

                new_profession = cls(uuid_id=profession.id, name=profession.name)
                new_profession.save()





class Manager(models.Model):
    uuid = models.CharField(max_length=50, default=0)
    name = models.CharField(max_length=50, default=0)
    job = models.CharField(max_length=50, default=0)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'testapp_manager'


    @classmethod

    def transfer(cls):
        managers = Employee.objects.all()
        existing_uuid_ids = cls.objects.values_list('uuid', flat=True)


        for manager in managers:

            existing_manager = cls.objects.filter(uuid=manager.id).first()

            if existing_manager:
                existing_manager.uuid = manager.id
                existing_manager.name = manager.name
                existing_manager.job = manager.fulljobtitle
                existing_manager.save()
            else:
                new_manager = cls(uuid=manager.id, name=manager.name, job=manager.fulljobtitle)
                new_manager.save()




class Agency(models.Model):
    # id = models.IntegerField(primary_key=True, unique=True)
    uuid = models.CharField(max_length=50, default=0)
    name = models.CharField(max_length=250, default='empty')


    agency_id = models.CharField(max_length=253, default=0)

    # agency_id = models.ForeignKey("Agency", on_delete=models.CASCADE, default=0)
    phone = models.CharField(max_length=254)
    # part_type = models.ForeignKey('TypeofPartner', on_delete=models.CASCADE, default=0)
    part_type = models.CharField(max_length=255, default=0)

    def __str__(self):
        return str(self.uuid)

    class Meta:
        db_table = 'testapp_agency'


    @classmethod
    def transfer(cls):

        accounts = Account.objects.all()
        partner_type = TypeofPartner.objects.all()
        existed_agency_uuid = cls.objects.values_list('uuid', flat=True)
        for agency in accounts:
            existed_agency = cls.objects.filter(uuid=agency.id).first()

            if existed_agency:
                existed_agency.uuid = agency.id
                existed_agency.name = agency.name
                existed_agency.phone = agency.phone

                if str(agency.usragencythatgiveusemployerid) != '00000000-0000-0000-0000-000000000000':
                    existed_agency.agency_id = agency.usragencythatgiveusemployerid
                else:
                    existed_agency.agency_id = 0

                existed_agency.part_type = agency.usrpartnertypeid

                existed_agency.save()

            else:
                if str(agency.usrpartnertypeid) == 'ad63bf94-f0d1-4a63-9b24-87a6e0f990de':
                    new_agency = cls(uuid=agency.id, name=agency.name, phone=agency.phone, agency_id=agency.usragencythatgiveusemployerid, part_type=agency.usrpartnertypeid)
                    if new_agency.agency_id != '00000000-0000-0000-0000-000000000000':
                        new_agency.save()
                    else:
                        new_agency.agency_id = 0

                        new_agency.save()









class Employer(models.Model):
    uuid = models.CharField(max_length=50, default=0)
    name = models.CharField(max_length=50, default='empty')
    agency_id = models.CharField(max_length=255, default=0)
    # agency_id = models.ForeignKey("Agency", on_delete=models.CASCADE, default=0)
    # agency_id = Agency.uuid
    phone = models.CharField(max_length=50)
    part_type = models.CharField(max_length=255, default=0)
    # part_type = models.ForeignKey('TypeofPartner', on_delete=models.CASCADE, default=0)


    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'testapp_employer'

    @classmethod
    def transfer(cls):
        accounts = Account.objects.all()
        partner_type = TypeofPartner.objects.all()
        existed_employer_uuid = cls.objects.values_list('uuid', flat=True)
        for employer in accounts:
            existed_employer = cls.objects.filter(uuid=employer.id)
            if str(employer.usrpartnertypeid) != 'ad63bf94-f0d1-4a63-9b24-87a6e0f990de':
                if existed_employer:
                    existed_employer.uuid = employer.id
                    existed_employer.name = employer.name
                    existed_employer.phone = employer.phone
                    existed_employer.agency_id = employer.usragencythatgiveusemployerid
                    existed_employer.part_type = employer.usrpartnertypeid
                    existed_employer.save()
                else:
                    new_employer = cls(uuid=employer.id, name=employer.name, phone=employer.phone,agency_id=employer.usragencythatgiveusemployerid, part_type=employer.usrpartnertypeid)
                    new_employer.save()



class Boss(models.Model):
    id = models.IntegerField(primary_key= True, unique=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self)