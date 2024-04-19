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
from django.db.models import Count, Sum, F, Q
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
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


def dashboard_index(request):
    if request.user.is_authenticated:
        department_conditions = Q()
        for department_id in range(1, 13):  # Assuming departments IDs range from 1 to 12
            department_conditions |= Q(department_id=department_id)

        budget_totals = BudgetTotals.objects.filter(
            Q(posted=False) & department_conditions
        ).order_by('-department_id', '-last_updated')

        ceo = budget_totals.filter(department_id=1)

        internal_audit = budget_totals.filter(department_id=2)

        supply_chain = budget_totals.filter(department_id=3)

        bds = budget_totals.filter(department_id=4)

        public_relations = budget_totals.filter(department_id=10)

        technical = budget_totals.filter(department_id=6)

        information_systems = budget_totals.filter(department_id=7)

        legal_risk = budget_totals.filter(department_id=8)

        human_capital = budget_totals.filter(department_id=9)

        sales_marketing = budget_totals.filter(department_id=10)

        admin = budget_totals.filter(department_id=11)

        finance = budget_totals.filter(department_id=12)

        data = {
            'dept_totals': [
                {
                    'acctdesc': 'CEO',
                    'Q1': ceo.Q1,
                    'Q2': ceo.Q2,
                    'Q3': ceo.Q3,
                    'Q4': ceo.Q4,
                    'H1': ceo.H1,
                    'H2': ceo.H2,
                    'dept': ceo
                },
                {
                    'acctdesc': 'Internal Audit',
                    'Q1': internal_audit.Q1,
                    'Q2': internal_audit.Q2,
                    'Q3': internal_audit.Q3,
                    'Q4': internal_audit.Q4,
                    'H1': internal_audit.H1,
                    'H2': internal_audit.H2,
                    'dept': internal_audit
                },
                {
                    'acctdesc': 'Supply Chain',
                    'Q1': supply_chain.Q1,
                    'Q2': supply_chain.Q2,
                    'Q3': supply_chain.Q3,
                    'Q4': supply_chain.Q4,
                    'H1': supply_chain.H1,
                    'H2': supply_chain.H2,
                    'dept': supply_chain
                },
                {
                    'acctdesc': 'BDS',
                    'Q1': bds.Q1,
                    'Q2': bds.Q2,
                    'Q3': bds.Q3,
                    'Q4': bds.Q4,
                    'H1': bds.H1,
                    'H2': bds.H2,
                    'dept': bds
                },
                {
                    'acctdesc': 'Public Relations',
                    'Q1': public_relations.Q1,
                    'Q2': public_relations.Q2,
                    'Q3': public_relations.Q3,
                    'Q4': public_relations.Q4,
                    'H1': public_relations.H1,
                    'H2': public_relations.H2,
                    'dept': public_relations
                },
                {
                    'acctdesc': 'Technical',
                    'Q1': technical.Q1,
                    'Q2': technical.Q2,
                    'Q3': technical.Q3,
                    'Q4': technical.Q4,
                    'H1': technical.H1,
                    'H2': technical.H2,
                    'dept': technical
                },
                {
                    'acctdesc': 'Information Systems',
                    'Q1': information_systems.Q1,
                    'Q2': information_systems.Q2,
                    'Q3': information_systems.Q3,
                    'Q4': information_systems.Q4,
                    'H1': information_systems.H1,
                    'H2': information_systems.H2,
                    'dept': information_systems
                },
                {
                    'acctdesc': 'Legal & Risk',
                    'Q1': legal_risk.Q1,
                    'Q2': legal_risk.Q2,
                    'Q3': legal_risk.Q3,
                    'Q4':legal_risk.Q4,
                    'H1': legal_risk.H1,
                    'H2': legal_risk.H2,
                    'dept': legal_risk
                },
                {
                    'acctdesc': 'Human Capital',
                    'Q1': human_capital.Q1,
                    'Q2': human_capital.Q2,
                    'Q3': human_capital.Q3,
                    'Q4': human_capital.Q4,
                    'H1':human_capital.H1,
                    'H2': human_capital.H2,
                    'dept': human_capital
                },
                {
                    'acctdesc': 'Sales & Marketing',
                    'Q1': sales_marketing.Q1,
                    'Q2': sales_marketing.Q2,
                    'Q3': sales_marketing.Q3,
                    'Q4': sales_marketing.Q4,
                    'H1': sales_marketing.H1,
                    'H2': sales_marketing.H2,
                    'dept': sales_marketing
                },
                {
                    'acctdesc': 'Administration',
                    'Q1': admin.Q1,
                    'Q2': admin.Q2,
                    'Q3': admin.Q3,
                    'Q4': admin.Q4,
                    'H1': admin.H1,
                    'H2': admin.H2,
                    'dept': admin
                },
                {
                    'acctdesc': 'Finance',
                    'Q1': finance.Q1,
                    'Q2': finance.Q2,
                    'Q3': finance.Q3,
                    'Q4': finance.Q4,
                    'H1': finance.H1,
                    'H2': finance.H2,
                    'dept': finance
                },
            ]
        }
        return render(request, 'index.html', {'data':data})
    else:
        return redirect('budgets:login')

def index(request, budget_set):
            if request.user.is_authenticated:
                account_details = BudgetTotals.objects.filter(budget_set=budget_set, posted=False).order_by(
                    '-last_updated').annotate(
                    count=Count('department__id'))

                # Income accounts
                income = BudgetTotals.objects.filter(budget_set=budget_set, department_id=17, posted=False).order_by(
                    '-last_updated')
                paginator = Paginator(income, 10)
                page_number = request.GET.get('page')
                income_obj = paginator.get_page(page_number)

                # Asset accounts
                asset = BudgetTotals.objects.filter(budget_set=budget_set, department_id=13, posted=False).order_by(
                    '-last_updated')
                paginator = Paginator(asset, 10)
                page_number = request.GET.get('page')
                asset_obj = paginator.get_page(page_number)

                # Liability accounts
                liability = BudgetTotals.objects.filter(budget_set=budget_set, department_id=14, posted=False).order_by(
                    '-last_updated')
                paginator = Paginator(liability, 10)
                page_number = request.GET.get('page')
                liability_obj = paginator.get_page(page_number)

                # Equity accounts
                equity = BudgetTotals.objects.filter(budget_set=budget_set, department_id=11, posted=False).order_by(
                    '-last_updated')
                paginator = Paginator(equity, 10)
                page_number = request.GET.get('page')
                equity_obj = paginator.get_page(page_number)

                # Clearing accounts
                clearing = BudgetTotals.objects.filter(budget_set=budget_set, department_id=16, posted=False).order_by(
                    '-last_updated')
                paginator = Paginator(clearing, 10)
                page_number = request.GET.get('page')
                clearing_obj = paginator.get_page(page_number)

                total_sum = account_details.aggregate(total_sum=Sum('total'))['total_sum']

                context = {
                    'income': income_obj,
                    'asset': asset_obj,
                    'liability': liability_obj,
                    'equity': equity_obj,
                    'clearing': clearing_obj,
                    'budget_set': budget_set,
                    'total': total_sum
                }
                return render(request, 'capex-index.html', context)
            else:
                return redirect('budgets:login')

def dept_user_index(request, budget_set):
        if request.user.is_authenticated:
            department_conditions = Q()
            for department_id in range(1, 13):  # Assuming departments IDs range from 1 to 12
                department_conditions |= Q(department_id=department_id)

            # Fetch all relevant budget totals in a single query
            budget_totals = BudgetTotals.objects.filter(
                Q(budget_set=budget_set) & Q(posted=False) & department_conditions
            ).order_by('-department_id', '-last_updated')

            # Create separate variables for each department
            ceo = budget_totals.filter(department_id=1)
            paginator = Paginator(ceo, 10)
            page_number = request.GET.get('page')
            ceo_obj = paginator.get_page(page_number)
            internal_audit = budget_totals.filter(department_id=2)
            paginator = Paginator(internal_audit, 10)
            page_number = request.GET.get('page')
            internal_audit_obj = paginator.get_page(page_number)
            supply_chain = budget_totals.filter(department_id=3)
            paginator = Paginator(supply_chain, 10)
            page_number = request.GET.get('page')
            supply_chain_obj = paginator.get_page(page_number)
            bds = budget_totals.filter(department_id=4)
            paginator = Paginator(bds, 10)
            page_number = request.GET.get('page')
            bds_obj = paginator.get_page(page_number)
            public_relations = budget_totals.filter(department_id=10)
            paginator = Paginator(public_relations, 10)
            page_number = request.GET.get('page')
            public_relations_obj = paginator.get_page(page_number)
            technical = budget_totals.filter(department_id=6)
            paginator = Paginator(technical, 10)
            page_number = request.GET.get('page')
            technical_obj = paginator.get_page(page_number)
            information_systems = budget_totals.filter(department_id=7)
            paginator = Paginator(information_systems, 10)
            page_number = request.GET.get('page')
            information_systems_obj = paginator.get_page(page_number)
            legal_risk = budget_totals.filter(department_id=8)
            paginator = Paginator(legal_risk, 10)
            page_number = request.GET.get('page')
            legal_risk_obj = paginator.get_page(page_number)
            human_capital = budget_totals.filter(department_id=9)
            paginator = Paginator(human_capital, 10)
            page_number = request.GET.get('page')
            human_capital_obj = paginator.get_page(page_number)
            sales_marketing = budget_totals.filter(department_id=10)
            paginator = Paginator(sales_marketing, 10)
            page_number = request.GET.get('page')
            sales_marketing_obj = paginator.get_page(page_number)
            admin = budget_totals.filter(department_id=11)
            paginator = Paginator(admin, 10)
            page_number = request.GET.get('page')
            admin_page_obj = paginator.get_page(page_number)
            finance = budget_totals.filter(department_id=12)
            paginator = Paginator(finance, 10)
            page_number = request.GET.get('page')
            finance_page_obj = paginator.get_page(page_number)
            # Calculate total sum
            total_sum = budget_totals.filter(department=request.user.department).aggregate(total_sum=Sum('total'))[
                'total_sum']

            # Populate context variable
            context = {
                'ceo': ceo_obj,
                'internal_audit': internal_audit_obj,
                'supply_chain': supply_chain_obj,
                'bds': bds_obj,
                'public_relations': public_relations_obj,
                'technical': technical_obj,
                'information_systems': information_systems_obj,
                'legal_risk': legal_risk_obj,
                'human_capital': human_capital_obj,
                'sales_marketing': sales_marketing_obj,
                'admin': admin_page_obj,
                'finance': finance_page_obj,
                'budget_set': budget_set,
                'total': total_sum
            }
            return render(request, 'index-deptuser.html', context)
        else:
            return redirect('budgets:login')

def opex_index(request, budget_set):
        if request.user.is_authenticated:
            if not budget_set:
                return HttpResponseBadRequest("Invalid budget set")

            # Combine all department conditions using Q objects
            department_conditions = Q()
            for department_id in range(1, 13):  # Assuming departments IDs range from 1 to 12
                department_conditions |= Q(department_id=department_id)

            # Fetch all relevant budget totals in a single query
            budget_totals = BudgetTotals.objects.filter(
                Q(budget_set=budget_set) & Q(posted=False) & department_conditions
            ).order_by('-department_id', '-last_updated')

            # Create separate variables for each department
            ceo = budget_totals.filter(department_id=1)
            paginator = Paginator(ceo, 10)
            page_number = request.GET.get('page')
            ceo_obj = paginator.get_page(page_number)
            internal_audit = budget_totals.filter(department_id=2)
            paginator = Paginator(internal_audit, 10)
            page_number = request.GET.get('page')
            internal_audit_obj = paginator.get_page(page_number)
            supply_chain = budget_totals.filter(department_id=3)
            paginator = Paginator(supply_chain, 10)
            page_number = request.GET.get('page')
            supply_chain_obj = paginator.get_page(page_number)
            bds = budget_totals.filter(department_id=4)
            paginator = Paginator(bds, 10)
            page_number = request.GET.get('page')
            bds_obj = paginator.get_page(page_number)
            public_relations = budget_totals.filter(department_id=10)
            paginator = Paginator(public_relations, 10)
            page_number = request.GET.get('page')
            public_relations_obj = paginator.get_page(page_number)
            technical = budget_totals.filter(department_id=6)
            paginator = Paginator(technical, 10)
            page_number = request.GET.get('page')
            technical_obj = paginator.get_page(page_number)
            information_systems = budget_totals.filter(department_id=7)
            paginator = Paginator(information_systems, 10)
            page_number = request.GET.get('page')
            information_systems_obj = paginator.get_page(page_number)
            legal_risk = budget_totals.filter(department_id=8)
            paginator = Paginator(legal_risk, 10)
            page_number = request.GET.get('page')
            legal_risk_obj = paginator.get_page(page_number)
            human_capital = budget_totals.filter(department_id=9)
            paginator = Paginator(human_capital, 10)
            page_number = request.GET.get('page')
            human_capital_obj = paginator.get_page(page_number)
            sales_marketing = budget_totals.filter(department_id=10)
            paginator = Paginator(sales_marketing, 10)
            page_number = request.GET.get('page')
            sales_marketing_obj = paginator.get_page(page_number)
            admin = budget_totals.filter(department_id=11)
            paginator = Paginator(admin, 10)
            page_number = request.GET.get('page')
            admin_page_obj = paginator.get_page(page_number)
            finance = budget_totals.filter(department_id=12)
            paginator = Paginator(finance, 10)
            page_number = request.GET.get('page')
            finance_page_obj = paginator.get_page(page_number)
            # Calculate total sum
            total_sum = budget_totals.aggregate(total_sum=Sum('total'))['total_sum']

            # Populate context variable
            context = {
                'ceo': ceo_obj,
                'internal_audit': internal_audit_obj,
                'supply_chain': supply_chain_obj,
                'bds': bds_obj,
                'public_relations': public_relations_obj,
                'technical': technical_obj,
                'information_systems': information_systems_obj,
                'legal_risk': legal_risk_obj,
                'human_capital': human_capital_obj,
                'sales_marketing': sales_marketing_obj,
                'admin': admin_page_obj,
                'finance': finance_page_obj,
                'budget_set': budget_set,
                'total': total_sum
            }
            return render(request, 'opex-index.html', context)
        else:
            return redirect('budgets:login')

def reports(request):

    return render(request, 'reports.html')

def generate_excel(request):
        # Define the header row for the Excel file
        excel_header = ['Account Number', 'Period 1', 'Period 2', 'Period 3', 'Q1', 'Period 4', 'Period 5', 'Period 6',
                        'Q2', 'H1', 'Period 7', 'Period 8', 'Period 9',
                        'Q3', 'Period 10', 'Period 11', 'Period 12', 'Q4', 'H2', 'TOTAL']
        quarter_periods = [1, 2, 3, 4]
        half1_periods = [1, 2, 3, 4, 5, 6]
        half2_periods = [7, 8, 9, 10, 11, 12]

        # Grouping the values according to quarters and halves
        budget_totals = defaultdict(lambda: defaultdict(Decimal))

        for budget_total in BudgetTotals.objects.exclude(total=0).all():
            for period in range(1, 13):
                value = getattr(budget_total, f'period{period}', Decimal('0'))
                budget_totals[budget_total.account][f'Period {period}'] = value
                for quarter in range(1, 5):
                    start_period = (quarter - 1) * 3 + 1
                    end_period = quarter * 3
                    quarter_value = sum(getattr(budget_total, f'period{period}', Decimal('0')) for period in
                                        range(start_period, end_period + 1))
                    budget_totals[budget_total.account][f'Q{quarter}'] = quarter_value

                half1_value = sum(getattr(budget_total, f'period{period}', Decimal('0')) for period in half1_periods)
                budget_totals[budget_total.account]['H1'] = half1_value

                half2_value = sum(getattr(budget_total, f'period{period}', Decimal('0')) for period in half2_periods)
                budget_totals[budget_total.account]['H2'] = half2_value
            budget_totals[budget_total.account]['TOTAL'] = getattr(budget_total, 'total', Decimal('0'))

        # Create a new Excel workbook
        workbook = Workbook()
        sheet = workbook.active

        # Writing the header row with bold and blue background color
        for col, header in enumerate(excel_header, start=1):
            cell = sheet.cell(row=1, column=col)
            cell.value = header
            cell.font = cell.font.copy(bold=True, color=colors.WHITE)
            cell.fill = cell.fill.copy(fill_type='solid', start_color='00008B')

        # Writing the data rows

        for row, (account, totals) in enumerate(budget_totals.items(), start=2):
            sheet.cell(row=row, column=1, value=account.pk)
            for col, period in enumerate(excel_header[1:], start=2):
                if 'P' in period:
                    sheet.cell(row=row, column=col, value=Decimal(totals[period]))
                elif 'Q' in period:
                    sheet.cell(row=row, column=col, value=Decimal(totals[period]))
                elif period == 'H1':
                    sheet.cell(row=row, column=col, value=Decimal(totals[period]))
                elif period == 'H2':
                    sheet.cell(row=row, column=col, value=Decimal(totals[period]))
                elif period == 'TOTAL':
                    sheet.cell(row=row, column=col, value=Decimal(totals[period]))

        # Create a HttpResponse with an Excel file attachment
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="budget_totals.xlsx"'

        # Save the workbook to the HttpResponse
        workbook.save(response)

        return response

def department_budget_settings(request, dept_id):
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
                BudgetStatus.objects.filter(department=request.user.department,
                                            budget_set=request.GET.get('budget_id')).update(is_complete=True,
                                                                                            is_active=False,
                                                                                            comment=request.GET.get(
                                                                                                'comment'))
                return JsonResponse({'result': 'success'})
            elif request.GET.get('incomplete') == '1':
                if request.user.role != '002':
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
                BudgetStatus.objects.filter(department=request.user.department, budget_set=budget).update(
                    is_complete=False,
                    comment=request.GET.get(
                        'comment'))
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
                BudgetStatus.objects.filter(department=request.user.department,
                                            budget_set=request.GET.get('budget_id')).update(is_complete=True,
                                                                                            is_active=False,
                                                                                            comment=request.GET.get(
                                                                                                'comment'))
                return JsonResponse({'result': 'success'})
            elif request.GET.get('incomplete') == '1':
                if request.user.role != '002':
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
                BudgetStatus.objects.filter(department=request.user.department, budget_set=budget).update(
                    is_complete=False,
                    comment=request.GET.get(
                        'comment'))
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

                    obj = BudgetAssumptions.objects.filter(
                        department_id=request.user.department.id)  # Refresh assumptions
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
            context = {'assumptions': page_obj, 'currency': currency_obj, 'department': request.user.department.name}
            return render(request, 'assumptions.html', context)
        else:
            return redirect('budgets:login')

def accounts_search(request):
        field_mapping = {
            'account_id': 'account__acctid__icontains',
            'account_name': 'account__acctdesc__icontains',
        }

        filter = request.GET.get('filter')
        value = request.GET.get('value')
        dept = request.GET.get('department')
        active = BudgetStatus.objects.filter(is_active=True).values('budget_set')
        if dept:
            account_info = BudgetTotals.objects.filter(Q(budget_set__in=active), **{field_mapping[filter]: value},
                                                       department=dept).values('id', 'total', 'account_id',
                                                                               'account__acctdesc', 'year',
                                                                               'currency__currency', 'period1',
                                                                               'period2', 'period3', 'period4',
                                                                               'period5', 'period6', 'period7',
                                                                               'period8', 'period9', 'period10',
                                                                               'period11', 'period12').all()
            print(account_info)
            return JsonResponse({'data': list(account_info)}, status=200)
        else:
            if filter in field_mapping and value:
                if request.user.role != '002':
                    account_info = BudgetTotals.objects.filter(Q(budget_set__in=active),
                                                               **{field_mapping[filter]: value},
                                                               department=request.user.department).values(
                        'account_id', 'account__acctdesc', 'id').all()
                    return JsonResponse({'data': list(account_info)}, status=200)
                else:
                    account_info = BudgetTotals.objects.filter(Q(budget_set__in=active),
                                                               **{field_mapping[filter]: value}).values(
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

def toggle_status_incomplete(request, id):
        budget_obj = BudgetStatus.objects.get(id=id)
        budget_obj.is_complete = False
        budget_obj.save()
        return redirect('budgets:settings')

def toggle_status_complete(request, id):
        budget_obj = BudgetStatus.objects.get(id=id)
        budget_obj.is_complete = True
        budget_obj.save()
        return redirect('budgets:settings')

def toggle_status_false(request, id):
        budget_obj = BudgetStatus.objects.get(id=id)
        budget_obj.is_active = False
        budget_obj.save()
        return redirect('budgets:settings')

def toggle_status_true(request, id):
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
        dept = line.department_id
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
        return redirect('budgets:update-expenses', dept)

def changelog(request):
        if request.user.is_authenticated:
            obj = BudgetLinesLog.objects.all()
            paginator = Paginator(obj, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'changelog.html', {'changes': page_obj})
        else:
            return redirect('budgets:login')

def update(request, object_id):
        if request.user.is_authenticated:

            obj_t = get_object_or_404(BudgetTotals, id=object_id)
            lines = BudgetLines.objects.filter(account__acctid=obj_t.account.acctid)

            active = get_object_or_404(BudgetStatus, department_id=obj_t.department.id, is_active=True)
            if active:
                if request.user.role != '002':
                    single_object = BudgetTotals.objects.filter(budget_set=active.budget_set,
                                                                department=request.user.department)
                else:
                    single_object = BudgetTotals.objects.filter(budget_set=active.budget_set)

                first_dept_obj = BudgetTotals.objects.filter(budget_set=active.budget_set,
                                                             department_id=obj_t.department.id,
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

                first_obj = BudgetTotals.objects.filter(department_id=obj_t.department.id,
                                                        budget_set=active.budget_set).first()
                last_obj = BudgetTotals.objects.filter(department_id=obj_t.department.id,
                                                       budget_set=active.budget_set).last()

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

def delete_assumption(request, id):
        BudgetAssumptions.objects.filter(id=id).delete()
        return redirect('budgets:assumptions')

def delete_currency(request, id):
        Currency.objects.filter(id=id).delete()
        return redirect('budgets:assumptions')

def update_expenses(request, department_id):
        if request.user.is_authenticated:
            active = get_object_or_404(BudgetStatus, department_id=department_id, is_active=True)

            if active:
                if request.user.role != '002':
                    single_object = BudgetTotals.objects.filter(budget_set=active.budget_set,
                                                                department=request.user.department)
                else:
                    single_object = BudgetTotals.objects.filter(budget_set=active.budget_set)

                first_dept_obj = BudgetTotals.objects.filter(budget_set=active.budget_set,
                                                             department_id=department_id).first()
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

                first_obj = BudgetTotals.objects.filter(department_id=department_id,
                                                        budget_set=active.budget_set).first()
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
        objects = BudgetTotals.objects.filter(budget_set=budget_set).exclude(total=0)
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

                        return redirect('budgets:home-dept', f'{active.budget_set}')
                    """user_obj = get_object_or_404(Users, username=username)
                    totp = pyotp.TOTP(user.otp_base32).now()
                    user_obj.login_otp = totp
                    user_obj.otp_created_at = datetime.now(timezone.utc)
                    user_obj.login_otp_used = False
                    user_obj.save(update_fields=["login_otp", "otp_created_at", "login_otp_used"])
                    #return redirect('budgets:enter-otp')"""
                    return redirect('budgets:dashboard-home')
                else:
                    messages.error(request, message="Username/Password not registered")
                    return redirect("budgets:login")

            except Exception as e:
                print(e)
                messages.error(request, message="An error occurred. Please try again.")

                return redirect("budgets:login")

        else:

            return render(request, 'login.html')
