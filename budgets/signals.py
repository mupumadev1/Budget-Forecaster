import datetime
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from budgets import models
from budgets.models import BudgetStatus, Users, ChangeLog, BudgetLines, BudgetLinesLog, BudgetTotals
from django.db.models import F

@receiver(pre_save, sender=BudgetStatus)
def ensure_single_active(sender, instance, **kwargs):
    if instance.is_active:
        dept = instance.department.id
        # Ensure that only one object has a True value
        if sender.objects.filter(is_active=True,department_id=dept).exclude(id=instance.id).exists():
            instance.is_active = False
            instance.full_clean()
            raise ValidationError('There can only be one active budget-set per department')
        # Set all other objects to False

@receiver(post_save, sender=BudgetLines)
def save_budget_line_log(sender, instance, created, **kwargs):
    if created:
        action = 'Added'
    else:
        action = 'Updated'

    # Check if the flag is True in the BudgetLinesLog model
    if ChangeLog.objects.filter(department=instance.department.id,budget_set=instance.budget_set, flag=True).exists():


        BudgetLinesLog.objects.create(
            timestamp=datetime.datetime.now(),
            user_id=instance.last_updated_by_id,
            action=action,
            item_description=instance.item_description,
            total=instance.total,
            account=instance.account,
            department=instance.department.name,
            budget_set=instance.budget_set
        )





def round_to_two_places(value):

        return value.quantize(Decimal('0.00'))

@receiver(pre_save, sender=BudgetLines)
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
            else:
                BudgetTotals.objects.filter(account=instance.account, currency=instance.currency,
                                            department=instance.department, year=instance.year).update(
                    **{field_name: F(field_name) + difference})

@receiver(pre_delete, sender=BudgetLines)
def delete_budget_line_log(sender, instance, **kwargs):
    if ChangeLog.objects.filter(department=instance.department.id,budget_set=instance.budget_set, flag=True).exists():

        BudgetLinesLog.objects.create(
            timestamp= datetime.datetime.now(),
            user_id=instance.last_updated_by_id,
            action='Removed',
            item_description=instance.item_description,
            total=instance.total,
            account=instance.account,
            department=instance.department.name,
            budget_set=instance.budget_set
        )


@receiver(pre_save, sender=BudgetStatus)
def handle_budget_status_changes(sender, instance, **kwargs):
    if instance.pk:  # Check if instance already exists (not being created)
        original = sender.objects.get(pk=instance.pk)

        # Update flag field in ChangeLog model based on is_complete changes
        if original.is_complete and not instance.is_complete:  # Change condition here
            log_obj = ChangeLog.objects.filter(department=instance.department, budget_set=instance.budget_set)
            if log_obj.exists():
                log_obj.update(flag=True)
            else:
                ChangeLog.objects.create(flag=True,department=instance.department, budget_set=instance.budget_set)
        elif not original.is_complete and instance.is_complete:
            ChangeLog.objects.filter(department=instance.department, budget_set=instance.budget_set).update(
                flag=False)

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