import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from budgets.models import BudgetStatus, Users, ChangeLog, BudgetLines, BudgetLinesLog


@receiver(pre_save, sender=BudgetStatus)
def ensure_single_active(sender, instance, **kwargs):
    if instance.is_active:
        dept = instance.department.id
        # Ensure that only one object has a True value
        if sender.objects.filter(is_active=True,department_id=dept).exclude(id=instance.id).exists():
            raise ValidationError('There can only be one active budget-set per department')
        # Set all other objects to False
        sender.objects.filter(is_active=True).exclude(id=instance.id).update(is_active=False)

@receiver(post_save, sender=BudgetLines)
def save_budget_line_log(sender, instance, created, **kwargs):
    if created:
        action = 'Created'
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
            department=instance.department.name,
            budget_set=instance.budget_set
        )

@receiver(pre_delete, sender=BudgetLines)
def delete_budget_line_log(sender, instance, **kwargs):
    if ChangeLog.objects.filter(department=instance.department.id,budget_set=instance.budget_set, flag=True).exists():

        BudgetLinesLog.objects.create(
            timestamp= datetime.datetime.now(),
            user_id=instance.last_updated_by_id,
            action='Deleted',
            item_description=instance.item_description,
            total=instance.total,
            department=instance.department.name,
            budget_set=instance.budget_set
        )


@receiver(pre_save, sender=BudgetStatus)
def handle_budget_status_changes(sender, instance, **kwargs):
    if instance.pk:  # Check if instance already exists (not being created)
        original = sender.objects.get(pk=instance.pk)

        # Update flag field in ChangeLog model based on is_complete changes
        if original.is_complete and not instance.is_complete:  # Change condition here
            ChangeLog.objects.filter(department=instance.department, budget_set=instance.budget_set).update(
                flag=True)
        elif not original.is_complete and instance.is_complete:
            ChangeLog.objects.filter(department=instance.department, budget_set=instance.budget_set).update(
                flag=False)

        # Send notifications based on is_complete changes
        if original.is_complete != instance.is_complete:
            channel_layer = get_channel_layer()
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