from django.urls import path
from . import api

urlpatterns = [
	path('', api.index, name='index'),
	path('expense/', api.expense, name='get all expense'),
    path('expense/<int:expense_id>/', api.expense, name='get expense id'),
]