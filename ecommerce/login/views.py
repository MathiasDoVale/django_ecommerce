from django.http import HttpResponse
from django.shortcuts import render


def accounts(request, year):
    context = {"year": year, "article_list": year}
    return render(request, "registration/login.html", context)
