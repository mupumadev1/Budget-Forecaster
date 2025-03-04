from decimal import Decimal

from django import template
from django.shortcuts import get_object_or_404

from budgets.models import BudgetStatus, BudgetLines, BudgetTotals, BudgetVariations, FinancialYear

register = template.Library()


@register.filter(name='calculate_sum_month')
def calculate_sum(queryset, netperd):
    return sum(getattr(obj, f'netperd{netperd}') for obj in queryset)


@register.filter(name='calculate_sums')
def calculate_sum(dept_totals, netperd):
    # Initialize sum
    total = 0

    # Iterate over values (which are lists of dictionaries) in dept_totals
    for department_data in dept_totals.values():
        # Iterate over dictionaries in the list
        for obj in department_data:
            value = obj.get(netperd, 0)
            if isinstance(value, str):
                value = Decimal(value)
            total += value

    return total


@register.filter(name='calculate_sum_quarter')
def calculate_sum_quarter(obj, q):
    if q == 1:
        return sum(getattr(obj, f'netperd{i}', 0) for i in range(1, 4))
    elif q == 2:
        return sum(getattr(obj, f'netperd{i}', 0) for i in range(4, 7))
    elif q == 3:
        return sum(getattr(obj, f'netperd{i}', 0) for i in range(7, 10))
    elif q == 4:
        return sum(getattr(obj, f'netperd{i}', 0) for i in range(10, 13))
    else:
        raise (ValueError("Quarter number should be between 1 and 4"))


@register.filter(name='calculate_sum_half')
def calculate_sum_half(obj, q):
    if q == 1:
        return sum(getattr(obj, f'netperd{i}', 0) for i in range(1, 7))
    elif q == 2:
        return sum(getattr(obj, f'netperd{i}', 0) for i in range(7, 13))

@register.filter(name='department')
def determine_department(obj):
    if obj.department != 13:
        return 'opex'
    elif obj.department == 13:
        return 'capex'

@register.filter(name='calculate_sum')
def calculate_sum(queryset):
    return sum(obj.total for obj in queryset)


@register.filter(name='get_dept')
def get_dept(queryset):
    for obj in queryset:
        return obj.department.id


@register.filter(name='calculate_obj_id')
def calculate_obj_id(user):
    if user.department.id == 12:
        status = BudgetStatus.objects.filter(is_active=True).first()
        for s in status:
            active = get_object_or_404(BudgetStatus, department=s.department.id, is_active=True)
            budget = BudgetLines.objects.filter(department=active.department,
                                                budget_set=active.get_budget_set_display()).first()
            if budget:
                return budget.id
    else:
        department = user.department
        if department:
            active = get_object_or_404(BudgetStatus, department=department.id, is_active=True)

            budget = BudgetTotals.objects.filter(department=department, budget_set=active.budget_set).first()
            if budget:
                return budget.id
        return None


@register.filter(name='budget_status_filter')
def budget_status(queryset):
    for object in queryset:
        obj = get_object_or_404(BudgetVariations, budget_set=object.budget_set)
        if obj.is_complete:
            return True
        else:
            return False


@register.filter(name='budget_active_filter')
def budget_status(queryset):
    year= FinancialYear.objects.get(is_active=True)
    for object in queryset:
        obj = get_object_or_404(BudgetVariations, budget_set=object.budget_set,year=year.year)
        if obj.is_active:
            return True
        else:
            return False


@register.filter(name='object_complete_filter')
def budget_status(objct):
    obj = get_object_or_404(BudgetVariations, budget_set=objct.budget_set)
    if obj.is_complete:
        return True
    else:
        return False
