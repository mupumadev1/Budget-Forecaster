# Generated by Django 5.0.3 on 2024-10-06 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0017_budgetlineslogvariations'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetlineslogvariations',
            name='year',
            field=models.CharField(default='2024', max_length=4),
        ),
    ]
