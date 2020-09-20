from django.urls import path
from . import api

urlpatterns = [
	path('', api.index, name='index'),
	path('expense/', api.expense, name='expense'),
    path('expense/<int:expense_id>/', api.expense, name='expense id'),
    path('expense/category/', api.category, name='category'),
    path('expense/account/', api.account, name='account'),
]