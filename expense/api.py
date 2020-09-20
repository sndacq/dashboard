from django.shortcuts import HttpResponse
from django.http import Http404, JsonResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django import forms
from rest_framework.decorators import api_view

from scripts import parse
from .models import Expense, Account, Category

import json


class ExpenseValidationForm(forms.Form):
    date = forms.DateTimeField()
    amount = forms.DecimalField()
    account = forms.IntegerField()
    category = forms.IntegerField()
    expense_type = forms.IntegerField()


def index(request):
    clean_data = parse.get_clean_data()
    return HttpResponse(clean_data)

@csrf_exempt
def expense(request, expense_id=None):
    if request.method == 'GET':
        return get_expense(request, expense_id)

    elif request.method == 'POST':
        return create_expense(request)

    elif request.method == 'PUT':
        return update_expense(request)

    elif request.method == 'DELETE':
        return delete_expense(request, expense_id)

    else:
        raise Http404('Invalid Request Method')

def get_expense(request, expense_id):
    try:
        expense_list = []
        if expense_id:
            expense = Expense.objects.get(pk=expense_id)
            expense_list.append({
                'id': expense.pk,
                'date': expense.date,
                'amount': expense.amount,
                'expense_type': expense.expense_type,
                'account': expense.account.pk,
                'category': expense.category.pk,
            })  
        else:
            expense_objects = Expense.objects.all().order_by('-date')
            for entry in expense_objects:
                expense_list.append({
                    'id': entry.pk,
                    'date': entry.date,
                    'amount': entry.amount,
                    'expense_type': entry.expense_type,
                    'account': entry.account.pk,
                    'category': entry.category.pk,
                })
        return JsonResponse(expense_list, safe=False)
    except Exception as error:
        print(error)
        raise Http404('Entry not found')

# TODO: figure out csrf on postman
def create_expense(request):
    form_data = json.loads(request.body)
    entry = ExpenseValidationForm(form_data or None)
 
    if entry.is_valid():
        try:
            entry_account = Account.objects.get(pk=form_data['account'])
            entry_category = Category.objects.get(pk=form_data['category'])

            e = Expense(
                date = form_data['date'],
                amount = form_data['amount'],
                account = entry_account,
                category = entry_category,
                expense_type = form_data['expense_type']
            )
            e.save()
            return JsonResponse({"id": e.pk})

        except Exception as error:
            print(error)
            return HttpResponseBadRequest('Unable to create entry')
    else:
        return HttpResponseBadRequest('Invalid form data')

#TODO: validate if data has id
def update_expense(request):
    form_data = json.loads(request.body)
    entry = ExpenseValidationForm(form_data or None)

    if entry.is_valid():
        try:
            entry_account = Account.objects.get(pk=form_data['account'])
            entry_category = Category.objects.get(pk=form_data['category'])

            expense = Expense.objects.get(pk=form_data['id'])

            expense.date = form_data['date']
            expense.amount = form_data['amount']
            expense.account = entry_account
            expense.category = entry_category
            expense.expense_type = form_data['expense_type']
            expense.save()

            return JsonResponse({
                'id': expense.pk,
                'date': expense.date,
                'amount': expense.amount,
                'expense_type': expense.expense_type,
                'account': expense.account.pk,
                'category': expense.category.pk,
            })

        except Exception as error:
            print(error)
            raise Http404('Unable to update entry')

    else:
        return HttpResponseBadRequest('Invalid form data')

def delete_expense(request, expense_id):
    if expense_id:
        try:
            expense = Expense.objects.get(pk=expense_id)
            expense.delete()
            return HttpResponse('Succesfully deleted entry')

        except Exception as error:
            print(error)
            raise Http404('Entry not found')

    else:
        raise Http404('Entry not found')

def category(request):
    if request.method == 'GET':
        try:
            category_list = []
            category_objects = Category.objects.all()
            for category in category_objects:
                category_list.append({
                    'id': category.pk,
                    'name': category.category_name,
                })
            return JsonResponse(category_list, safe=False)

        except Exception as error:
            print(error)
            raise Http404('No categories found')
    else:
        raise Http404('Invalid Request Method')

def account(request):
    if request.method == 'GET':
        try:
            account_list = []
            account_objects = Account.objects.all()
            for account in account_objects:
                account_list.append({
                    'id': account.pk,
                    'name': account.account_name,
                })
            return JsonResponse(account_list, safe=False)
        except Exception as error:
            print(error)
            raise Http404('No accounts found')
    else:
        raise Http404('Invalid Request Method')
