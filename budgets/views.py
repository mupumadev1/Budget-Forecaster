import csv
import json
from collections import defaultdict
from datetime import datetime
from decimal import Decimal

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, Sum, F
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from openpyxl.styles import colors
from openpyxl.workbook import Workbook
from rest_framework_simplejwt.tokens import RefreshToken

from budgets.forms import BudgetEditForm, UserCreate
from budgets.models import BudgetLines, Users, Glafs, BudgetComments, BudgetStatus, BudgetAssumptions, BudgetTotals, \
    Currency, BudgetLinesLog


# Create your views here.
def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request, exception):
    return render(request, '500.html', status=500)


def index(request, budget_set):
    if request.user.is_authenticated:
        account_details = BudgetTotals.objects.filter(budget_set=budget_set, posted=False).order_by(
            '-last_updated').annotate(
            count=Count('department__id'))

        # CEO department
        ceo = BudgetTotals.objects.filter(budget_set=budget_set, department_id=1, posted=False).order_by(
            '-last_updated')

        # Internal Audit department
        internal_audit = BudgetTotals.objects.filter(budget_set=budget_set, department_id=2, posted=False).order_by(
            '-last_updated')

        # Supply Chain department
        supply_chain = BudgetTotals.objects.filter(budget_set=budget_set, department_id=3, posted=False).order_by(
            '-last_updated')

        # BDS department
        bds = BudgetTotals.objects.filter(budget_set=budget_set, department_id=4, posted=False).order_by(
            '-last_updated')

        # Public Relations department
        public_relations = BudgetTotals.objects.filter(budget_set=budget_set, department_id=5, posted=False).order_by(
            '-last_updated')

        # Technical department
        technical = BudgetTotals.objects.filter(budget_set=budget_set, department_id=6, posted=False).order_by(
            '-last_updated')
        technical_total = technical.aggregate(total_technical=Sum('total'))['total_technical']

        # Information System department
        information_system = BudgetTotals.objects.filter(budget_set=budget_set, department_id=7, posted=False).order_by(
            '-last_updated')

        # Legal Risk department
        legal_risk = BudgetTotals.objects.filter(budget_set=budget_set, department_id=8, posted=False).order_by(
            '-last_updated')

        # Human Capital department
        human_capital = BudgetTotals.objects.filter(budget_set=budget_set, department_id=9, posted=False).order_by(
            '-last_updated')

        # Sales & Marketing department
        sales_marketing = BudgetTotals.objects.filter(budget_set=budget_set, department_id=10, posted=False).order_by(
            '-last_updated')

        # Admin department
        admin = BudgetTotals.objects.filter(budget_set=budget_set, department_id=11, posted=False).order_by(
            '-last_updated')

        # Finance department
        finance = BudgetTotals.objects.filter(budget_set=budget_set, department_id=12, posted=False).order_by(
            '-last_updated')

        # Income accounts
        income = BudgetTotals.objects.filter(budget_set=budget_set, department_id=17, posted=False).order_by(
            '-last_updated')


        # Asset accounts
        asset = BudgetTotals.objects.filter(budget_set=budget_set, department_id=13, posted=False).order_by(
            '-last_updated')

        # Liability accounts
        liability = BudgetTotals.objects.filter(budget_set=budget_set, department_id=14, posted=False).order_by(
            '-last_updated')

        # Equity accounts
        equity = BudgetTotals.objects.filter(budget_set=budget_set, department_id=15, posted=False).order_by(
            '-last_updated')

        # Clearing accounts
        clearing = BudgetTotals.objects.filter(budget_set=budget_set, department_id=16, posted=False).order_by(
            '-last_updated')
        if request.user.role == '002':
            total_sum = account_details.aggregate(total_sum=Sum('total'))['total_sum']
        elif not request.user.role == '002':
            total_sum = account_details.filter(department=request.user.department).aggregate(total_sum=Sum('total'))['total_sum']


        context = {
            'income': income,
            'asset': asset,
            'liability': liability,
            'equity': equity,
            'clearing': clearing,
            'ceo': ceo,
            'internal_audit': internal_audit,
            'supply_chain': supply_chain,
            'bds': bds,
            'public_relations': public_relations,
            'technical': technical,
            'information_systems': information_system,
            'legal_risk': legal_risk,
            'human_capital': human_capital,
            'sales_marketing': sales_marketing,
            'admin': admin,
            'finance': finance,
            'budget_set': budget_set,
            'total': total_sum
        }
        return render(request, 'index.html', context)
    else:
        return redirect('budgets:login')



def generate_excel(request):
    # Define the header row for the Excel file
    excel_header = ['BUDGET SUMMARY', 'Q1', 'Q2', 'H1', 'Q3', 'Q4', 'H2','TOTAL']

    # Define quarter and half period ranges
    quarter_periods = [1, 2, 3, 4]
    half1_periods = [1, 2, 3, 4, 5, 6]
    half2_periods = [7, 8, 9, 10, 11, 12]

    # Grouping the values according to quarters and halves
    budget_totals = defaultdict(lambda: defaultdict(Decimal))

    for budget_total in BudgetTotals.objects.exclude(total=0).all():
        for period in range(1, 13):
            value = getattr(budget_total, f'period{period}', Decimal('0'))
            if period in quarter_periods:
                budget_totals[budget_total.account][f'Q{period}'] += value
            if period in half1_periods:
                budget_totals[budget_total.account]['H1'] += value
            if period in half2_periods:
                budget_totals[budget_total.account]['H2'] += value
        budget_totals[budget_total.account]['TOTAL'] = getattr(budget_total,'total',Decimal('0'))

    # Create a new Excel workbook
    workbook = Workbook()
    sheet = workbook.active

    # Writing the header row with bold and blue background color
    for col, header in enumerate(excel_header, start=1):
        cell = sheet.cell(row=1, column=col)
        cell.value = header
        cell.font = cell.font.copy(bold=True,color=colors.WHITE)
        cell.fill = cell.fill.copy(fill_type='solid', start_color='00008B')

    # Writing the data rows

    for row, (account, totals) in enumerate(budget_totals.items(), start=2):
        sheet.cell(row=row, column=1, value=account.pk)
        for col, period in enumerate(excel_header[1:], start=2):
            sheet.cell(row=row, column=col, value=Decimal(totals[period]))

    # Create a HttpResponse with an Excel file attachment
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="budget_totals.xlsx"'

    # Save the workbook to the HttpResponse
    workbook.save(response)

    return response

def department_budget_settings(request,dept_id):
    if request.user.is_authenticated:
        obj = BudgetStatus.objects.filter(department_id=dept_id).all()
        if request.GET.get('complete') == '1':
            if request.user.role != '002':
                message = f"{request.GET.get('budget_id')} from {request.user.department.name} department has been marked as complete"
                    # Send the notification message
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'public_room',
                    {
                        "type": "send_notification",
                        "message": message
                    }
                )
            BudgetStatus.objects.filter(department=request.user.department,budget_set=request.GET.get('budget_id')).update(is_complete=True,is_active=False,comment=request.GET.get('comment'))
            return JsonResponse({'result':'success'})
        elif request.GET.get('incomplete') == '1':
            if request.user.role != '002' :

                message = f"Changes to be made to {request.GET.get('budget_id')} from {request.user.department.name} department require your approval"

                # Send the notification message
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'public_room',
                    {
                        "type": "send_notification",
                        "message": message
                    }
                )
            budget = request.GET.get('budget_id')
            BudgetStatus.objects.filter(department=request.user.department, budget_set=budget).update(is_complete=False,comment=request.GET.get('comment'))
            return JsonResponse({'result': 'success'})
        return render(request, 'budget-settings.html', {'budgetStatus': obj})
    else:
        return redirect('budgets:login')


def budget_settings(request):
    if request.user.is_authenticated:
        obj = BudgetStatus.objects.all()
        if request.GET.get('complete') == '1':
            if request.user.role != '002':
                message = f"{request.GET.get('budget_id')} from {request.user.department.name} department has been marked as complete"
                    # Send the notification message
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'public_room',
                    {
                        "type": "send_notification",
                        "message": message
                    }
                )
            BudgetStatus.objects.filter(department=request.user.department,budget_set=request.GET.get('budget_id')).update(is_complete=True,is_active=False, comment=request.GET.get('comment'))
            return JsonResponse({'result':'success'})
        elif request.GET.get('incomplete') == '1':
            if request.user.role != '002' :
                message = f"Changes to be made to {request.GET.get('budget_id')} from {request.user.department.name} department require your approval"

                # Send the notification message
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'public_room',
                    {
                        "type": "send_notification",
                        "message": message
                    }
                )
            budget = request.GET.get('budget_id')
            BudgetStatus.objects.filter(department=request.user.department, budget_set=budget).update(is_complete=False,comment=request.GET.get('comment'))
            return JsonResponse({'result': 'success'})
        return render(request, 'budget-settings.html', {'budgetStatus': obj})
    else:
        return redirect('budgets:login')




def budget_assumptions(request):
    if request.user.is_authenticated:
        obj = BudgetAssumptions.objects.filter(department_id=request.user.department.id)
        currency_obj = Currency.objects.all()
        if request.method == 'POST':
            data = json.loads(request.body)

            if data['target'] == "assumptions":

                assumption_obj = BudgetAssumptions.objects.filter(factor=data['factor'],
                                                                  department=request.user.department).first()

                if not assumption_obj:
                    BudgetAssumptions.objects.create(rate=data['rate'], factor=data['factor'],
                                                     department=request.user.department, updated_by=request.user)
                else:

                    assumption_obj.rate = data['rate']
                    assumption_obj.save()

                obj = BudgetAssumptions.objects.filter(department_id=request.user.department.id)  # Refresh assumptions
            elif data['target'] == 'currency':
                currency = Currency.objects.filter(currency=data['currency']).first()
                if not currency:
                    Currency.objects.create(currency=data['currency'], rate=data['rate'], updated_by=request.user)
                else:
                    currency.rate = data['rate']
                    currency.save()
                currency_obj = Currency.objects.all()
        paginator = Paginator(obj, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context =  {'assumptions': page_obj, 'currency': currency_obj, 'department': request.user.department.name}
        return render(request, 'assumptions.html',context)
    else:
        return redirect('budgets:login')


def accounts_search(request):
    field_mapping = {
        'account_id': 'account_id',
        'account_name': 'account__acctdesc__icontains',
    }

    filter = request.GET.get('filter')
    value = request.GET.get('value')

    if filter in field_mapping and value:
        if request.user.role != '002':
            account_info = BudgetTotals.objects.filter(**{field_mapping[filter]: value},
                                                       department=request.user.department).values(
                'account_id', 'account__acctdesc', 'id').all()
            return JsonResponse({'data': list(account_info)}, status=200)
        else:
            account_info = BudgetTotals.objects.filter(**{field_mapping[filter]: value}).values(
                'account_id', 'account__acctdesc', 'id').all()
            return JsonResponse({'data': list(account_info)}, status=200)



def get_budget_set(request, object_id, budget_set):
    single_object = BudgetTotals.objects.all()
    obj = get_object_or_404(BudgetTotals, id=object_id, budget_set=budget_set)

    next_obj = BudgetTotals.objects.filter(id__gt=obj.id).order_by('id').first()
    prev_obj = BudgetTotals.objects.filter(id__lt=obj.id).order_by('-id').first()

    first_obj = BudgetTotals.objects.first()
    last_obj = BudgetTotals.objects.last()
    form = BudgetEditForm(instance=obj)
    context = {
        'form': form,
        'obj': single_object,
        'object': obj,
        'next_obj': next_obj,
        'prev_obj': prev_obj,
        'first_obj': first_obj,
        'last_obj': last_obj
    }

    return render(request, 'forms.html', context)


def user_logout(request):
    logout(request)
    return redirect('budgets:login')


def check_otp(entered_otp, saved_otp):
    if entered_otp == saved_otp:
        return True
    else:
        return False


def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user_id = request.user.id

        user = get_object_or_404(Users, id=user_id)

        if check_password(otp, user.login_otp) or user.is_valid_otp():
            RefreshToken.for_user(user)
            user.login_otp_used = True
            user.save(update_fields=["login_otp_used"])
            return redirect('budgets:home', budget_set=1)
        else:
            messages.error(request, message="Authentication Failed Try Again")
            return redirect("budgets:login")
    return render(request, 'enter-otp.html')


def create_user(request):
    form = UserCreate(request.POST)

    if form.is_valid():
        form.save()
        return redirect('budgets:login')
    return render(request, 'user-create.html', {'form': UserCreate(request.GET)})


def toggle_status_incomplete(request,id):
    budget_obj = BudgetStatus.objects.get(id=id)
    budget_obj.is_complete = False
    budget_obj.save()
    return redirect('budgets:settings')

def toggle_status_complete(request,id):
    budget_obj = BudgetStatus.objects.get(id=id)
    budget_obj.is_complete = True
    budget_obj.save()
    return redirect('budgets:settings')

def toggle_status_false(request, id):
    budget_obj = BudgetStatus.objects.get(id=id)
    budget_obj.is_active = False
    budget_obj.save()
    return redirect('budgets:settings')


def toggle_status_true(request,id):
    try:
        budget_obj = BudgetStatus.objects.get(id=id)
        budget_obj.is_active = True
        budget_obj.save()
        return redirect('budgets:settings')
    except ValidationError as e:
        messages.error(request, e.message)
        return redirect('budgets:settings')


def clear_budget_line(request, object_id):
    line = get_object_or_404(BudgetLines, id=object_id)
    with transaction.atomic():
        BudgetTotals.objects.filter(account_id=line.account.acctid).update(
            total=F('total') - line.total,
            period1=F('period1') - line.period1,
            period2=F('period2') - line.period2,
            period3=F('period3') - line.period3,
            period4=F('period4') - line.period4,
            period5=F('period5') - line.period5,
            period6=F('period6') - line.period6,
            period7=F('period7') - line.period7,
            period8=F('period8') - line.period8,
            period9=F('period9') - line.period9,
            period10=F('period10') - line.period10,
            period11=F('period11') - line.period11,
            period12=F('period12') - line.period12,
            last_updated=datetime.now(),
            last_updated_by_id=request.user.id
        )
        line.delete()
    return redirect('budgets:home', 'Budget 1')

def changelog(request):
    if request.user.is_authenticated:
        obj = BudgetLinesLog.objects.all()
        paginator = Paginator(obj, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'changelog.html', {'changes':page_obj})
    else:
        return redirect('budgets:login')

def update(request, object_id):
    if request.user.is_authenticated:
        if request.user.role != '002':
            single_object = BudgetTotals.objects.filter(department=request.user.department)
        else:
            single_object = BudgetTotals.objects.all()

        obj_t = get_object_or_404(BudgetTotals, id=object_id)
        lines = BudgetLines.objects.filter(account__acctid=obj_t.account.acctid)

        active = get_object_or_404(BudgetStatus, department_id=obj_t.department.id, is_active=True)
        if active:

            first_dept_obj = BudgetTotals.objects.filter(budget_set=active.budget_set, department_id=obj_t.department.id,
                                                         id=object_id).first()
            user = get_object_or_404(Users, id=request.user.id)
            obj = get_object_or_404(BudgetTotals, id=first_dept_obj.id)
            if request.user.role != '002':
                assumptions = BudgetAssumptions.objects.filter(department=request.user.department)
            else:
                assumptions = BudgetAssumptions.objects.all()
            next_obj = BudgetTotals.objects.filter(id__gt=obj.id, department_id=obj_t.department.id,
                                                   budget_set=active.budget_set).order_by('id').first()
            prev_obj = BudgetTotals.objects.filter(id__lt=obj.id, department_id=obj_t.department.id,
                                                   budget_set=active.budget_set).order_by('-id').first()

            first_obj = BudgetTotals.objects.filter(department_id=obj_t.department.id, budget_set=active.budget_set).first()
            last_obj = BudgetTotals.objects.filter(department_id=obj_t.department.id, budget_set=active.budget_set).last()

            form = BudgetEditForm()

            if request.method == 'POST':

                data = json.loads(request.body)
                currency_obj = get_object_or_404(Currency, id=data['currency'])
                with transaction.atomic():
                    BudgetTotals.objects.filter(id=object_id).update(last_updated=datetime.now(),
                                                                     last_updated_by_id=request.user.id,

                                                                     total=F('total') + data['total'],
                                                                     period1=F('period1') + data['period1'],
                                                                     period2=F('period2') + data['period2'],
                                                                     period3=F('period3') + data['period3'],
                                                                     period4=F('period4') + data['period4'],
                                                                     period5=F('period5') + data['period5'],
                                                                     period6=F('period6') + data['period6'],
                                                                     period7=F('period7') + data['period7'],
                                                                     period8=F('period8') + data['period8'],
                                                                     period9=F('period9') + data['period9'],
                                                                     period10=F('period10') + data['period10'],
                                                                     period11=F('period11') + data['period11'],
                                                                     period12=F('period12') + data['period12']
                                                                     )
                if data['entryType'] == 'function':

                    BudgetLines.objects.create(
                        account=obj.account,
                        exchange_rate=data['exchange_rate'],
                        item_description=data['item_description'],
                        department=obj.department,
                        total=Decimal(data['total']),
                        rate=Decimal(data['rate']),
                        usage=Decimal(data['usage']),
                        factor=Decimal(data['factor']),
                        staff=Decimal(data['staff']),
                        period1=Decimal(data['period1']),
                        period2=Decimal(data['period2']),
                        period3=Decimal(data['period3']),
                        period4=Decimal(data['period4']),
                        period5=Decimal(data['period5']),
                        period6=Decimal(data['period6']),
                        period7=Decimal(data['period7']),
                        period8=Decimal(data['period8']),
                        period9=Decimal(data['period9']),
                        period10=Decimal(data['period10']),
                        period11=Decimal(data['period11']),
                        period12=Decimal(data['period12']),
                        currency=currency_obj,
                        budget_set=active.budget_set,
                        last_updated=datetime.now(),
                        last_updated_by_id=request.user.id)
                    return JsonResponse({'status': 'success'})
                elif data['entryType'] == 'manual':

                    BudgetLines.objects.create(
                        account=obj.account,
                        exchange_rate=data['exchange_rate'],
                        department=obj.department,
                        total=Decimal(data['total']),
                        item_description=data['item_description'],
                        rate=Decimal(0),
                        usage=Decimal(0),
                        factor=Decimal(0),
                        staff=Decimal(0),
                        period1=Decimal(data['period1']),
                        period2=Decimal(data['period2']),
                        period3=Decimal(data['period3']),
                        period4=Decimal(data['period4']),
                        period5=Decimal(data['period5']),
                        period6=Decimal(data['period6']),
                        period7=Decimal(data['period7']),
                        period8=Decimal(data['period8']),
                        period9=Decimal(data['period9']),
                        period10=Decimal(data['period10']),
                        period11=Decimal(data['period11']),
                        period12=Decimal(data['period12']),
                        currency=currency_obj,
                        budget_set=active.budget_set,
                        last_updated=datetime.now(),
                        last_updated_by_id=request.user.id)

                    return JsonResponse({'status': 'success'})
            context = {
                'currency': Currency.objects.all(),
                'name': obj.account.acctdesc,
                'form': form,
                'obj': single_object,
                'object': obj,
                'next_obj': next_obj,
                'prev_obj': prev_obj,
                'first_obj': first_obj,
                'last_obj': last_obj,
                'assumptions': assumptions,
                'activebs': active.budget_set,
                'department': obj_t.department.name,
                'lines': lines
            }

            return render(request, 'forms.html', context)
    else:
        return redirect('budgets:login')



def delete_assumption(request,id):
    BudgetAssumptions.objects.filter(id=id).delete()
    return redirect('budgets:assumptions')
def delete_currency(request,id):
    Currency.objects.filter(id=id).delete()
    return redirect('budgets:assumptions')

def update_expenses(request, department_id):
    if request.user.is_authenticated:
        if request.user.role != '002':
            single_object = BudgetTotals.objects.filter(department=request.user.department)
        else:
            single_object = BudgetTotals.objects.all()
        active = get_object_or_404(BudgetStatus, department_id=department_id, is_active=True)

        if active:
            first_dept_obj = BudgetTotals.objects.filter(budget_set=active.budget_set, department_id=department_id).first()
            user = get_object_or_404(Users, id=request.user.id)
            obj = get_object_or_404(BudgetTotals, id=first_dept_obj.id)
            if request.user.role != '002':
                assumptions = BudgetAssumptions.objects.filter(department=request.user.department)
            else:
                assumptions = BudgetAssumptions.objects.all()
            next_obj = BudgetTotals.objects.filter(id__gt=obj.id, department_id=department_id,
                                                   budget_set=active.budget_set).order_by('id').first()
            prev_obj = BudgetTotals.objects.filter(id__lt=obj.id, department_id=department_id,
                                                   budget_set=active.budget_set).order_by('-id').first()

            first_obj = BudgetTotals.objects.filter(department_id=department_id, budget_set=active.budget_set).first()
            last_obj = BudgetTotals.objects.filter(department_id=department_id, budget_set=active.budget_set).last()

            form = BudgetEditForm()
            if request.method == 'POST':

                data = json.loads(request.body)
                currency_obj = get_object_or_404(Currency, id=data['currency'])
                with transaction.atomic():
                    BudgetTotals.objects.filter(id=obj.id).update(last_updated=datetime.now(),
                                                                  last_updated_by_id=request.user.id,

                                                                  total=F('total') + data['total'],
                                                                  period1=F('period1') + data['period1'],
                                                                  period2=F('period2') + data['period2'],
                                                                  period3=F('period3') + data['period3'],
                                                                  period4=F('period4') + data['period4'],
                                                                  period5=F('period5') + data['period5'],
                                                                  period6=F('period6') + data['period6'],
                                                                  period7=F('period7') + data['period7'],
                                                                  period8=F('period8') + data['period8'],
                                                                  period9=F('period9') + data['period9'],
                                                                  period10=F('period10') + data['period10'],
                                                                  period11=F('period11') + data['period11'],
                                                                  period12=F('period12') + data['period12']
                                                                  )
                if data['entryType'] == 'function':

                    BudgetLines.objects.create(
                        account=obj.account,
                        exchange_rate=data['exchange_rate'],
                        item_description=data['item_description'],
                        department=obj.department,
                        total=Decimal(data['total']),
                        rate=Decimal(data['rate']),
                        usage=Decimal(data['usage']),
                        factor=Decimal(data['factor']),
                        staff=Decimal(data['staff']),
                        period1=Decimal(data['period1']),
                        period2=Decimal(data['period2']),
                        period3=Decimal(data['period3']),
                        period4=Decimal(data['period4']),
                        period5=Decimal(data['period5']),
                        period6=Decimal(data['period6']),
                        period7=Decimal(data['period7']),
                        period8=Decimal(data['period8']),
                        period9=Decimal(data['period9']),
                        period10=Decimal(data['period10']),
                        period11=Decimal(data['period11']),
                        period12=Decimal(data['period12']),
                        currency=currency_obj,
                        budget_set=active.budget_set,
                        last_updated=datetime.now(),
                        last_updated_by_id=request.user.id)
                    return JsonResponse({'status': 'success'})
                elif data['entryType'] == 'manual':

                    BudgetLines.objects.create(
                        account=obj.account,
                        exchange_rate=data['exchange_rate'],
                        department=obj.department,
                        total=Decimal(data['total']),
                        item_description=data['item_description'],
                        rate=Decimal(0),
                        usage=Decimal(0),
                        factor=Decimal(0),
                        staff=Decimal(0),
                        period1=Decimal(data['period1']),
                        period2=Decimal(data['period2']),
                        period3=Decimal(data['period3']),
                        period4=Decimal(data['period4']),
                        period5=Decimal(data['period5']),
                        period6=Decimal(data['period6']),
                        period7=Decimal(data['period7']),
                        period8=Decimal(data['period8']),
                        period9=Decimal(data['period9']),
                        period10=Decimal(data['period10']),
                        period11=Decimal(data['period11']),
                        period12=Decimal(data['period12']),
                        currency=currency_obj,
                        budget_set=active.budget_set,
                        last_updated=datetime.now(),
                        last_updated_by_id=request.user.id)

                    return JsonResponse({'status': 'success'})
            context = {
                'form': form,
                'obj': single_object,
                'name': obj.account.acctdesc,
                'object': obj,
                'next_obj': next_obj,
                'prev_obj': prev_obj,
                'first_obj': first_obj,
                'last_obj': last_obj,
                'lines': BudgetLines.objects.filter(account__acctid=obj.account.acctid),
                'currency': Currency.objects.all(),
                'assumptions': assumptions,
                'activebs': active.budget_set,
                'department': active.department.name

            }

            return render(request, 'forms.html', context)
        return render(request, 'forms.html')
    else:
        return redirect('budgets:login')

def saveComments(request):
    if request.method == 'GET':
        budget = request.POST.get('budget_id')
        field_name = request.POST.get('field_name')
        new_comment = request.POST.get('comment')
        obj = get_object_or_404(BudgetComments, budget=budget, field_name=field_name)
        obj.comment = new_comment
        obj.save()
        return JsonResponse({'status': 'success', 'data': new_comment})
    else:
        return JsonResponse({'error': 'Unsupported method'}, status=405)


def post_to_sage(request, budget_set):
    objects = BudgetTotals.objects.filter(budget_set=budget_set)
    income_objects = BudgetTotals.objects.filter(account__acctid__startswith=5)
    asset_objects = BudgetTotals.objects.filter(account__acctid__startswith=1)
    liability_objects = BudgetTotals.objects.filter(account__acctid__startswith=2)
    equity_objects = BudgetTotals.objects.filter(account__acctid__startswith=3)
    clearing_objects = BudgetTotals.objects.filter(account__acctid__startswith=4)
    for obj in objects:
        # Determine if the object should be saved as positive or negative
        if obj in income_objects or equity_objects or clearing_objects or liability_objects or asset_objects:
            # For income objects, save them as positive
            total = -obj.total
            net_periods = [-getattr(obj, f'period{i}') for i in range(1, 13)]
        else:
            # For other objects, save them as negative
            total = obj.total
            net_periods = [getattr(obj, f'period{i}') for i in range(1, 13)]

        sql_obj = Glafs.objects.filter(acctid=obj.account_id).update(
            fscsyr=datetime.now().year,
            fscsdsg=budget_set,
            fscscurn='ZMW',
            curntype='1',
            audtdate=datetime.now().date().strftime('%Y%m%d'),
            audttime=datetime.now().strftime('%H%M%S'),
            audtuser='ADMIN',
            audtorg='INFTST',
            swrvl=0,
            codervl='',
            scurndec='2',
            openbal=total,
            netperd1=net_periods[0],
            netperd2=net_periods[1],
            netperd3=net_periods[2],
            netperd4=net_periods[3],
            netperd5=net_periods[4],
            netperd6=net_periods[5],
            netperd7=net_periods[6],
            netperd8=net_periods[7],
            netperd9=net_periods[8],
            netperd10=net_periods[9],
            netperd11=net_periods[10],
            netperd12=net_periods[11],
            netperd13=0.00,
            netperd14=0.00,
            netperd15=0.00,
            activitysw=1
        )
        sql_obj.save(using='sql_server')
        obj.posted = True
        obj.save()
    return redirect('budgets:home', budget_set=budget_set + 1)


def user_login(request):
    if request.method == 'POST':
        try:
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role != '002':
                    active = BudgetStatus.objects.get(department=request.user.department, is_active=True)

                    return redirect('budgets:home', f'{active.budget_set}')
                """user_obj = get_object_or_404(Users, username=username)
                totp = pyotp.TOTP(user.otp_base32).now()
                user_obj.login_otp = totp
                user_obj.otp_created_at = datetime.now(timezone.utc)
                user_obj.login_otp_used = False
                user_obj.save(update_fields=["login_otp", "otp_created_at", "login_otp_used"])
                #return redirect('budgets:enter-otp')"""
                return redirect('budgets:home', 'Budget 1')
            else:
                messages.error(request, message="Username/Password not registered")
                return redirect("budgets:login")

        except Exception as e:
            messages.error(request, message="An error occurred. Please try again.")

            return redirect("budgets:login")

    else:

        return render(request, 'login.html')
