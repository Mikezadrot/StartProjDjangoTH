from django.contrib import admin
# from .models import Test_table, Manager, Leads
from .models import  Worker, Manager, Boss, Tested, Vacancy, TypeofPartner, Agency, Employer

# Register your models here.
admin.site.register(Worker)
admin.site.register(Manager)
admin.site.register(Boss)
admin.site.register(Tested)
admin.site.register(Vacancy)
admin.site.register(TypeofPartner)
admin.site.register(Agency)
admin.site.register(Employer)