from django.shortcuts import HttpResponse
from scripts import parse

def index(request):
    clean_data = parse.get_clean_data()
    return HttpResponse(clean_data)