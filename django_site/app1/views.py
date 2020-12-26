from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
def home(request):
    return HttpResponse(content=b'This is a Django website.\n', status=200)
