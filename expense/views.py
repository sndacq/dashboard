from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Entry
from .serializer import EntrySerializer

@api_view(['GET'])
def getEntries(request):
    expense = Entry.objects.all()
    serializer = EntrySerializer(expense, many=True)
    return Response(serializer.data)
