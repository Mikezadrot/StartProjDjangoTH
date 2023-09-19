from django.shortcuts import render

from .models import Contacts, Tested, Worker


def worker_view(request):
    # Отримати дані з моделі
    cont = Worker.objects.all()
    context = {'contact': cont}
    # print(context)
    # Передати дані в шаблон та відобразити їх
    return render(request, 'testapp/leads/leads.html', context)


def tested_view(request):
    data = Tested.objects.all()
    context = {'data': data}
    return render(request, 'testapp/test_dir/test.html', context)


def contats_view(request):
    data = Contacts.objects.all()
    context = {'data': data}
    return render(request, 'testapp/test_dir/cont_test.html',context)