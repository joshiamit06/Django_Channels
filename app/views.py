from django.shortcuts import render


def index(request, group_name):
    return render(request, 'app/index.html', {'groupname':group_name})