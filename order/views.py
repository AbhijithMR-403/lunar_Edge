from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.


def add_address(request):
    print('This reach here atleast once')
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
