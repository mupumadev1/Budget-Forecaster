from django.contrib import admin

from budgets.models import BudgetLines, Department, Users, BudgetComments, BudgetStatus, BudgetAssumptions, \
    BudgetTotals, Accounts, ChangeLog, BudgetLinesLog, BudgetVariations

# Register your models here.
admin.site.register(BudgetLines)
admin.site.register(BudgetVariations)
admin.site.register(BudgetTotals)
admin.site.register(Accounts)
admin.site.register(Users)
admin.site.register(Department)
admin.site.register(BudgetComments)
admin.site.register(BudgetStatus)
admin.site.register(BudgetAssumptions)
admin.site.register(ChangeLog)
admin.site.register(BudgetLinesLog)
