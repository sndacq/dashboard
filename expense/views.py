from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .models import Entry
from .serializer import EntrySerializer


class Expense(APIView):
    @swagger_auto_schema(method='get')
    def get(request, pk):
        expense = Entry.objects.all()
        serializer = EntrySerializer(expense, many=True)
        return Response(serializer.data)

    @swagger_auto_schema
    def post(request):
        expense = Entry.objects.all()
        serializer = EntrySerializer(expense, many=True)
        return Response(serializer.data)
