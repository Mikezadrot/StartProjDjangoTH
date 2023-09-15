from django.shortcuts import render
from django.db import connection
from django.db import connections
from django.conf import settings
from .models import Account

from .models import Contacts

# def contacts_list(request):
#     table_name = "Contacts"  # Замініть це на вашу реальну назву таблиці
#     context = {'table_name': table_name}
#     return render(request, 'crm_app/contacts/contacts_list.html', context)

# print(connection.settings_dict['NAME'])

# Вивести список таблиць
# with connections['db_from_crm'].cursor() as cursor:
#     cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
#     table_names = [row[0] for row in cursor.fetchall()]
#
# # Отримуємо вміст кожної таблиці
# table_data = {}
# for table in table_names:
#     with connections['db_from_crm'].cursor() as cursor:
#         cursor.execute(f"SELECT * FROM {table} LIMIT 10")  # Отримати перші 10 рядків для прикладу
#         rows = cursor.fetchall()
#         table_data[table] = rows
# print(table_data)
def contacts_list(request):
    # # Отримуємо назву бази даних з налаштувань
    # db_name = settings.DATABASES['db_from_crm']['NAME']
    #
    # # Отримуємо список таблиць з бази даних
    # with connections['db_from_crm'].cursor() as cursor:
    #     cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    #     table_names = [row[0] for row in cursor.fetchall()]
    #
    # # Отримуємо вміст кожної таблиці
    # table_data = {}
    # for table in table_names:
    #     with connections['db_from_crm'].cursor() as cursor:
    #         cursor.execute(f"SELECT * FROM {table} LIMIT 10")  # Отримати перші 10 рядків для прикладу
    #         rows = cursor.fetchall()
    #         table_data[table] = rows
    #
    # context = {'db_name': db_name, 'table_names': table_names, 'table_data': table_data}
    # return render(request, 'crm_app/contacts/contacts_list.html', context)
    contex = {'acc': Account.objects.all()}
    return render(request,'crm_app/contacts/contacts_list.html', contex )





def table_list(request):
    db_name = settings.DATABASES['default']['NAME']
    with connection.cursor() as cursor:
        # Отримати список всіх таблиць
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        table_names = [row[0] for row in cursor.fetchall()]

    table_data = {}
    for table in table_names:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table} LIMIT 10")  # Отримати перші 10 рядків для прикладу
            rows = cursor.fetchall()
            table_data[table] = rows

    context = {'table_names': table_names, 'db_name': db_name, 'table_data': table_data}
    return render(request, 'crm_app/contacts/table_list.html', context)
