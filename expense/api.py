from django.shortcuts import HttpResponse
from django.http import Http404, JsonResponse,HttpResponseBadRequest
from django.http.multipartparser import MultiPartParser
from django.views.decorators.csrf import csrf_exempt
from django import forms
from rest_framework.decorators import api_view

from scripts import parse
from .models import Expense, Account, Category


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
        return update_expense(request, expense_id)

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
            expense_objects = Expense.objects.all()
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


    class ExpenseValidationForm(forms.Form):
        date = forms.DateTimeField()
        amount = forms.DecimalField()
        account = forms.IntegerField()
        category = forms.IntegerField()
        expense_type = forms.IntegerField()


    entry = ExpenseValidationForm(request.POST or None)
    if entry.is_valid():
        try:
            request_body = request.POST

            entry_account = Account.objects.get(pk=request_body['account'])
            entry_category = Category.objects.get(pk=request_body['category'])

            e = Expense(
                date = request_body['date'],
                amount = request_body['amount'],
                account = entry_account,
                category = entry_category,
                expense_type = request_body['expense_type']
            )
            e.save()
            return JsonResponse({"id": e.pk})

        except Exception as error:
            print(error)
            return HttpResponseBadRequest('Unable to create entry')
    else:
        return HttpResponseBadRequest('Invalid form data')

def update_expense(request, expense_id):
    if expense_id:
        try:
            request_body = MultiPartParser(request.META, request, request.upload_handlers).parse()
            request_body = request_body[0]

            entry_account = Account.objects.get(pk=request_body['account'])
            entry_category = Category.objects.get(pk=request_body['category'])
            expense = Expense.objects.get(pk=expense_id)
            expense.date = request_body['date']
            expense.amount = request_body['amount']
            expense.account = entry_account
            expense.category = entry_category
            expense.expense_type = request_body['expense_type']
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
        raise Http404('Entry not found')

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
