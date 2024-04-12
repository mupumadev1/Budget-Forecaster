from django import template
from django.shortcuts import get_object_or_404

from budgets.models import BudgetStatus, BudgetLines, BudgetTotals

register = template.Library()


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
            budget = BudgetLines.objects.filter(department=active.department, budget_set=active.get_budget_set_display()).first()
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
        obj = get_object_or_404(BudgetStatus, department=object.department, budget_set=object.budget_set)
        if obj.is_complete:
            return True
        else:
            return False


@register.filter(name='budget_active_filter')
def budget_status(queryset):
    for object in queryset:
        obj = get_object_or_404(BudgetStatus, department=object.department, budget_set=object.budget_set)
        if obj.is_active:
            return True
        else:
            return False
