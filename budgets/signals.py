import datetime
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from budgets import models
from budgets.models import BudgetStatus, Users, ChangeLog, BudgetLines, BudgetLinesLog, BudgetTotals, FinancialYear
from django.db.models import F, Sum


@receiver(pre_save, sender=BudgetStatus)
def ensure_single_active(sender, instance, **kwargs):
    if instance.is_active:
        dept = instance.department.id
        # Ensure that only one object has a True value
        if sender.objects.filter(is_active=True,department_id=dept,year='2025').exclude(id=instance.id).exists():
            instance.is_active = False
            instance.full_clean()
            raise ValidationError('There can only be one active budget-set per department')
        # Set all other objects to False


def log_budget_line_action(budget_line, action, user):
    BudgetLinesLog.objects.create(
        user=user,
        action=action,
        amount=budget_line.total,  # You can log a specific amount or total
        item_description=budget_line.item_description,
        account=budget_line.account,
        total=budget_line.total,
        netperd1=budget_line.netperd1,
        netperd2=budget_line.netperd2,
        netperd3=budget_line.netperd3,
        netperd4=budget_line.netperd4,
        netperd5=budget_line.netperd5,
        netperd6=budget_line.netperd6,
        netperd7=budget_line.netperd7,
        netperd8=budget_line.netperd8,
        netperd9=budget_line.netperd9,
        netperd10=budget_line.netperd10,
        netperd11=budget_line.netperd11,
        netperd12=budget_line.netperd12,
        department = budget_line.department,
        year=budget_line.year
    )


# Signal to log updates and additions
@receiver(post_save, sender=BudgetLines)
def log_budget_lines_save(sender, instance, created, **kwargs):

    year = FinancialYear.objects.get(is_active=True)
    if ChangeLog.objects.filter(year=year.year, flag=True,
                                        ).exists():
                user = instance.last_updated_by  # Assuming you have a way to access the user who made the changes
                action = 'created' if created else 'updated'

                # Log the action
                log_budget_line_action(instance, action, user)




# Signal to log deletions
@receiver(pre_delete, sender=BudgetLines)
def log_budget_lines_delete(sender, instance, **kwargs):
    year = FinancialYear.objects.get(is_active=True)

    if ChangeLog.objects.filter( flag=True,
                                year=year.year).exists():
        user = instance.last_updated_by  # Assuming you have a way to access the user who made the changes

        # Log the delete action
        log_budget_line_action(instance, 'deleted', user)



def round_to_two_places(value):

        return value.quantize(Decimal('0.00'))

"""@receiver(pre_save, sender=BudgetLines)
def track_budget_changes(sender, instance, **kwargs):
    try:
        old_instance = BudgetLines.objects.get(pk=instance.pk)
    except BudgetLines.DoesNotExist:
        # New instance, no old instance to compare with
        return
    fields_to_compare = [field.name for field in BudgetLines._meta.fields]

    # Dictionary to store changes
    changes = {}

    for field in fields_to_compare:

        old_value = getattr(old_instance, field)
        new_value = getattr(instance, field)
        if isinstance(new_value,Decimal):
            new_value = round_to_two_places(new_value)
            if old_value != new_value:
                changes[field] = old_value - new_value
        else:
            if old_value != new_value:
                changes[field] = new_value


            # If there are changes, you can handle them here
    print(changes)


    # Update BudgetTotals based on differences
    for field_name, difference in changes.items():
        if hasattr(BudgetTotals, field_name):
            if field_name == 'last_updated':
                BudgetTotals.objects.filter(account=instance.account, currency=instance.currency,
                                            department=instance.department, year=instance.year).update(
                    **{field_name: datetime.datetime.now()})
            elif field_name == 'last_updated_by':
                BudgetTotals.objects.filter(account=instance.account, currency=instance.currency,
                                            department=instance.department, year=instance.year).update(
                    **{field_name: instance.last_updated_by})
            else:
                BudgetTotals.objects.filter(account=instance.account, currency=instance.currency,
                                            department=instance.department, year=instance.year).update(
                    **{field_name: F(field_name) + difference})"""


@receiver(post_save, sender=BudgetLines)
def update_budget_totals_on_save(sender, instance, created, **kwargs):
    """
    Updates the BudgetTotals table whenever a BudgetLines instance is saved (created or updated).
    """
    year = instance.year
    budget_set = instance.budget_set
    account = instance.account

    try:
        budget_total = BudgetTotals.objects.get(
            account=account, budget_set=budget_set, year=year
        )
    except BudgetTotals.DoesNotExist:
        print(
            f"BudgetTotals object not found for account {account}, budget_set {budget_set}, year {year}. Creation might be needed.")
        return  # Exit if not found

    # Calculate the sum of all BudgetLines for this account, budget_set, and year
    total_from_lines = BudgetLines.objects.filter(
        account=account, budget_set=budget_set, year=year
    ).aggregate(total_sum=Sum('total'))['total_sum'] or Decimal('0.00')

    # Update the netperds from BudgetLines
    netperd_totals = BudgetLines.objects.filter(
        account=account, budget_set=budget_set, year=year
    ).aggregate(
        netperd1_sum=Sum('netperd1'),
        netperd2_sum=Sum('netperd2'),
        netperd3_sum=Sum('netperd3'),
        netperd4_sum=Sum('netperd4'),
        netperd5_sum=Sum('netperd5'),
        netperd6_sum=Sum('netperd6'),
        netperd7_sum=Sum('netperd7'),
        netperd8_sum=Sum('netperd8'),
        netperd9_sum=Sum('netperd9'),
        netperd10_sum=Sum('netperd10'),
        netperd11_sum=Sum('netperd11'),
        netperd12_sum=Sum('netperd12')
    )

    # Update the BudgetTotals object with the new total and netperds
    budget_total.total = total_from_lines
    budget_total.netperd1 = netperd_totals['netperd1_sum'] or Decimal('0.00')
    budget_total.netperd2 = netperd_totals['netperd2_sum'] or Decimal('0.00')
    budget_total.netperd3 = netperd_totals['netperd3_sum'] or Decimal('0.00')
    budget_total.netperd4 = netperd_totals['netperd4_sum'] or Decimal('0.00')
    budget_total.netperd5 = netperd_totals['netperd5_sum'] or Decimal('0.00')
    budget_total.netperd6 = netperd_totals['netperd6_sum'] or Decimal('0.00')
    budget_total.netperd7 = netperd_totals['netperd7_sum'] or Decimal('0.00')
    budget_total.netperd8 = netperd_totals['netperd8_sum'] or Decimal('0.00')
    budget_total.netperd9 = netperd_totals['netperd9_sum'] or Decimal('0.00')
    budget_total.netperd10 = netperd_totals['netperd10_sum'] or Decimal('0.00')
    budget_total.netperd11 = netperd_totals['netperd11_sum'] or Decimal('0.00')
    budget_total.netperd12 = netperd_totals['netperd12_sum'] or Decimal('0.00')

    # Update last_updated field if needed
    budget_total.last_updated = datetime.datetime.now()

    # Save changes to BudgetTotals
    budget_total.save()

    print(
        f"BudgetTotals updated for account {account}, budget_set {budget_set}, year {year}. New total: {total_from_lines}")

@receiver(pre_save, sender=BudgetStatus)
def handle_budget_status_changes(sender, instance, **kwargs):
    if instance.pk:  # Check if instance already exists (not being created)
        original = sender.objects.get(pk=instance.pk)

        # Update flag field in ChangeLog model based on is_complete changes


        # Send notifications based on is_complete changes
        if original.is_complete != instance.is_complete:
            channel_layer = get_channel_layer()
            id = instance
            if instance.is_complete:
                message = "Budget Set " + instance.get_budget_set_display() + " from the " + instance.department.name + " department has been marked as complete"
            else:
                message = "Changes to be made to budget Set " + instance.get_budget_set_display() + " from the " + instance.department.name + " department require your approval"

            async_to_sync(channel_layer.group_send)(
                'public_room',
                {
                    "type": "send_notification",
                    "message": message
                }
            )