from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Entry, Account, Category
from .serializer import EntrySerializer, IDParamSerializer


class Expense(APIView):
    @swagger_auto_schema(method='get')
    def get(self, request):
        expense = Entry.objects.all()
        serializer = EntrySerializer(expense, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=EntrySerializer)
    def post(self, request):
        form_data = request.data
        try:
            account = Account.objects.get(id=form_data['account'])
            category = Category.objects.get(id=form_data['category'])

            form_data['category'] = category
            form_data['account'] = account

            Entry.objects.create(**form_data)
            return Response()
        except:
            # TODO: return error response
            return Response()

    @swagger_auto_schema(query_serializer=IDParamSerializer)
    def delete(self, request):
        id = request.GET['id']
        try:
            entry = Entry.objects.get(id=id)
            entry.delete()
            return Response()
        except:
            # TODO: return error response
            return Response()
