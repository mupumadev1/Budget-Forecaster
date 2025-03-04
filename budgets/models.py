from datetime import datetime, timezone
from decimal import Decimal

from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from simple_history.models import HistoricalRecords

ROLE = (
    ('001', "department user"),  # Adds Bank Details
    ('002', "budget manager"),  # Posts Transactions
)
SET_TYPE = (
    ('Budget 1', '1'),
    ('Budget 2', '2'),
    ('Budget 3', '3'),

)
YEAR = (
    ('2024', '2024'),
    ('2025', '2025'),
    ('2026', '2026'),

)


class Department(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)


class Group(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    parent_group = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_groups')

    def __str__(self):
        return self.name

class Accounts(models.Model):
    acctid = models.CharField(db_column='ACCTID', primary_key=True, max_length=45,
                              )
    group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True)

    audtdate = models.DecimalField(db_column='AUDTDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    audttime = models.DecimalField(db_column='AUDTTIME', max_digits=9, decimal_places=0)  # Field name made lowercase.
    audtuser = models.CharField(db_column='AUDTUSER', max_length=8,
                                )  # Field name made lowercase.
    audtorg = models.CharField(db_column='AUDTORG', max_length=6,
                               )  # Field name made lowercase.
    createdate = models.DecimalField(db_column='CREATEDATE', max_digits=9,
                                     decimal_places=0)  # Field name made lowercase.
    acctdesc = models.CharField(db_column='ACCTDESC', max_length=60,
                                )  # Field name made lowercase.
    accttype = models.CharField(db_column='ACCTTYPE', max_length=1,
                                )  # Field name made lowercase.
    acctbal = models.CharField(db_column='ACCTBAL', max_length=1,
                               )  # Field name made lowercase.
    activesw = models.SmallIntegerField(db_column='ACTIVESW')  # Field name made lowercase.
    consldsw = models.SmallIntegerField(db_column='CONSLDSW')  # Field name made lowercase.
    qtysw = models.SmallIntegerField(db_column='QTYSW')  # Field name made lowercase.
    uom = models.CharField(db_column='UOM', max_length=6,
                           )  # Field name made lowercase.
    allocsw = models.SmallIntegerField(db_column='ALLOCSW')  # Field name made lowercase.
    acctofset = models.CharField(db_column='ACCTOFSET', max_length=45,
                                 )  # Field name made lowercase.
    acctsrty = models.CharField(db_column='ACCTSRTY', max_length=2,
                                )  # Field name made lowercase.
    mcsw = models.SmallIntegerField(db_column='MCSW')  # Field name made lowercase.
    specsw = models.SmallIntegerField(db_column='SPECSW')  # Field name made lowercase.
    acctgrpcod = models.CharField(db_column='ACCTGRPCOD', max_length=12,
                                  )  # Field name made lowercase.
    ctrlacctsw = models.SmallIntegerField(db_column='CTRLACCTSW')  # Field name made lowercase.
    srceldgid = models.CharField(db_column='SRCELDGID', max_length=2,
                                 )  # Field name made lowercase.
    alloctot = models.DecimalField(db_column='ALLOCTOT', max_digits=15, decimal_places=7)  # Field name made lowercase.
    abrkid = models.CharField(db_column='ABRKID', max_length=6,
                              )  # Field name madeite
    yracctclos = models.DecimalField(db_column='YRACCTCLOS', max_digits=7,
                                     decimal_places=0)  # Field name made lowercase.
    acctfmttd = models.CharField(db_column='ACCTFMTTD', max_length=45,
                                 )  # Field name made lowercase.
    acsegval01 = models.CharField(db_column='ACSEGVAL01', max_length=15,
                                  )  # Field name made lowercase.
    acsegval02 = models.CharField(db_column='ACSEGVAL02', max_length=15,
                                  )  # Field name made lowercase.
    acsegval03 = models.CharField(db_column='ACSEGVAL03', max_length=15,
                                  )  # Field name made lowercase.
    acsegval04 = models.CharField(db_column='ACSEGVAL04', max_length=15,
                                  )  # Field name made lowercase.
    acsegval05 = models.CharField(db_column='ACSEGVAL05', max_length=15,
                                  )  # Field name made lowercase.
    acsegval06 = models.CharField(db_column='ACSEGVAL06', max_length=15,
                                  )  # Field name made lowercase.
    acsegval07 = models.CharField(db_column='ACSEGVAL07', max_length=15,
                                  )  # Field name made lowercase.
    acsegval08 = models.CharField(db_column='ACSEGVAL08', max_length=15,
                                  )  # Field name made lowercase.
    acsegval09 = models.CharField(db_column='ACSEGVAL09', max_length=15,
                                  )  # Field name made lowercase.
    acsegval10 = models.CharField(db_column='ACSEGVAL10', max_length=15,
                                  )  # Field name made lowercase.
    acctsegval = models.CharField(db_column='ACCTSEGVAL', max_length=15,
                                  )  # Field name made lowercase.
    acctgrpscd = models.CharField(db_column='ACCTGRPSCD', max_length=12,
                                  )  # Field name made lowercase.
    postosegid = models.CharField(db_column='POSTOSEGID', max_length=6,
                                  )  # Field name made lowercase.
    defcurncod = models.CharField(db_column='DEFCURNCOD', max_length=3,
                                  )  # Field name made lowercase.
    ovalues = models.IntegerField(db_column='OVALUES')  # Field name made lowercase.
    tovalues = models.IntegerField(db_column='TOVALUES')  # Field name made lowercase.
    rollupsw = models.SmallIntegerField(db_column='ROLLUPSW')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    


class Users(AbstractUser, PermissionsMixin):
    role = models.CharField(max_length=255, choices=ROLE, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    otpauth_url = models.CharField(max_length=225, blank=True, null=True)
    otp_base32 = models.CharField(max_length=255, null=True, blank=True)
    qr_code = models.ImageField(upload_to="qrcode/", blank=True, null=True)
    login_otp = models.CharField(max_length=255, null=True, blank=True)
    login_otp_used = models.BooleanField(default=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    

    def is_valid_otp(self):
        lifespan_in_seconds = 30
        now = datetime.now(timezone.utc)
        time_diff = now - self.otp_created_at
        time_diff = time_diff.total_seconds()
        if time_diff >= lifespan_in_seconds or self.login_otp_used:
            return False
        return True


class Currency(models.Model):
    currency = models.CharField(max_length=255)
    rate = models.DecimalField(decimal_places=2, max_digits=10)

    updated_by = models.ForeignKey(Users, on_delete=models.CASCADE)


class BudgetVariations(models.Model):
    budget_set = models.CharField(max_length=255, choices=SET_TYPE)
    year = models.CharField(max_length=4, choices=YEAR)
    is_active = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    is_posted = models.BooleanField(default=False)
    updated_by = models.ForeignKey(Users, on_delete=models.CASCADE)

class FinancialYear(models.Model):
    is_active = models.BooleanField(default=False)
    year = models.CharField(max_length=4, choices=YEAR)

class BudgetAssumptions(models.Model):
    factor = models.CharField(max_length=255, null=True)
    rate = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(Users, on_delete=models.CASCADE)




class BudgetTotals(models.Model):
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default=1)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.CharField(max_length=4, default='2024')
    total = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd1 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd2 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd3 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd4 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd5 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd6 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd7 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd8 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd9 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd10 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd11 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd12 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    budget_set = models.CharField(max_length=255, choices=SET_TYPE)
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    posted = models.BooleanField(default=False)
    exchange_rate = models.DecimalField(decimal_places=2, max_digits=20, null=True)


    def calculate_quarter_sums(self):
        # Calculate the sum of each quarter based on the netperd fields
        q1 = self.netperd1 + self.netperd2 + self.netperd3
        q2 = self.netperd4 + self.netperd5 + self.netperd6
        q3 = self.netperd7 + self.netperd8 + self.netperd9
        q4 = self.netperd10 + self.netperd11 + self.netperd12

        # Update the instance with the calculated quarter sums
        self.Q1 = q1
        self.Q2 = q2
        self.Q3 = q3
        self.Q4 = q4

        # Save the instance to persist the changes
        self.save()

    def calculate_half_sums(self):
        # Calculate the sum of each quarter based on the netperd fields
        h1 = self.netperd1 + self.netperd2 + self.netperd3 + self.netperd4 + self.netperd5 + self.netperd6
        h2 = self.netperd7 + self.netperd8 + self.netperd9 + self.netperd10 + self.netperd11 + self.netperd12

        # Update the instance with the calculated quarter sums
        self.H1 = h1
        self.H2 = h2

        # Save the instance to persist the changes
        self.save()




class ChangeLog(models.Model):
    flag = models.BooleanField(default=False)
    year = models.CharField(max_length=4, default='2024', null=True)
    budget_set = models.CharField(max_length=255, null=True)

    def toggle_flag(self):
        # Toggle the value of the flag
        self.flag = not self.flag
        # Save the instance to persist the change in the database
        self.save()

class BudgetLinesLogVariations(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    amount= models.DecimalField(decimal_places=2, max_digits=20,null=True)
    item_description = models.CharField(max_length=255, null=True)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE,default='11140                                        ')
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=True)
    period = models.CharField(max_length=50)
    year = models.CharField(max_length=4, default='2024')
    comment= models.TextField()

class BudgetLinesLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    amount= models.DecimalField(decimal_places=2, max_digits=20,null=True)
    item_description = models.CharField(max_length=255, null=True)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE,default='11140                                        ')
    total = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=True)
    netperd1 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd2 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd3 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd4 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd5 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd6 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd7 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd8 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd9 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd10 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd11 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd12 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    year = models.CharField(max_length=4, default='2024')


class AccountChanges(models.Model):
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE,default='11140                                        ')
    initial = models.DecimalField(decimal_places=2, max_digits=20)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    netperd1 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd2 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd3 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd4 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd5 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd6 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd7 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd8 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd9 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd10 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd11 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd12 = models.DecimalField(decimal_places=2, max_digits=20, null=True)

# Create your models here.
class BudgetLines(models.Model):
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    item_description = models.CharField(max_length=255, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.CharField(max_length=4, default='2024')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default=1)
    assumption = models.ForeignKey(BudgetAssumptions, on_delete=models.CASCADE, null=True)
    rate = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    usage = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    staff = models.IntegerField(null=True)
    factor = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd1 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd2 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd3 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd4 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd5 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd6 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd7 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd8 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd9 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd10 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd11 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    netperd12 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    budget_set = models.CharField(max_length=255, choices=SET_TYPE)
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    posted = models.BooleanField(default=False)
    exchange_rate = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True)
    


class BudgetStatus(models.Model):
    budget_set = models.CharField(max_length=255, choices=SET_TYPE)
    year = models.CharField(max_length=4, default='2024')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=True)
    updated_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255, null=True, blank=True)
    


class BudgetComments(models.Model):
    BUDGET_FIELDS = (
        ('rate', 'Rate'),
        ('usage', 'Usage'),
        ('factor', 'Factor'),
        # Add other fields here as needed
    )
    budget = models.ForeignKey(BudgetLines, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100, choices=BUDGET_FIELDS)
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Glafs(models.Model):
    acctid = models.CharField(db_column='ACCTID', primary_key=True, max_length=45,
                              db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    fscsyr = models.CharField(db_column='FSCSYR', max_length=4,
                              db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    fscsdsg = models.CharField(db_column='FSCSDSG', max_length=1,
                               db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    fscscurn = models.CharField(db_column='FSCSCURN', max_length=3,
                                db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    curntype = models.CharField(db_column='CURNTYPE', max_length=1,
                                db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    audtdate = models.DecimalField(db_column='AUDTDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    audttime = models.DecimalField(db_column='AUDTTIME', max_digits=9, decimal_places=0)  # Field name made lowercase.
    audtuser = models.CharField(db_column='AUDTUSER', max_length=8,
                                db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    audtorg = models.CharField(db_column='AUDTORG', max_length=6,
                               db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    swrvl = models.SmallIntegerField(db_column='SWRVL')  # Field name made lowercase.
    codervl = models.CharField(db_column='CODERVL', max_length=6,
                               db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    scurndec = models.CharField(db_column='SCURNDEC', max_length=1,
                                db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    openbal = models.DecimalField(db_column='OPENBAL', max_digits=19, decimal_places=3)  # Field name made lowercase.
    netperd1 = models.DecimalField(db_column='NETPERD1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    netperd2 = models.DecimalField(db_column='NETPERD2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    netperd3 = models.DecimalField(db_column='NETPERD3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    netperd4 = models.DecimalField(db_column='NETPERD4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    netperd5 = models.DecimalField(db_column='NETPERD5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    netperd6 = models.DecimalField(db_column='NETPERD6', max_digits=19, decimal_places=3)  # Field name made lowercase.
    netperd7 = models.DecimalField(db_column='NETPERD7', max_digits=19, decimal_places=3)  # Field name made lowercase.
    netperd8 = models.DecimalField(db_column='NETPERD8', max_digits=19, decimal_places=3)  # Field name made lowercase.
    netperd9 = models.DecimalField(db_column='NETPERD9', max_digits=19, decimal_places=3)  # Field name made lowercase.
    netperd10 = models.DecimalField(db_column='NETPERD10', max_digits=19,
                                    decimal_places=3)  # Field name made lowercase.
    netperd11 = models.DecimalField(db_column='NETPERD11', max_digits=19,
                                    decimal_places=3)  # Field name made lowercase.
    netperd12 = models.DecimalField(db_column='NETPERD12', max_digits=19,
                                    decimal_places=3)  # Field name made lowercase.
    netperd13 = models.DecimalField(db_column='NETPERD13', max_digits=19,
                                    decimal_places=3)  # Field name made lowercase.
    netperd14 = models.DecimalField(db_column='NETPERD14', max_digits=19,
                                    decimal_places=3)  # Field name made lowercase.
    netperd15 = models.DecimalField(db_column='NETPERD15', max_digits=19,
                                    decimal_places=3)  # Field name made lowercase.
    activitysw = models.SmallIntegerField(db_column='ACTIVITYSW')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GLAFS'
        db_tablespace = 'sql_server'
        unique_together = (('acctid', 'fscsyr', 'fscsdsg', 'fscscurn', 'curntype'),)

    def get_netper_sum(self):
        # Sum up the values from netperd1 to netperd12
        netper_sum = sum(getattr(self, f'netperd{i}', Decimal(0)) for i in range(1, 13))
        return netper_sum


class Glamf(models.Model):
    acctid = models.CharField(db_column='ACCTID', primary_key=True, max_length=45,
                              db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    audtdate = models.DecimalField(db_column='AUDTDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    audttime = models.DecimalField(db_column='AUDTTIME', max_digits=9, decimal_places=0)  # Field name made lowercase.
    audtuser = models.CharField(db_column='AUDTUSER', max_length=8,
                                db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    audtorg = models.CharField(db_column='AUDTORG', max_length=6,
                               db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    createdate = models.DecimalField(db_column='CREATEDATE', max_digits=9,
                                     decimal_places=0)  # Field name made lowercase.
    acctdesc = models.CharField(db_column='ACCTDESC', max_length=60,
                                db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    accttype = models.CharField(db_column='ACCTTYPE', max_length=1,
                                db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    acctbal = models.CharField(db_column='ACCTBAL', max_length=1,
                               db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    activesw = models.SmallIntegerField(db_column='ACTIVESW')  # Field name made lowercase.
    consldsw = models.SmallIntegerField(db_column='CONSLDSW')  # Field name made lowercase.
    qtysw = models.SmallIntegerField(db_column='QTYSW')  # Field name made lowercase.
    uom = models.CharField(db_column='UOM', max_length=6,
                           db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    allocsw = models.SmallIntegerField(db_column='ALLOCSW')  # Field name made lowercase.
    acctofset = models.CharField(db_column='ACCTOFSET', max_length=45,
                                 db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    acctsrty = models.CharField(db_column='ACCTSRTY', max_length=2,
                                db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    mcsw = models.SmallIntegerField(db_column='MCSW')  # Field name made lowercase.
    specsw = models.SmallIntegerField(db_column='SPECSW')  # Field name made lowercase.
    acctgrpcod = models.CharField(db_column='ACCTGRPCOD', max_length=12,
                                  db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    ctrlacctsw = models.SmallIntegerField(db_column='CTRLACCTSW')  # Field name made lowercase.
    srceldgid = models.CharField(db_column='SRCELDGID', max_length=2,
                                 db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    alloctot = models.DecimalField(db_column='ALLOCTOT', max_digits=15, decimal_places=7)  # Field name made lowercase.
    abrkid = models.CharField(db_column='ABRKID', max_length=6,
                              db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    yracctclos = models.DecimalField(db_column='YRACCTCLOS', max_digits=7,
                                     decimal_places=0)  # Field name made lowercase.
    acctfmttd = models.CharField(db_column='ACCTFMTTD', max_length=45,
                                 db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    acsegval01 = models.CharField(db_column='ACSEGVAL01', max_length=15,
                                  db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    acsegval02 = models.CharField(db_column='ACSEGVAL02', max_length=15,
                                  db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    acsegval03 = models.CharField(db_column='ACSEGVAL03', max_length=15,
                                  db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    acsegval04 = models.CharField(db_column='ACSEGVAL04', max_length=15,
                                  db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    acsegval05 = models.CharField(db_column='ACSEGVAL05', max_length=15,
                                  db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    acsegval06 = models.CharField(db_column='ACSEGVAL06', max_length=15,
                                  db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    acsegval07 = models.CharField(db_column='ACSEGVAL07', max_length=15,
                                  db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    acsegval08 = models.CharField(db_column='ACSEGVAL08', max_length=15,
                                  db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    acsegval09 = models.CharField(db_column='ACSEGVAL09', max_length=15,
                                  db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    acsegval10 = models.CharField(db_column='ACSEGVAL10', max_length=15,
                                  db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    acctsegval = models.CharField(db_column='ACCTSEGVAL', max_length=15,
                                  db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    acctgrpscd = models.CharField(db_column='ACCTGRPSCD', max_length=12,
                                  db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    postosegid = models.CharField(db_column='POSTOSEGID', max_length=6,
                                  db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    defcurncod = models.CharField(db_column='DEFCURNCOD', max_length=3,
                                  db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    ovalues = models.IntegerField(db_column='OVALUES')  # Field name made lowercase.
    tovalues = models.IntegerField(db_column='TOVALUES')  # Field name made lowercase.
    rollupsw = models.SmallIntegerField(db_column='ROLLUPSW')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GLAMF'
        db_tablespace = 'sql_server'


class Enrqnl(models.Model):
    rqnhseq = models.DecimalField(db_column='RQNHSEQ', primary_key=True, max_digits=19, decimal_places=0)  # Field name made lowercase. The composite primary key (RQNHSEQ, RQNLREV) found, that is not supported. The first column is selected.
    rqnlrev = models.DecimalField(db_column='RQNLREV', max_digits=19, decimal_places=0)  # Field name made lowercase.
    audtdate = models.DecimalField(db_column='AUDTDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    audttime = models.DecimalField(db_column='AUDTTIME', max_digits=9, decimal_places=0)  # Field name made lowercase.
    audtuser = models.CharField(db_column='AUDTUSER', max_length=8)  # Field name made lowercase.
    audtorg = models.CharField(db_column='AUDTORG', max_length=6)  # Field name made lowercase.
    rqncseq = models.DecimalField(db_column='RQNCSEQ', max_digits=19, decimal_places=0)  # Field name made lowercase.
    oeonumber = models.CharField(db_column='OEONUMBER', max_length=22)  # Field name made lowercase.
    vdexists = models.SmallIntegerField(db_column='VDEXISTS')  # Field name made lowercase.
    vdcode = models.CharField(db_column='VDCODE', max_length=12)  # Field name made lowercase.
    vdname = models.CharField(db_column='VDNAME', max_length=60)  # Field name made lowercase.
    itemexists = models.SmallIntegerField(db_column='ITEMEXISTS')  # Field name made lowercase.
    itemno = models.CharField(db_column='ITEMNO', max_length=24)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=6)  # Field name made lowercase.
    itemdesc = models.CharField(db_column='ITEMDESC', max_length=60)  # Field name made lowercase.
    exparrival = models.DecimalField(db_column='EXPARRIVAL', max_digits=9, decimal_places=0)  # Field name made lowercase.
    venditemno = models.CharField(db_column='VENDITEMNO', max_length=24)  # Field name made lowercase.
    hascomment = models.SmallIntegerField(db_column='HASCOMMENT')  # Field name made lowercase.
    orderunit = models.CharField(db_column='ORDERUNIT', max_length=10)  # Field name made lowercase.
    orderconv = models.DecimalField(db_column='ORDERCONV', max_digits=19, decimal_places=6)  # Field name made lowercase.
    orderdecml = models.SmallIntegerField(db_column='ORDERDECML')  # Field name made lowercase.
    stockdecml = models.SmallIntegerField(db_column='STOCKDECML')  # Field name made lowercase.
    oqordered = models.DecimalField(db_column='OQORDERED', max_digits=19, decimal_places=4)  # Field name made lowercase.
    stockitem = models.SmallIntegerField(db_column='STOCKITEM')  # Field name made lowercase.
    manitemno = models.CharField(db_column='MANITEMNO', max_length=24)  # Field name made lowercase.
    values = models.IntegerField(db_column='VALUES')  # Field name made lowercase.
    contract = models.CharField(db_column='CONTRACT', max_length=16)  # Field name made lowercase.
    project = models.CharField(db_column='PROJECT', max_length=16)  # Field name made lowercase.
    ccategory = models.CharField(db_column='CCATEGORY', max_length=16)  # Field name made lowercase.
    costclass = models.SmallIntegerField(db_column='COSTCLASS')  # Field name made lowercase.
    unitcost = models.DecimalField(db_column='UNITCOST', max_digits=19, decimal_places=6)  # Field name made lowercase.
    cpcosttopo = models.SmallIntegerField(db_column='CPCOSTTOPO')  # Field name made lowercase.
    ucismanual = models.SmallIntegerField(db_column='UCISMANUAL')  # Field name made lowercase.
    extended = models.DecimalField(db_column='EXTENDED', max_digits=19, decimal_places=3)  # Field name made lowercase.
    fcextended = models.DecimalField(db_column='FCEXTENDED', max_digits=19, decimal_places=3)  # Field name made lowercase.
    unitweight = models.DecimalField(db_column='UNITWEIGHT', max_digits=19, decimal_places=4)  # Field name made lowercase.
    extweight = models.DecimalField(db_column='EXTWEIGHT', max_digits=19, decimal_places=4)  # Field name made lowercase.
    weightunit = models.CharField(db_column='WEIGHTUNIT', max_length=10)  # Field name made lowercase.
    weightconv = models.DecimalField(db_column='WEIGHTCONV', max_digits=19, decimal_places=6)  # Field name made lowercase.
    defuweight = models.DecimalField(db_column='DEFUWEIGHT', max_digits=19, decimal_places=4)  # Field name made lowercase.
    defextwght = models.DecimalField(db_column='DEFEXTWGHT', max_digits=19, decimal_places=4)  # Field name made lowercase.
    detailnum = models.SmallIntegerField(db_column='DETAILNUM')  # Field name made lowercase.
    pid = models.CharField(db_column='PID', max_length=36)  # Field name made lowercase.
    tid = models.DecimalField(db_column='TID', max_digits=19, decimal_places=0)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='STATUS')  # Field name made lowercase.
    appraction = models.CharField(db_column='APPRACTION', max_length=255)  # Field name made lowercase.
    currency = models.CharField(db_column='CURRENCY', max_length=3)  # Field name made lowercase.
    rate = models.DecimalField(db_column='RATE', max_digits=15, decimal_places=7)  # Field name made lowercase.
    rateexists = models.SmallIntegerField(db_column='RATEEXISTS')  # Field name made lowercase.
    ratetype = models.CharField(db_column='RATETYPE', max_length=2)  # Field name made lowercase.
    ratedate = models.DecimalField(db_column='RATEDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    rateoper = models.SmallIntegerField(db_column='RATEOPER')  # Field name made lowercase.
    qtcnt = models.IntegerField(db_column='QTCNT')  # Field name made lowercase.
    codedivis = models.CharField(db_column='CODEDIVIS', max_length=12)  # Field name made lowercase.
    codereg = models.CharField(db_column='CODEREG', max_length=12)  # Field name made lowercase.
    codedep = models.CharField(db_column='CODEDEP', max_length=12)  # Field name made lowercase.
    codecst = models.CharField(db_column='CODECST', max_length=12)  # Field name made lowercase.
    codejob = models.CharField(db_column='CODEJOB', max_length=16)  # Field name made lowercase.
    bgcode = models.CharField(db_column='BGCODE', max_length=45)  # Field name made lowercase.
    employeid = models.CharField(db_column='EMPLOYEID', max_length=16)  # Field name made lowercase.
    year = models.CharField(db_column='YEAR', max_length=4)  # Field name made lowercase.
    period = models.SmallIntegerField(db_column='PERIOD')  # Field name made lowercase.
    apprcnt = models.IntegerField(db_column='APPRCNT')  # Field name made lowercase.
    rejectcnt = models.IntegerField(db_column='REJECTCNT')  # Field name made lowercase.
    passcnt = models.IntegerField(db_column='PASSCNT')  # Field name made lowercase.
    swoverbgt = models.SmallIntegerField(db_column='SWOVERBGT')  # Field name made lowercase.
    usewfcode = models.CharField(db_column='USEWFCODE', max_length=12)  # Field name made lowercase.
    rqnnumber = models.CharField(db_column='RQNNUMBER', max_length=22)  # Field name made lowercase.
    wfver = models.IntegerField(db_column='WFVER')  # Field name made lowercase.
    porhseq = models.DecimalField(db_column='PORHSEQ', max_digits=19, decimal_places=0)  # Field name made lowercase.
    ponumber = models.CharField(db_column='PONUMBER', max_length=22)  # Field name made lowercase.
    fileid = models.CharField(db_column='FILEID', max_length=36)  # Field name made lowercase.
    docname = models.CharField(db_column='DOCNAME', max_length=255)  # Field name made lowercase.
    weblink = models.CharField(db_column='WEBLINK', max_length=255)  # Field name made lowercase.
    weblink2 = models.CharField(db_column='WEBLINK2', max_length=255)  # Field name made lowercase.
    weblink3 = models.CharField(db_column='WEBLINK3', max_length=255)  # Field name made lowercase.
    weblink4 = models.CharField(db_column='WEBLINK4', max_length=255)  # Field name made lowercase.
    linekey = models.CharField(db_column='LINEKEY', max_length=36)  # Field name made lowercase.
    glacct = models.CharField(db_column='GLACCT', max_length=45)  # Field name made lowercase.
    fmtglacct = models.CharField(db_column='FMTGLACCT', max_length=45)  # Field name made lowercase.
    termcode = models.CharField(db_column='TERMCODE', max_length=6)  # Field name made lowercase.
    fmtitem = models.CharField(db_column='FMTITEM', max_length=24)  # Field name made lowercase.
    fmtcontno = models.CharField(db_column='FMTCONTNO', max_length=16)  # Field name made lowercase.
    ismodified = models.SmallIntegerField(db_column='ISMODIFIED')  # Field name made lowercase.
    rejectrole = models.CharField(db_column='REJECTROLE', max_length=36)  # Field name made lowercase.
    taxgroup = models.CharField(db_column='TAXGROUP', max_length=12)  # Field name made lowercase.
    taxauth1 = models.CharField(db_column='TAXAUTH1', max_length=12)  # Field name made lowercase.
    taxauth2 = models.CharField(db_column='TAXAUTH2', max_length=12)  # Field name made lowercase.
    taxauth3 = models.CharField(db_column='TAXAUTH3', max_length=12)  # Field name made lowercase.
    taxauth4 = models.CharField(db_column='TAXAUTH4', max_length=12)  # Field name made lowercase.
    taxauth5 = models.CharField(db_column='TAXAUTH5', max_length=12)  # Field name made lowercase.
    htaxclass1 = models.SmallIntegerField(db_column='HTAXCLASS1')  # Field name made lowercase.
    htaxclass2 = models.SmallIntegerField(db_column='HTAXCLASS2')  # Field name made lowercase.
    htaxclass3 = models.SmallIntegerField(db_column='HTAXCLASS3')  # Field name made lowercase.
    htaxclass4 = models.SmallIntegerField(db_column='HTAXCLASS4')  # Field name made lowercase.
    htaxclass5 = models.SmallIntegerField(db_column='HTAXCLASS5')  # Field name made lowercase.
    taxbase1 = models.DecimalField(db_column='TAXBASE1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxbase2 = models.DecimalField(db_column='TAXBASE2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxbase3 = models.DecimalField(db_column='TAXBASE3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxbase4 = models.DecimalField(db_column='TAXBASE4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxbase5 = models.DecimalField(db_column='TAXBASE5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxclass1 = models.SmallIntegerField(db_column='TAXCLASS1')  # Field name made lowercase.
    taxclass2 = models.SmallIntegerField(db_column='TAXCLASS2')  # Field name made lowercase.
    taxclass3 = models.SmallIntegerField(db_column='TAXCLASS3')  # Field name made lowercase.
    taxclass4 = models.SmallIntegerField(db_column='TAXCLASS4')  # Field name made lowercase.
    taxclass5 = models.SmallIntegerField(db_column='TAXCLASS5')  # Field name made lowercase.
    taxrate1 = models.DecimalField(db_column='TAXRATE1', max_digits=15, decimal_places=5)  # Field name made lowercase.
    taxrate2 = models.DecimalField(db_column='TAXRATE2', max_digits=15, decimal_places=5)  # Field name made lowercase.
    taxrate3 = models.DecimalField(db_column='TAXRATE3', max_digits=15, decimal_places=5)  # Field name made lowercase.
    taxrate4 = models.DecimalField(db_column='TAXRATE4', max_digits=15, decimal_places=5)  # Field name made lowercase.
    taxrate5 = models.DecimalField(db_column='TAXRATE5', max_digits=15, decimal_places=5)  # Field name made lowercase.
    taxinclud1 = models.SmallIntegerField(db_column='TAXINCLUD1')  # Field name made lowercase.
    taxinclud2 = models.SmallIntegerField(db_column='TAXINCLUD2')  # Field name made lowercase.
    taxinclud3 = models.SmallIntegerField(db_column='TAXINCLUD3')  # Field name made lowercase.
    taxinclud4 = models.SmallIntegerField(db_column='TAXINCLUD4')  # Field name made lowercase.
    taxinclud5 = models.SmallIntegerField(db_column='TAXINCLUD5')  # Field name made lowercase.
    txinclude1 = models.DecimalField(db_column='TXINCLUDE1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txinclude2 = models.DecimalField(db_column='TXINCLUDE2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txinclude3 = models.DecimalField(db_column='TXINCLUDE3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txinclude4 = models.DecimalField(db_column='TXINCLUDE4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txinclude5 = models.DecimalField(db_column='TXINCLUDE5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexclude1 = models.DecimalField(db_column='TXEXCLUDE1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexclude2 = models.DecimalField(db_column='TXEXCLUDE2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexclude3 = models.DecimalField(db_column='TXEXCLUDE3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexclude4 = models.DecimalField(db_column='TXEXCLUDE4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexclude5 = models.DecimalField(db_column='TXEXCLUDE5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxamount1 = models.DecimalField(db_column='TAXAMOUNT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxamount2 = models.DecimalField(db_column='TAXAMOUNT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxamount3 = models.DecimalField(db_column='TAXAMOUNT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxamount4 = models.DecimalField(db_column='TAXAMOUNT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxamount5 = models.DecimalField(db_column='TAXAMOUNT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecvamt1 = models.DecimalField(db_column='TXRECVAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecvamt2 = models.DecimalField(db_column='TXRECVAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecvamt3 = models.DecimalField(db_column='TXRECVAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecvamt4 = models.DecimalField(db_column='TXRECVAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecvamt5 = models.DecimalField(db_column='TXRECVAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexpsamt1 = models.DecimalField(db_column='TXEXPSAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexpsamt2 = models.DecimalField(db_column='TXEXPSAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexpsamt3 = models.DecimalField(db_column='TXEXPSAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexpsamt4 = models.DecimalField(db_column='TXEXPSAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexpsamt5 = models.DecimalField(db_column='TXEXPSAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txalloamt1 = models.DecimalField(db_column='TXALLOAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txalloamt2 = models.DecimalField(db_column='TXALLOAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txalloamt3 = models.DecimalField(db_column='TXALLOAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txalloamt4 = models.DecimalField(db_column='TXALLOAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txalloamt5 = models.DecimalField(db_column='TXALLOAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbaseallo = models.DecimalField(db_column='TXBASEALLO', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txincluded = models.DecimalField(db_column='TXINCLUDED', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexcluded = models.DecimalField(db_column='TXEXCLUDED', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxamount = models.DecimalField(db_column='TAXAMOUNT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecvamt = models.DecimalField(db_column='TXRECVAMT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexpsamt = models.DecimalField(db_column='TXEXPSAMT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txalloamt = models.DecimalField(db_column='TXALLOAMT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    disamt = models.DecimalField(db_column='DISAMT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    linetot = models.DecimalField(db_column='LINETOT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfbaseallo = models.DecimalField(db_column='TFBASEALLO', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfamount1 = models.DecimalField(db_column='TFAMOUNT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfamount2 = models.DecimalField(db_column='TFAMOUNT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfamount3 = models.DecimalField(db_column='TFAMOUNT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfamount4 = models.DecimalField(db_column='TFAMOUNT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfamount5 = models.DecimalField(db_column='TFAMOUNT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfalloamt1 = models.DecimalField(db_column='TFALLOAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfalloamt2 = models.DecimalField(db_column='TFALLOAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfalloamt3 = models.DecimalField(db_column='TFALLOAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfalloamt4 = models.DecimalField(db_column='TFALLOAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfalloamt5 = models.DecimalField(db_column='TFALLOAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfrecvamt1 = models.DecimalField(db_column='TFRECVAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfrecvamt2 = models.DecimalField(db_column='TFRECVAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfrecvamt3 = models.DecimalField(db_column='TFRECVAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfrecvamt4 = models.DecimalField(db_column='TFRECVAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfrecvamt5 = models.DecimalField(db_column='TFRECVAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfexpsamt1 = models.DecimalField(db_column='TFEXPSAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfexpsamt2 = models.DecimalField(db_column='TFEXPSAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfexpsamt3 = models.DecimalField(db_column='TFEXPSAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfexpsamt4 = models.DecimalField(db_column='TFEXPSAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfexpsamt5 = models.DecimalField(db_column='TFEXPSAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    fdisamt = models.DecimalField(db_column='FDISAMT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    flinetot = models.DecimalField(db_column='FLINETOT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    appvdate = models.DecimalField(db_column='APPVDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    porlseq = models.DecimalField(db_column='PORLSEQ', max_digits=19, decimal_places=0)  # Field name made lowercase.
    porcseq = models.DecimalField(db_column='PORCSEQ', max_digits=19, decimal_places=0)  # Field name made lowercase.
    oqreceived = models.DecimalField(db_column='OQRECEIVED', max_digits=19, decimal_places=4)  # Field name made lowercase.
    oqcanceled = models.DecimalField(db_column='OQCANCELED', max_digits=19, decimal_places=4)  # Field name made lowercase.
    extreceive = models.DecimalField(db_column='EXTRECEIVE', max_digits=19, decimal_places=3)  # Field name made lowercase.
    extcancel = models.DecimalField(db_column='EXTCANCEL', max_digits=19, decimal_places=3)  # Field name made lowercase.
    srreceived = models.DecimalField(db_column='SRRECEIVED', max_digits=19, decimal_places=3)  # Field name made lowercase.
    fcreceived = models.DecimalField(db_column='FCRECEIVED', max_digits=19, decimal_places=3)  # Field name made lowercase.
    iscomplete = models.SmallIntegerField(db_column='ISCOMPLETE')  # Field name made lowercase.
    discpct = models.DecimalField(db_column='DISCPCT', max_digits=9, decimal_places=5)  # Field name made lowercase.
    discount = models.DecimalField(db_column='DISCOUNT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    discountf = models.DecimalField(db_column='DISCOUNTF', max_digits=19, decimal_places=3)  # Field name made lowercase.
    disext = models.DecimalField(db_column='DISEXT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    orqnhseq = models.DecimalField(db_column='ORQNHSEQ', max_digits=19, decimal_places=0)  # Field name made lowercase.
    orqnlseq = models.DecimalField(db_column='ORQNLSEQ', max_digits=19, decimal_places=0)  # Field name made lowercase.
    olinekey = models.CharField(db_column='OLINEKEY', max_length=36)  # Field name made lowercase.
    orqnnumber = models.CharField(db_column='ORQNNUMBER', max_length=22)  # Field name made lowercase.
    toporlseq = models.DecimalField(db_column='TOPORLSEQ', max_digits=19, decimal_places=0)  # Field name made lowercase.
    oqrcpextra = models.DecimalField(db_column='OQRCPEXTRA', max_digits=19, decimal_places=4)  # Field name made lowercase.
    oqoutstand = models.DecimalField(db_column='OQOUTSTAND', max_digits=19, decimal_places=4)  # Field name made lowercase.
    oiscomplet = models.SmallIntegerField(db_column='OISCOMPLET')  # Field name made lowercase.
    tids = models.CharField(db_column='TIDS', max_length=255)  # Field name made lowercase.
    hasdropshi = models.SmallIntegerField(db_column='HASDROPSHI')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ENRQNL'
        unique_together = (('rqnhseq', 'rqnlrev'), ('rqnhseq', 'vdcode', 'rqnlrev'),)


class Enebd(models.Model):
    cntbtch = models.IntegerField(db_column='CNTBTCH', primary_key=True)  # Field name made lowercase. The composite primary key (CNTBTCH, CNTITEM, CNTLINE) found, that is not supported. The first column is selected.
    cntitem = models.IntegerField(db_column='CNTITEM')  # Field name made lowercase.
    cntline = models.IntegerField(db_column='CNTLINE')  # Field name made lowercase.
    audtdate = models.DecimalField(db_column='AUDTDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    audttime = models.DecimalField(db_column='AUDTTIME', max_digits=9, decimal_places=0)  # Field name made lowercase.
    audtuser = models.CharField(db_column='AUDTUSER', max_length=8)  # Field name made lowercase.
    audtorg = models.CharField(db_column='AUDTORG', max_length=6)  # Field name made lowercase.
    fsyear = models.CharField(db_column='FSYEAR', max_length=4)  # Field name made lowercase.
    itemcode = models.CharField(db_column='ITEMCODE', max_length=12)  # Field name made lowercase.
    textdesc = models.CharField(db_column='TEXTDESC', max_length=60)  # Field name made lowercase.
    idglacct = models.CharField(db_column='IDGLACCT', max_length=45)  # Field name made lowercase.
    amtlineh = models.DecimalField(db_column='AMTLINEH', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amtlinet = models.DecimalField(db_column='AMTLINET', max_digits=19, decimal_places=3)  # Field name made lowercase.
    codedivis = models.CharField(db_column='CODEDIVIS', max_length=12)  # Field name made lowercase.
    codereg = models.CharField(db_column='CODEREG', max_length=12)  # Field name made lowercase.
    codedep = models.CharField(db_column='CODEDEP', max_length=12)  # Field name made lowercase.
    codecst = models.CharField(db_column='CODECST', max_length=12)  # Field name made lowercase.
    codejob = models.CharField(db_column='CODEJOB', max_length=16)  # Field name made lowercase.
    comment = models.CharField(db_column='COMMENT', max_length=250)  # Field name made lowercase.
    amttottax = models.DecimalField(db_column='AMTTOTTAX', max_digits=19, decimal_places=3)  # Field name made lowercase.
    swmanltx = models.SmallIntegerField(db_column='SWMANLTX')  # Field name made lowercase.
    basetax1 = models.DecimalField(db_column='BASETAX1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    basetax2 = models.DecimalField(db_column='BASETAX2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    basetax3 = models.DecimalField(db_column='BASETAX3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    basetax4 = models.DecimalField(db_column='BASETAX4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    basetax5 = models.DecimalField(db_column='BASETAX5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxclass1 = models.SmallIntegerField(db_column='TAXCLASS1')  # Field name made lowercase.
    taxclass2 = models.SmallIntegerField(db_column='TAXCLASS2')  # Field name made lowercase.
    taxclass3 = models.SmallIntegerField(db_column='TAXCLASS3')  # Field name made lowercase.
    taxclass4 = models.SmallIntegerField(db_column='TAXCLASS4')  # Field name made lowercase.
    taxclass5 = models.SmallIntegerField(db_column='TAXCLASS5')  # Field name made lowercase.
    swtaxincl1 = models.SmallIntegerField(db_column='SWTAXINCL1')  # Field name made lowercase.
    swtaxincl2 = models.SmallIntegerField(db_column='SWTAXINCL2')  # Field name made lowercase.
    swtaxincl3 = models.SmallIntegerField(db_column='SWTAXINCL3')  # Field name made lowercase.
    swtaxincl4 = models.SmallIntegerField(db_column='SWTAXINCL4')  # Field name made lowercase.
    swtaxincl5 = models.SmallIntegerField(db_column='SWTAXINCL5')  # Field name made lowercase.
    ratetax1 = models.DecimalField(db_column='RATETAX1', max_digits=15, decimal_places=5)  # Field name made lowercase.
    ratetax2 = models.DecimalField(db_column='RATETAX2', max_digits=15, decimal_places=5)  # Field name made lowercase.
    ratetax3 = models.DecimalField(db_column='RATETAX3', max_digits=15, decimal_places=5)  # Field name made lowercase.
    ratetax4 = models.DecimalField(db_column='RATETAX4', max_digits=15, decimal_places=5)  # Field name made lowercase.
    ratetax5 = models.DecimalField(db_column='RATETAX5', max_digits=15, decimal_places=5)  # Field name made lowercase.
    amttax1 = models.DecimalField(db_column='AMTTAX1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amttax2 = models.DecimalField(db_column='AMTTAX2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amttax3 = models.DecimalField(db_column='AMTTAX3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amttax4 = models.DecimalField(db_column='AMTTAX4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amttax5 = models.DecimalField(db_column='AMTTAX5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amttaxrec1 = models.DecimalField(db_column='AMTTAXREC1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amttaxrec2 = models.DecimalField(db_column='AMTTAXREC2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amttaxrec3 = models.DecimalField(db_column='AMTTAXREC3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amttaxrec4 = models.DecimalField(db_column='AMTTAXREC4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amttaxrec5 = models.DecimalField(db_column='AMTTAXREC5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amttaxexp1 = models.DecimalField(db_column='AMTTAXEXP1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amttaxexp2 = models.DecimalField(db_column='AMTTAXEXP2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amttaxexp3 = models.DecimalField(db_column='AMTTAXEXP3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amttaxexp4 = models.DecimalField(db_column='AMTTAXEXP4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amttaxexp5 = models.DecimalField(db_column='AMTTAXEXP5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    disamt = models.DecimalField(db_column='DISAMT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexpamt = models.DecimalField(db_column='TXEXPAMT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    contract = models.CharField(db_column='CONTRACT', max_length=16)  # Field name made lowercase.
    project = models.CharField(db_column='PROJECT', max_length=16)  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=16)  # Field name made lowercase.
    resource = models.CharField(db_column='RESOURCE', max_length=24)  # Field name made lowercase.
    values = models.IntegerField(db_column='VALUES')  # Field name made lowercase.
    processcmd = models.SmallIntegerField(db_column='PROCESSCMD')  # Field name made lowercase.
    descomp = models.CharField(db_column='DESCOMP', max_length=6)  # Field name made lowercase.
    txbs1tc = models.DecimalField(db_column='TXBS1TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbs2tc = models.DecimalField(db_column='TXBS2TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbs3tc = models.DecimalField(db_column='TXBS3TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbs4tc = models.DecimalField(db_column='TXBS4TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbs5tc = models.DecimalField(db_column='TXBS5TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt1tc = models.DecimalField(db_column='TXAMT1TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt2tc = models.DecimalField(db_column='TXAMT2TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt3tc = models.DecimalField(db_column='TXAMT3TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt4tc = models.DecimalField(db_column='TXAMT4TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt5tc = models.DecimalField(db_column='TXAMT5TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txtotrc = models.DecimalField(db_column='TXTOTRC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txallrc = models.DecimalField(db_column='TXALLRC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexp1rc = models.DecimalField(db_column='TXEXP1RC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexp2rc = models.DecimalField(db_column='TXEXP2RC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexp3rc = models.DecimalField(db_column='TXEXP3RC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexp4rc = models.DecimalField(db_column='TXEXP4RC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexp5rc = models.DecimalField(db_column='TXEXP5RC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrec1rc = models.DecimalField(db_column='TXREC1RC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrec2rc = models.DecimalField(db_column='TXREC2RC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrec3rc = models.DecimalField(db_column='TXREC3RC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrec4rc = models.DecimalField(db_column='TXREC4RC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrec5rc = models.DecimalField(db_column='TXREC5RC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    codecurnrc = models.CharField(db_column='CODECURNRC', max_length=3)  # Field name made lowercase.
    txall1tc = models.DecimalField(db_column='TXALL1TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txall2tc = models.DecimalField(db_column='TXALL2TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txall3tc = models.DecimalField(db_column='TXALL3TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txall4tc = models.DecimalField(db_column='TXALL4TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txall5tc = models.DecimalField(db_column='TXALL5TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    sourcurr = models.CharField(db_column='SOURCURR', max_length=3)  # Field name made lowercase.
    ratetype = models.CharField(db_column='RATETYPE', max_length=2)  # Field name made lowercase.
    exchratehc = models.DecimalField(db_column='EXCHRATEHC', max_digits=15, decimal_places=7)  # Field name made lowercase.
    ratedate = models.DecimalField(db_column='RATEDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    reimcurr = models.CharField(db_column='REIMCURR', max_length=3)  # Field name made lowercase.
    rmratetype = models.CharField(db_column='RMRATETYPE', max_length=2)  # Field name made lowercase.
    rmratedate = models.DecimalField(db_column='RMRATEDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    exchraterm = models.DecimalField(db_column='EXCHRATERM', max_digits=15, decimal_places=7)  # Field name made lowercase.
    amtexprm = models.DecimalField(db_column='AMTEXPRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    billtype = models.SmallIntegerField(db_column='BILLTYPE')  # Field name made lowercase.
    unitcost = models.DecimalField(db_column='UNITCOST', max_digits=19, decimal_places=6)  # Field name made lowercase.
    quantity = models.DecimalField(db_column='QUANTITY', max_digits=19, decimal_places=2)  # Field name made lowercase.
    raterc = models.DecimalField(db_column='RATERC', max_digits=15, decimal_places=7)  # Field name made lowercase.
    ratedaterc = models.DecimalField(db_column='RATEDATERC', max_digits=9, decimal_places=0)  # Field name made lowercase.
    ratetyperc = models.CharField(db_column='RATETYPERC', max_length=2)  # Field name made lowercase.
    spreadrc = models.DecimalField(db_column='SPREADRC', max_digits=15, decimal_places=7)  # Field name made lowercase.
    datematcrc = models.SmallIntegerField(db_column='DATEMATCRC')  # Field name made lowercase.
    rateoperrc = models.SmallIntegerField(db_column='RATEOPERRC')  # Field name made lowercase.
    swraterc = models.SmallIntegerField(db_column='SWRATERC')  # Field name made lowercase.
    spreadhc = models.DecimalField(db_column='SPREADHC', max_digits=15, decimal_places=7)  # Field name made lowercase.
    datematchc = models.SmallIntegerField(db_column='DATEMATCHC')  # Field name made lowercase.
    rateoperhc = models.SmallIntegerField(db_column='RATEOPERHC')  # Field name made lowercase.
    spreadrm = models.DecimalField(db_column='SPREADRM', max_digits=15, decimal_places=7)  # Field name made lowercase.
    datematcrm = models.SmallIntegerField(db_column='DATEMATCRM')  # Field name made lowercase.
    rateoperrm = models.SmallIntegerField(db_column='RATEOPERRM')  # Field name made lowercase.
    txtothc = models.DecimalField(db_column='TXTOTHC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbse1hc = models.DecimalField(db_column='TXBSE1HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbse2hc = models.DecimalField(db_column='TXBSE2HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbse3hc = models.DecimalField(db_column='TXBSE3HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbse4hc = models.DecimalField(db_column='TXBSE4HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbse5hc = models.DecimalField(db_column='TXBSE5HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt1hc = models.DecimalField(db_column='TXAMT1HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt2hc = models.DecimalField(db_column='TXAMT2HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt3hc = models.DecimalField(db_column='TXAMT3HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt4hc = models.DecimalField(db_column='TXAMT4HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt5hc = models.DecimalField(db_column='TXAMT5HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrec1hc = models.DecimalField(db_column='TXREC1HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrec2hc = models.DecimalField(db_column='TXREC2HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrec3hc = models.DecimalField(db_column='TXREC3HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrec4hc = models.DecimalField(db_column='TXREC4HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrec5hc = models.DecimalField(db_column='TXREC5HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexp1hc = models.DecimalField(db_column='TXEXP1HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexp2hc = models.DecimalField(db_column='TXEXP2HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexp3hc = models.DecimalField(db_column='TXEXP3HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexp4hc = models.DecimalField(db_column='TXEXP4HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexp5hc = models.DecimalField(db_column='TXEXP5HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txall1hc = models.DecimalField(db_column='TXALL1HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txall2hc = models.DecimalField(db_column='TXALL2HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txall3hc = models.DecimalField(db_column='TXALL3HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txall4hc = models.DecimalField(db_column='TXALL4HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txall5hc = models.DecimalField(db_column='TXALL5HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txallhc = models.DecimalField(db_column='TXALLHC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txdishc = models.DecimalField(db_column='TXDISHC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amtgldishc = models.DecimalField(db_column='AMTGLDISHC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    doctothc = models.DecimalField(db_column='DOCTOTHC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txtotrm = models.DecimalField(db_column='TXTOTRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexprm = models.DecimalField(db_column='TXEXPRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecrm = models.DecimalField(db_column='TXRECRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txallrm = models.DecimalField(db_column='TXALLRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txdisrm = models.DecimalField(db_column='TXDISRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amtgldisrm = models.DecimalField(db_column='AMTGLDISRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    doctotrm = models.DecimalField(db_column='DOCTOTRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    fmtcontno = models.CharField(db_column='FMTCONTNO', max_length=16)  # Field name made lowercase.
    expdate = models.DecimalField(db_column='EXPDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=10)  # Field name made lowercase.
    aritem = models.CharField(db_column='ARITEM', max_length=16)  # Field name made lowercase.
    customer = models.CharField(db_column='CUSTOMER', max_length=12)  # Field name made lowercase.
    phase = models.CharField(db_column='PHASE', max_length=16)  # Field name made lowercase.
    wbs = models.CharField(db_column='WBS', max_length=16)  # Field name made lowercase.
    task = models.CharField(db_column='TASK', max_length=12)  # Field name made lowercase.
    pid = models.CharField(db_column='PID', max_length=36)  # Field name made lowercase.
    tid = models.DecimalField(db_column='TID', max_digits=19, decimal_places=0)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='STATUS')  # Field name made lowercase.
    role = models.CharField(db_column='ROLE', max_length=12)  # Field name made lowercase.
    billrate = models.DecimalField(db_column='BILLRATE', max_digits=19, decimal_places=6)  # Field name made lowercase.
    billamth = models.DecimalField(db_column='BILLAMTH', max_digits=19, decimal_places=3)  # Field name made lowercase.
    billamts = models.DecimalField(db_column='BILLAMTS', max_digits=19, decimal_places=3)  # Field name made lowercase.
    billcurr = models.CharField(db_column='BILLCURR', max_length=3)  # Field name made lowercase.
    bratetype = models.CharField(db_column='BRATETYPE', max_length=2)  # Field name made lowercase.
    bratedate = models.DecimalField(db_column='BRATEDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    bspread = models.DecimalField(db_column='BSPREAD', max_digits=15, decimal_places=7)  # Field name made lowercase.
    bdatematc = models.SmallIntegerField(db_column='BDATEMATC')  # Field name made lowercase.
    brateoper = models.SmallIntegerField(db_column='BRATEOPER')  # Field name made lowercase.
    brate = models.DecimalField(db_column='BRATE', max_digits=15, decimal_places=7)  # Field name made lowercase.
    appraction = models.CharField(db_column='APPRACTION', max_length=255)  # Field name made lowercase.
    swrb = models.SmallIntegerField(db_column='SWRB')  # Field name made lowercase.
    approver = models.CharField(db_column='APPROVER', max_length=16)  # Field name made lowercase.
    idexpst = models.CharField(db_column='IDEXPST', max_length=22)  # Field name made lowercase.
    reqid = models.CharField(db_column='REQID', max_length=36)  # Field name made lowercase.
    fileid = models.CharField(db_column='FILEID', max_length=36)  # Field name made lowercase.
    docname = models.CharField(db_column='DOCNAME', max_length=255)  # Field name made lowercase.
    ismodified = models.SmallIntegerField(db_column='ISMODIFIED')  # Field name made lowercase.
    rejectrole = models.CharField(db_column='REJECTROLE', max_length=36)  # Field name made lowercase.
    wfid = models.CharField(db_column='WFID', max_length=12)  # Field name made lowercase.
    wfver = models.IntegerField(db_column='WFVER')  # Field name made lowercase.
    apprcnt = models.IntegerField(db_column='APPRCNT')  # Field name made lowercase.
    rejectcnt = models.IntegerField(db_column='REJECTCNT')  # Field name made lowercase.
    passcnt = models.IntegerField(db_column='PASSCNT')  # Field name made lowercase.
    swcrcard = models.SmallIntegerField(db_column='SWCRCARD')  # Field name made lowercase.
    oamtrm = models.DecimalField(db_column='OAMTRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    otxtotrm = models.DecimalField(db_column='OTXTOTRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    otxexprm = models.DecimalField(db_column='OTXEXPRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    otxrecrm = models.DecimalField(db_column='OTXRECRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    otxallrm = models.DecimalField(db_column='OTXALLRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    otxdisrm = models.DecimalField(db_column='OTXDISRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    ogldisrm = models.DecimalField(db_column='OGLDISRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    olinetotrm = models.DecimalField(db_column='OLINETOTRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    idven = models.CharField(db_column='IDVEN', max_length=12)  # Field name made lowercase.
    invid = models.CharField(db_column='INVID', max_length=22)  # Field name made lowercase.
    invdate = models.DecimalField(db_column='INVDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    loccode = models.CharField(db_column='LOCCODE', max_length=16)  # Field name made lowercase.
    trlinekey = models.CharField(db_column='TRLINEKEY', max_length=36)  # Field name made lowercase.
    isovlimit = models.SmallIntegerField(db_column='ISOVLIMIT')  # Field name made lowercase.
    isovglbg = models.SmallIntegerField(db_column='ISOVGLBG')  # Field name made lowercase.
    isovpjcbg = models.SmallIntegerField(db_column='ISOVPJCBG')  # Field name made lowercase.
    tids = models.CharField(db_column='TIDS', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ENEBD'
        unique_together = (('cntbtch', 'cntitem', 'cntline'),)


class Poporl(models.Model):
    porhseq = models.DecimalField(db_column='PORHSEQ', primary_key=True, max_digits=19, decimal_places=0)  # Field name made lowercase. The composite primary key (PORHSEQ, PORLREV) found, that is not supported. The first column is selected.
    porlrev = models.DecimalField(db_column='PORLREV', max_digits=19, decimal_places=0)  # Field name made lowercase.
    audtdate = models.DecimalField(db_column='AUDTDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    audttime = models.DecimalField(db_column='AUDTTIME', max_digits=9, decimal_places=0)  # Field name made lowercase.
    audtuser = models.CharField(db_column='AUDTUSER', max_length=8)  # Field name made lowercase.
    audtorg = models.CharField(db_column='AUDTORG', max_length=6)  # Field name made lowercase.
    porlseq = models.DecimalField(db_column='PORLSEQ', max_digits=19, decimal_places=0)  # Field name made lowercase.
    porcseq = models.DecimalField(db_column='PORCSEQ', max_digits=19, decimal_places=0)  # Field name made lowercase.
    indbtable = models.SmallIntegerField(db_column='INDBTABLE')  # Field name made lowercase.
    consolseq = models.DecimalField(db_column='CONSOLSEQ', max_digits=19, decimal_places=0)  # Field name made lowercase.
    rqnhseq = models.DecimalField(db_column='RQNHSEQ', max_digits=19, decimal_places=0)  # Field name made lowercase.
    rqnlseq = models.DecimalField(db_column='RQNLSEQ', max_digits=19, decimal_places=0)  # Field name made lowercase.
    oeonumber = models.CharField(db_column='OEONUMBER', max_length=22)  # Field name made lowercase.
    postedtoic = models.SmallIntegerField(db_column='POSTEDTOIC')  # Field name made lowercase.
    toposttoic = models.SmallIntegerField(db_column='TOPOSTTOIC')  # Field name made lowercase.
    stprint = models.SmallIntegerField(db_column='STPRINT')  # Field name made lowercase.
    completion = models.SmallIntegerField(db_column='COMPLETION')  # Field name made lowercase.
    dtcomplete = models.DecimalField(db_column='DTCOMPLETE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    itemexists = models.SmallIntegerField(db_column='ITEMEXISTS')  # Field name made lowercase.
    itemno = models.CharField(db_column='ITEMNO', max_length=24)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=6)  # Field name made lowercase.
    itemdesc = models.CharField(db_column='ITEMDESC', max_length=60)  # Field name made lowercase.
    exparrival = models.DecimalField(db_column='EXPARRIVAL', max_digits=9, decimal_places=0)  # Field name made lowercase.
    venditemno = models.CharField(db_column='VENDITEMNO', max_length=24)  # Field name made lowercase.
    hascomment = models.SmallIntegerField(db_column='HASCOMMENT')  # Field name made lowercase.
    orderunit = models.CharField(db_column='ORDERUNIT', max_length=10)  # Field name made lowercase.
    orderconv = models.DecimalField(db_column='ORDERCONV', max_digits=19, decimal_places=6)  # Field name made lowercase.
    orderdecml = models.SmallIntegerField(db_column='ORDERDECML')  # Field name made lowercase.
    stockdecml = models.SmallIntegerField(db_column='STOCKDECML')  # Field name made lowercase.
    oqordered = models.DecimalField(db_column='OQORDERED', max_digits=19, decimal_places=4)  # Field name made lowercase.
    oqreceived = models.DecimalField(db_column='OQRECEIVED', max_digits=19, decimal_places=4)  # Field name made lowercase.
    oqcanceled = models.DecimalField(db_column='OQCANCELED', max_digits=19, decimal_places=4)  # Field name made lowercase.
    oqrcpextra = models.DecimalField(db_column='OQRCPEXTRA', max_digits=19, decimal_places=4)  # Field name made lowercase.
    oqoutstand = models.DecimalField(db_column='OQOUTSTAND', max_digits=19, decimal_places=4)  # Field name made lowercase.
    sqordered = models.DecimalField(db_column='SQORDERED', max_digits=19, decimal_places=4)  # Field name made lowercase.
    sqreceived = models.DecimalField(db_column='SQRECEIVED', max_digits=19, decimal_places=4)  # Field name made lowercase.
    sqcanceled = models.DecimalField(db_column='SQCANCELED', max_digits=19, decimal_places=4)  # Field name made lowercase.
    sqrcpextra = models.DecimalField(db_column='SQRCPEXTRA', max_digits=19, decimal_places=4)  # Field name made lowercase.
    sqsettled = models.DecimalField(db_column='SQSETTLED', max_digits=19, decimal_places=4)  # Field name made lowercase.
    sqoutstand = models.DecimalField(db_column='SQOUTSTAND', max_digits=19, decimal_places=4)  # Field name made lowercase.
    unitweight = models.DecimalField(db_column='UNITWEIGHT', max_digits=19, decimal_places=4)  # Field name made lowercase.
    extweight = models.DecimalField(db_column='EXTWEIGHT', max_digits=19, decimal_places=4)  # Field name made lowercase.
    oqrcpdays = models.DecimalField(db_column='OQRCPDAYS', max_digits=19, decimal_places=4)  # Field name made lowercase.
    extreceive = models.DecimalField(db_column='EXTRECEIVE', max_digits=19, decimal_places=3)  # Field name made lowercase.
    extcancel = models.DecimalField(db_column='EXTCANCEL', max_digits=19, decimal_places=3)  # Field name made lowercase.
    srreceived = models.DecimalField(db_column='SRRECEIVED', max_digits=19, decimal_places=3)  # Field name made lowercase.
    unitcost = models.DecimalField(db_column='UNITCOST', max_digits=19, decimal_places=6)  # Field name made lowercase.
    extended = models.DecimalField(db_column='EXTENDED', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxbase1 = models.DecimalField(db_column='TAXBASE1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxbase2 = models.DecimalField(db_column='TAXBASE2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxbase3 = models.DecimalField(db_column='TAXBASE3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxbase4 = models.DecimalField(db_column='TAXBASE4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxbase5 = models.DecimalField(db_column='TAXBASE5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxclass1 = models.SmallIntegerField(db_column='TAXCLASS1')  # Field name made lowercase.
    taxclass2 = models.SmallIntegerField(db_column='TAXCLASS2')  # Field name made lowercase.
    taxclass3 = models.SmallIntegerField(db_column='TAXCLASS3')  # Field name made lowercase.
    taxclass4 = models.SmallIntegerField(db_column='TAXCLASS4')  # Field name made lowercase.
    taxclass5 = models.SmallIntegerField(db_column='TAXCLASS5')  # Field name made lowercase.
    taxrate1 = models.DecimalField(db_column='TAXRATE1', max_digits=15, decimal_places=5)  # Field name made lowercase.
    taxrate2 = models.DecimalField(db_column='TAXRATE2', max_digits=15, decimal_places=5)  # Field name made lowercase.
    taxrate3 = models.DecimalField(db_column='TAXRATE3', max_digits=15, decimal_places=5)  # Field name made lowercase.
    taxrate4 = models.DecimalField(db_column='TAXRATE4', max_digits=15, decimal_places=5)  # Field name made lowercase.
    taxrate5 = models.DecimalField(db_column='TAXRATE5', max_digits=15, decimal_places=5)  # Field name made lowercase.
    taxinclud1 = models.SmallIntegerField(db_column='TAXINCLUD1')  # Field name made lowercase.
    taxinclud2 = models.SmallIntegerField(db_column='TAXINCLUD2')  # Field name made lowercase.
    taxinclud3 = models.SmallIntegerField(db_column='TAXINCLUD3')  # Field name made lowercase.
    taxinclud4 = models.SmallIntegerField(db_column='TAXINCLUD4')  # Field name made lowercase.
    taxinclud5 = models.SmallIntegerField(db_column='TAXINCLUD5')  # Field name made lowercase.
    taxamount1 = models.DecimalField(db_column='TAXAMOUNT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxamount2 = models.DecimalField(db_column='TAXAMOUNT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxamount3 = models.DecimalField(db_column='TAXAMOUNT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxamount4 = models.DecimalField(db_column='TAXAMOUNT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxamount5 = models.DecimalField(db_column='TAXAMOUNT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txalloamt1 = models.DecimalField(db_column='TXALLOAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txalloamt2 = models.DecimalField(db_column='TXALLOAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txalloamt3 = models.DecimalField(db_column='TXALLOAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txalloamt4 = models.DecimalField(db_column='TXALLOAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txalloamt5 = models.DecimalField(db_column='TXALLOAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecvamt1 = models.DecimalField(db_column='TXRECVAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecvamt2 = models.DecimalField(db_column='TXRECVAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecvamt3 = models.DecimalField(db_column='TXRECVAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecvamt4 = models.DecimalField(db_column='TXRECVAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecvamt5 = models.DecimalField(db_column='TXRECVAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexpsamt1 = models.DecimalField(db_column='TXEXPSAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexpsamt2 = models.DecimalField(db_column='TXEXPSAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexpsamt3 = models.DecimalField(db_column='TXEXPSAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexpsamt4 = models.DecimalField(db_column='TXEXPSAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexpsamt5 = models.DecimalField(db_column='TXEXPSAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbaseallo = models.DecimalField(db_column='TXBASEALLO', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txincluded = models.DecimalField(db_column='TXINCLUDED', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexcluded = models.DecimalField(db_column='TXEXCLUDED', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxamount = models.DecimalField(db_column='TAXAMOUNT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecvamt = models.DecimalField(db_column='TXRECVAMT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexpsamt = models.DecimalField(db_column='TXEXPSAMT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txalloamt = models.DecimalField(db_column='TXALLOAMT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    fcextended = models.DecimalField(db_column='FCEXTENDED', max_digits=19, decimal_places=3)  # Field name made lowercase.
    glacexpens = models.CharField(db_column='GLACEXPENS', max_length=45)  # Field name made lowercase.
    hasdropshi = models.SmallIntegerField(db_column='HASDROPSHI')  # Field name made lowercase.
    droptype = models.SmallIntegerField(db_column='DROPTYPE')  # Field name made lowercase.
    idcust = models.CharField(db_column='IDCUST', max_length=12)  # Field name made lowercase.
    idcustshpt = models.CharField(db_column='IDCUSTSHPT', max_length=6)  # Field name made lowercase.
    dlocation = models.CharField(db_column='DLOCATION', max_length=6)  # Field name made lowercase.
    desc = models.CharField(db_column='DESC', max_length=60)  # Field name made lowercase.
    address1 = models.CharField(db_column='ADDRESS1', max_length=60)  # Field name made lowercase.
    address2 = models.CharField(db_column='ADDRESS2', max_length=60)  # Field name made lowercase.
    address3 = models.CharField(db_column='ADDRESS3', max_length=60)  # Field name made lowercase.
    address4 = models.CharField(db_column='ADDRESS4', max_length=60)  # Field name made lowercase.
    city = models.CharField(db_column='CITY', max_length=30)  # Field name made lowercase.
    state = models.CharField(db_column='STATE', max_length=30)  # Field name made lowercase.
    zip = models.CharField(db_column='ZIP', max_length=20)  # Field name made lowercase.
    country = models.CharField(db_column='COUNTRY', max_length=30)  # Field name made lowercase.
    phone = models.CharField(db_column='PHONE', max_length=30)  # Field name made lowercase.
    fax = models.CharField(db_column='FAX', max_length=30)  # Field name made lowercase.
    contact = models.CharField(db_column='CONTACT', max_length=60)  # Field name made lowercase.
    stockitem = models.SmallIntegerField(db_column='STOCKITEM')  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=50)  # Field name made lowercase.
    phonec = models.CharField(db_column='PHONEC', max_length=30)  # Field name made lowercase.
    faxc = models.CharField(db_column='FAXC', max_length=30)  # Field name made lowercase.
    emailc = models.CharField(db_column='EMAILC', max_length=50)  # Field name made lowercase.
    glnonstkcr = models.CharField(db_column='GLNONSTKCR', max_length=45)  # Field name made lowercase.
    manitemno = models.CharField(db_column='MANITEMNO', max_length=24)  # Field name made lowercase.
    discpct = models.DecimalField(db_column='DISCPCT', max_digits=9, decimal_places=5)  # Field name made lowercase.
    discount = models.DecimalField(db_column='DISCOUNT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    values = models.IntegerField(db_column='VALUES')  # Field name made lowercase.
    discountf = models.DecimalField(db_column='DISCOUNTF', max_digits=19, decimal_places=3)  # Field name made lowercase.
    isreceived = models.SmallIntegerField(db_column='ISRECEIVED')  # Field name made lowercase.
    agentlseq = models.DecimalField(db_column='AGENTLSEQ', max_digits=19, decimal_places=0)  # Field name made lowercase.
    contract = models.CharField(db_column='CONTRACT', max_length=16)  # Field name made lowercase.
    project = models.CharField(db_column='PROJECT', max_length=16)  # Field name made lowercase.
    ccategory = models.CharField(db_column='CCATEGORY', max_length=16)  # Field name made lowercase.
    costclass = models.SmallIntegerField(db_column='COSTCLASS')  # Field name made lowercase.
    billtype = models.SmallIntegerField(db_column='BILLTYPE')  # Field name made lowercase.
    billrate = models.DecimalField(db_column='BILLRATE', max_digits=19, decimal_places=6)  # Field name made lowercase.
    billcurr = models.CharField(db_column='BILLCURR', max_length=3)  # Field name made lowercase.
    aritemno = models.CharField(db_column='ARITEMNO', max_length=16)  # Field name made lowercase.
    arunit = models.CharField(db_column='ARUNIT', max_length=10)  # Field name made lowercase.
    tfbaseallo = models.DecimalField(db_column='TFBASEALLO', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfinclude1 = models.DecimalField(db_column='TFINCLUDE1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfinclude2 = models.DecimalField(db_column='TFINCLUDE2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfinclude3 = models.DecimalField(db_column='TFINCLUDE3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfinclude4 = models.DecimalField(db_column='TFINCLUDE4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfinclude5 = models.DecimalField(db_column='TFINCLUDE5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfalloamt1 = models.DecimalField(db_column='TFALLOAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfalloamt2 = models.DecimalField(db_column='TFALLOAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfalloamt3 = models.DecimalField(db_column='TFALLOAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfalloamt4 = models.DecimalField(db_column='TFALLOAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfalloamt5 = models.DecimalField(db_column='TFALLOAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfrecvamt1 = models.DecimalField(db_column='TFRECVAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfrecvamt2 = models.DecimalField(db_column='TFRECVAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfrecvamt3 = models.DecimalField(db_column='TFRECVAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfrecvamt4 = models.DecimalField(db_column='TFRECVAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfrecvamt5 = models.DecimalField(db_column='TFRECVAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfexpsamt1 = models.DecimalField(db_column='TFEXPSAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfexpsamt2 = models.DecimalField(db_column='TFEXPSAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfexpsamt3 = models.DecimalField(db_column='TFEXPSAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfexpsamt4 = models.DecimalField(db_column='TFEXPSAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tfexpsamt5 = models.DecimalField(db_column='TFEXPSAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taramount1 = models.DecimalField(db_column='TARAMOUNT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taramount2 = models.DecimalField(db_column='TARAMOUNT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taramount3 = models.DecimalField(db_column='TARAMOUNT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taramount4 = models.DecimalField(db_column='TARAMOUNT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taramount5 = models.DecimalField(db_column='TARAMOUNT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tralloamt1 = models.DecimalField(db_column='TRALLOAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tralloamt2 = models.DecimalField(db_column='TRALLOAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tralloamt3 = models.DecimalField(db_column='TRALLOAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tralloamt4 = models.DecimalField(db_column='TRALLOAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tralloamt5 = models.DecimalField(db_column='TRALLOAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trrecvamt1 = models.DecimalField(db_column='TRRECVAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trrecvamt2 = models.DecimalField(db_column='TRRECVAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trrecvamt3 = models.DecimalField(db_column='TRRECVAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trrecvamt4 = models.DecimalField(db_column='TRRECVAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trrecvamt5 = models.DecimalField(db_column='TRRECVAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trexpsamt1 = models.DecimalField(db_column='TREXPSAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trexpsamt2 = models.DecimalField(db_column='TREXPSAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trexpsamt3 = models.DecimalField(db_column='TREXPSAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trexpsamt4 = models.DecimalField(db_column='TREXPSAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trexpsamt5 = models.DecimalField(db_column='TREXPSAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    ucismanual = models.SmallIntegerField(db_column='UCISMANUAL')  # Field name made lowercase.
    weightunit = models.CharField(db_column='WEIGHTUNIT', max_length=10)  # Field name made lowercase.
    weightconv = models.DecimalField(db_column='WEIGHTCONV', max_digits=19, decimal_places=6)  # Field name made lowercase.
    defuweight = models.DecimalField(db_column='DEFUWEIGHT', max_digits=19, decimal_places=4)  # Field name made lowercase.
    defextwght = models.DecimalField(db_column='DEFEXTWGHT', max_digits=19, decimal_places=4)  # Field name made lowercase.
    copydetail = models.SmallIntegerField(db_column='COPYDETAIL')  # Field name made lowercase.
    detailnum = models.SmallIntegerField(db_column='DETAILNUM')  # Field name made lowercase.
    caxable1 = models.SmallIntegerField(db_column='CAXABLE1')  # Field name made lowercase.
    caxable2 = models.SmallIntegerField(db_column='CAXABLE2')  # Field name made lowercase.
    caxable3 = models.SmallIntegerField(db_column='CAXABLE3')  # Field name made lowercase.
    caxable4 = models.SmallIntegerField(db_column='CAXABLE4')  # Field name made lowercase.
    caxable5 = models.SmallIntegerField(db_column='CAXABLE5')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'POPORL'
        unique_together = (('porhseq', 'porlrev'), ('porhseq', 'porlseq'), ('oeonumber', 'porhseq', 'porlseq'), ('itemno', 'exparrival', 'porhseq', 'porlseq'), ('porhseq', 'detailnum', 'porlseq'),)


class Enebh(models.Model):
    cntbtch = models.IntegerField(db_column='CNTBTCH', primary_key=True)  # Field name made lowercase. The composite primary key (CNTBTCH, CNTITEM) found, that is not supported. The first column is selected.
    cntitem = models.IntegerField(db_column='CNTITEM')  # Field name made lowercase.
    audtdate = models.DecimalField(db_column='AUDTDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    audttime = models.DecimalField(db_column='AUDTTIME', max_digits=9, decimal_places=0)  # Field name made lowercase.
    audtuser = models.CharField(db_column='AUDTUSER', max_length=8)  # Field name made lowercase.
    audtorg = models.CharField(db_column='AUDTORG', max_length=6)  # Field name made lowercase.
    idemployee = models.CharField(db_column='IDEMPLOYEE', max_length=12)  # Field name made lowercase.
    idexpst = models.CharField(db_column='IDEXPST', max_length=22)  # Field name made lowercase.
    texttrx = models.SmallIntegerField(db_column='TEXTTRX')  # Field name made lowercase.
    expdesc = models.CharField(db_column='EXPDESC', max_length=60)  # Field name made lowercase.
    adjapplto = models.CharField(db_column='ADJAPPLTO', max_length=22)  # Field name made lowercase.
    datedoc = models.DecimalField(db_column='DATEDOC', max_digits=9, decimal_places=0)  # Field name made lowercase.
    fiscyr = models.CharField(db_column='FISCYR', max_length=4)  # Field name made lowercase.
    fiscper = models.CharField(db_column='FISCPER', max_length=2)  # Field name made lowercase.
    currcode = models.CharField(db_column='CURRCODE', max_length=3)  # Field name made lowercase.
    ratetype = models.CharField(db_column='RATETYPE', max_length=2)  # Field name made lowercase.
    exchratehc = models.DecimalField(db_column='EXCHRATEHC', max_digits=15, decimal_places=7)  # Field name made lowercase.
    ratedate = models.DecimalField(db_column='RATEDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    lineqty = models.IntegerField(db_column='LINEQTY')  # Field name made lowercase.
    lastline = models.IntegerField(db_column='LASTLINE')  # Field name made lowercase.
    codedivis = models.CharField(db_column='CODEDIVIS', max_length=12)  # Field name made lowercase.
    codereg = models.CharField(db_column='CODEREG', max_length=12)  # Field name made lowercase.
    codedep = models.CharField(db_column='CODEDEP', max_length=12)  # Field name made lowercase.
    codecst = models.CharField(db_column='CODECST', max_length=12)  # Field name made lowercase.
    codejob = models.CharField(db_column='CODEJOB', max_length=16)  # Field name made lowercase.
    textopfl1 = models.CharField(db_column='TEXTOPFL1', max_length=2)  # Field name made lowercase.
    textopfl2 = models.CharField(db_column='TEXTOPFL2', max_length=3)  # Field name made lowercase.
    textopfl3 = models.CharField(db_column='TEXTOPFL3', max_length=4)  # Field name made lowercase.
    textopfl4 = models.CharField(db_column='TEXTOPFL4', max_length=12)  # Field name made lowercase.
    textopfl5 = models.CharField(db_column='TEXTOPFL5', max_length=15)  # Field name made lowercase.
    textopfl6 = models.CharField(db_column='TEXTOPFL6', max_length=30)  # Field name made lowercase.
    dateopfl1 = models.DecimalField(db_column='DATEOPFL1', max_digits=9, decimal_places=0)  # Field name made lowercase.
    amtopfl1 = models.DecimalField(db_column='AMTOPFL1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amtreimbt = models.DecimalField(db_column='AMTREIMBT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amtreimbh = models.DecimalField(db_column='AMTREIMBH', max_digits=19, decimal_places=3)  # Field name made lowercase.
    refdocid = models.CharField(db_column='REFDOCID', max_length=22)  # Field name made lowercase.
    suvisor = models.CharField(db_column='SUVISOR', max_length=12)  # Field name made lowercase.
    invstts = models.SmallIntegerField(db_column='INVSTTS')  # Field name made lowercase.
    idven = models.CharField(db_column='IDVEN', max_length=12)  # Field name made lowercase.
    invid = models.CharField(db_column='INVID', max_length=22)  # Field name made lowercase.
    swtaxbl = models.SmallIntegerField(db_column='SWTAXBL')  # Field name made lowercase.
    swcalctxa = models.SmallIntegerField(db_column='SWCALCTXA')  # Field name made lowercase.
    swcalctxb = models.SmallIntegerField(db_column='SWCALCTXB')  # Field name made lowercase.
    codetaxgrp = models.CharField(db_column='CODETAXGRP', max_length=12)  # Field name made lowercase.
    codetax1 = models.CharField(db_column='CODETAX1', max_length=12)  # Field name made lowercase.
    codetax2 = models.CharField(db_column='CODETAX2', max_length=12)  # Field name made lowercase.
    codetax3 = models.CharField(db_column='CODETAX3', max_length=12)  # Field name made lowercase.
    codetax4 = models.CharField(db_column='CODETAX4', max_length=12)  # Field name made lowercase.
    codetax5 = models.CharField(db_column='CODETAX5', max_length=12)  # Field name made lowercase.
    swtaxincl1 = models.SmallIntegerField(db_column='SWTAXINCL1')  # Field name made lowercase.
    swtaxincl2 = models.SmallIntegerField(db_column='SWTAXINCL2')  # Field name made lowercase.
    swtaxincl3 = models.SmallIntegerField(db_column='SWTAXINCL3')  # Field name made lowercase.
    swtaxincl4 = models.SmallIntegerField(db_column='SWTAXINCL4')  # Field name made lowercase.
    swtaxincl5 = models.SmallIntegerField(db_column='SWTAXINCL5')  # Field name made lowercase.
    taxclass1 = models.SmallIntegerField(db_column='TAXCLASS1')  # Field name made lowercase.
    taxclass2 = models.SmallIntegerField(db_column='TAXCLASS2')  # Field name made lowercase.
    taxclass3 = models.SmallIntegerField(db_column='TAXCLASS3')  # Field name made lowercase.
    taxclass4 = models.SmallIntegerField(db_column='TAXCLASS4')  # Field name made lowercase.
    taxclass5 = models.SmallIntegerField(db_column='TAXCLASS5')  # Field name made lowercase.
    taxrate1 = models.DecimalField(db_column='TAXRATE1', max_digits=15, decimal_places=5)  # Field name made lowercase.
    taxrate2 = models.DecimalField(db_column='TAXRATE2', max_digits=15, decimal_places=5)  # Field name made lowercase.
    taxrate3 = models.DecimalField(db_column='TAXRATE3', max_digits=15, decimal_places=5)  # Field name made lowercase.
    taxrate4 = models.DecimalField(db_column='TAXRATE4', max_digits=15, decimal_places=5)  # Field name made lowercase.
    taxrate5 = models.DecimalField(db_column='TAXRATE5', max_digits=15, decimal_places=5)  # Field name made lowercase.
    basetax1 = models.DecimalField(db_column='BASETAX1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    basetax2 = models.DecimalField(db_column='BASETAX2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    basetax3 = models.DecimalField(db_column='BASETAX3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    basetax4 = models.DecimalField(db_column='BASETAX4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    basetax5 = models.DecimalField(db_column='BASETAX5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amttax1 = models.DecimalField(db_column='AMTTAX1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amttax2 = models.DecimalField(db_column='AMTTAX2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amttax3 = models.DecimalField(db_column='AMTTAX3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amttax4 = models.DecimalField(db_column='AMTTAX4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amttax5 = models.DecimalField(db_column='AMTTAX5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    swcaltax = models.SmallIntegerField(db_column='SWCALTAX')  # Field name made lowercase.
    totaltax = models.DecimalField(db_column='TOTALTAX', max_digits=19, decimal_places=3)  # Field name made lowercase.
    jobrelated = models.SmallIntegerField(db_column='JOBRELATED')  # Field name made lowercase.
    codealloc = models.CharField(db_column='CODEALLOC', max_length=12)  # Field name made lowercase.
    allocamt = models.DecimalField(db_column='ALLOCAMT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    values = models.IntegerField(db_column='VALUES')  # Field name made lowercase.
    processcmd = models.SmallIntegerField(db_column='PROCESSCMD')  # Field name made lowercase.
    route = models.CharField(db_column='ROUTE', max_length=12)  # Field name made lowercase.
    orgcomp = models.CharField(db_column='ORGCOMP', max_length=6)  # Field name made lowercase.
    reimbacct = models.CharField(db_column='REIMBACCT', max_length=45)  # Field name made lowercase.
    dratesprea = models.DecimalField(db_column='DRATESPREA', max_digits=15, decimal_places=7)  # Field name made lowercase.
    dratemtchc = models.SmallIntegerField(db_column='DRATEMTCHC')  # Field name made lowercase.
    drateoper = models.SmallIntegerField(db_column='DRATEOPER')  # Field name made lowercase.
    payrlflag = models.SmallIntegerField(db_column='PAYRLFLAG')  # Field name made lowercase.
    payrlempid = models.CharField(db_column='PAYRLEMPID', max_length=12)  # Field name made lowercase.
    penddate = models.DecimalField(db_column='PENDDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    earnded = models.CharField(db_column='EARNDED', max_length=12)  # Field name made lowercase.
    pyrlcurr = models.CharField(db_column='PYRLCURR', max_length=3)  # Field name made lowercase.
    codecurnrc = models.CharField(db_column='CODECURNRC', max_length=3)  # Field name made lowercase.
    raterc = models.DecimalField(db_column='RATERC', max_digits=15, decimal_places=7)  # Field name made lowercase.
    ratedaterc = models.DecimalField(db_column='RATEDATERC', max_digits=9, decimal_places=0)  # Field name made lowercase.
    ratetyperc = models.CharField(db_column='RATETYPERC', max_length=2)  # Field name made lowercase.
    rateoprc = models.SmallIntegerField(db_column='RATEOPRC')  # Field name made lowercase.
    swraterc = models.SmallIntegerField(db_column='SWRATERC')  # Field name made lowercase.
    swtxctlrc = models.SmallIntegerField(db_column='SWTXCTLRC')  # Field name made lowercase.
    txbs1tc = models.DecimalField(db_column='TXBS1TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbs2tc = models.DecimalField(db_column='TXBS2TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbs3tc = models.DecimalField(db_column='TXBS3TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbs4tc = models.DecimalField(db_column='TXBS4TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbs5tc = models.DecimalField(db_column='TXBS5TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt1tc = models.DecimalField(db_column='TXAMT1TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt2tc = models.DecimalField(db_column='TXAMT2TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt3tc = models.DecimalField(db_column='TXAMT3TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt4tc = models.DecimalField(db_column='TXAMT4TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt5tc = models.DecimalField(db_column='TXAMT5TC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txtotrc = models.DecimalField(db_column='TXTOTRC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txallrc = models.DecimalField(db_column='TXALLRC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexprc = models.DecimalField(db_column='TXEXPRC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecrc = models.DecimalField(db_column='TXRECRC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbs1hc = models.DecimalField(db_column='TXBS1HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbs2hc = models.DecimalField(db_column='TXBS2HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbs3hc = models.DecimalField(db_column='TXBS3HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbs4hc = models.DecimalField(db_column='TXBS4HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbs5hc = models.DecimalField(db_column='TXBS5HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt1hc = models.DecimalField(db_column='TXAMT1HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt2hc = models.DecimalField(db_column='TXAMT2HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt3hc = models.DecimalField(db_column='TXAMT3HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt4hc = models.DecimalField(db_column='TXAMT4HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txamt5hc = models.DecimalField(db_column='TXAMT5HC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txtotrchc = models.DecimalField(db_column='TXTOTRCHC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txallrchc = models.DecimalField(db_column='TXALLRCHC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexprchc = models.DecimalField(db_column='TXEXPRCHC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecrchc = models.DecimalField(db_column='TXRECRCHC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    acctrec1 = models.CharField(db_column='ACCTREC1', max_length=45)  # Field name made lowercase.
    acctrec2 = models.CharField(db_column='ACCTREC2', max_length=45)  # Field name made lowercase.
    acctrec3 = models.CharField(db_column='ACCTREC3', max_length=45)  # Field name made lowercase.
    acctrec4 = models.CharField(db_column='ACCTREC4', max_length=45)  # Field name made lowercase.
    acctrec5 = models.CharField(db_column='ACCTREC5', max_length=45)  # Field name made lowercase.
    acctexp1 = models.CharField(db_column='ACCTEXP1', max_length=45)  # Field name made lowercase.
    acctexp2 = models.CharField(db_column='ACCTEXP2', max_length=45)  # Field name made lowercase.
    acctexp3 = models.CharField(db_column='ACCTEXP3', max_length=45)  # Field name made lowercase.
    acctexp4 = models.CharField(db_column='ACCTEXP4', max_length=45)  # Field name made lowercase.
    acctexp5 = models.CharField(db_column='ACCTEXP5', max_length=45)  # Field name made lowercase.
    employeid = models.CharField(db_column='EMPLOYEID', max_length=16)  # Field name made lowercase.
    entrytype = models.SmallIntegerField(db_column='ENTRYTYPE')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='STATUS')  # Field name made lowercase.
    postdate = models.DecimalField(db_column='POSTDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    reimcurr = models.CharField(db_column='REIMCURR', max_length=3)  # Field name made lowercase.
    rmratetype = models.CharField(db_column='RMRATETYPE', max_length=2)  # Field name made lowercase.
    rmratedate = models.DecimalField(db_column='RMRATEDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    exchraterm = models.DecimalField(db_column='EXCHRATERM', max_digits=15, decimal_places=7)  # Field name made lowercase.
    amtexprm = models.DecimalField(db_column='AMTEXPRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    manager = models.CharField(db_column='MANAGER', max_length=16)  # Field name made lowercase.
    pid = models.CharField(db_column='PID', max_length=36)  # Field name made lowercase.
    txdishc = models.DecimalField(db_column='TXDISHC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amtgldishc = models.DecimalField(db_column='AMTGLDISHC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    doctothc = models.DecimalField(db_column='DOCTOTHC', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txtotrm = models.DecimalField(db_column='TXTOTRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexprm = models.DecimalField(db_column='TXEXPRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecrm = models.DecimalField(db_column='TXRECRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txallrm = models.DecimalField(db_column='TXALLRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txdisrm = models.DecimalField(db_column='TXDISRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    amtgldisrm = models.DecimalField(db_column='AMTGLDISRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    doctotrm = models.DecimalField(db_column='DOCTOTRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    attaches = models.IntegerField(db_column='ATTACHES')  # Field name made lowercase.
    submitdate = models.DecimalField(db_column='SUBMITDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    appvdate = models.DecimalField(db_column='APPVDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    subemp = models.CharField(db_column='SUBEMP', max_length=16)  # Field name made lowercase.
    synced = models.SmallIntegerField(db_column='SYNCED')  # Field name made lowercase.
    billamth = models.DecimalField(db_column='BILLAMTH', max_digits=19, decimal_places=3)  # Field name made lowercase.
    billamts = models.DecimalField(db_column='BILLAMTS', max_digits=19, decimal_places=3)  # Field name made lowercase.
    wfid = models.CharField(db_column='WFID', max_length=12)  # Field name made lowercase.
    wfver = models.IntegerField(db_column='WFVER')  # Field name made lowercase.
    begindate = models.DecimalField(db_column='BEGINDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    enddate = models.DecimalField(db_column='ENDDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    apprcnt = models.IntegerField(db_column='APPRCNT')  # Field name made lowercase.
    rejectcnt = models.IntegerField(db_column='REJECTCNT')  # Field name made lowercase.
    passcnt = models.IntegerField(db_column='PASSCNT')  # Field name made lowercase.
    swlock = models.SmallIntegerField(db_column='SWLOCK')  # Field name made lowercase.
    lockid = models.CharField(db_column='LOCKID', max_length=36)  # Field name made lowercase.
    rejected = models.SmallIntegerField(db_column='REJECTED')  # Field name made lowercase.
    expwfby = models.SmallIntegerField(db_column='EXPWFBY')  # Field name made lowercase.
    otxtotrm = models.DecimalField(db_column='OTXTOTRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    otxexprm = models.DecimalField(db_column='OTXEXPRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    otxrecrm = models.DecimalField(db_column='OTXRECRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    otxallrm = models.DecimalField(db_column='OTXALLRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    otxdisrm = models.DecimalField(db_column='OTXDISRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    ogldisrm = models.DecimalField(db_column='OGLDISRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    odoctotrm = models.DecimalField(db_column='ODOCTOTRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    crcardrm = models.DecimalField(db_column='CRCARDRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    loccode = models.CharField(db_column='LOCCODE', max_length=16)  # Field name made lowercase.
    exptype = models.CharField(db_column='EXPTYPE', max_length=16)  # Field name made lowercase.
    swtrreq = models.SmallIntegerField(db_column='SWTRREQ')  # Field name made lowercase.
    trreqid = models.CharField(db_column='TRREQID', max_length=36)  # Field name made lowercase.
    swtype = models.SmallIntegerField(db_column='SWTYPE')  # Field name made lowercase.
    cadocno = models.CharField(db_column='CADOCNO', max_length=22)  # Field name made lowercase.
    cabalrm = models.DecimalField(db_column='CABALRM', max_digits=19, decimal_places=3)  # Field name made lowercase.
    applyamt = models.DecimalField(db_column='APPLYAMT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    applyamth = models.DecimalField(db_column='APPLYAMTH', max_digits=19, decimal_places=3)  # Field name made lowercase.
    isovlimit = models.SmallIntegerField(db_column='ISOVLIMIT')  # Field name made lowercase.
    isovglbg = models.SmallIntegerField(db_column='ISOVGLBG')  # Field name made lowercase.
    isovpjcbg = models.SmallIntegerField(db_column='ISOVPJCBG')  # Field name made lowercase.
    swplussign = models.SmallIntegerField(db_column='SWPLUSSIGN')  # Field name made lowercase.
    nonrbby = models.SmallIntegerField(db_column='NONRBBY')  # Field name made lowercase.
    swrb = models.SmallIntegerField(db_column='SWRB')  # Field name made lowercase.
    swcrcard = models.SmallIntegerField(db_column='SWCRCARD')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ENEBH'
        unique_together = (('cntbtch', 'cntitem'), ('employeid', 'idexpst'),)


class Poporh1(models.Model):
    porhseq = models.DecimalField(db_column='PORHSEQ', primary_key=True, max_digits=19, decimal_places=0)  # Field name made lowercase.
    audtdate = models.DecimalField(db_column='AUDTDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    audttime = models.DecimalField(db_column='AUDTTIME', max_digits=9, decimal_places=0)  # Field name made lowercase.
    audtuser = models.CharField(db_column='AUDTUSER', max_length=8)  # Field name made lowercase.
    audtorg = models.CharField(db_column='AUDTORG', max_length=6)  # Field name made lowercase.
    nextlseq = models.DecimalField(db_column='NEXTLSEQ', max_digits=19, decimal_places=0)  # Field name made lowercase.
    lines = models.IntegerField(db_column='LINES')  # Field name made lowercase.
    linescmpl = models.IntegerField(db_column='LINESCMPL')  # Field name made lowercase.
    taxlines = models.IntegerField(db_column='TAXLINES')  # Field name made lowercase.
    rqns = models.IntegerField(db_column='RQNS')  # Field name made lowercase.
    rqnscmpl = models.IntegerField(db_column='RQNSCMPL')  # Field name made lowercase.
    isprinted = models.SmallIntegerField(db_column='ISPRINTED')  # Field name made lowercase.
    taxautocal = models.SmallIntegerField(db_column='TAXAUTOCAL')  # Field name made lowercase.
    labelprint = models.SmallIntegerField(db_column='LABELPRINT')  # Field name made lowercase.
    labelcount = models.SmallIntegerField(db_column='LABELCOUNT')  # Field name made lowercase.
    iscomplete = models.SmallIntegerField(db_column='ISCOMPLETE')  # Field name made lowercase.
    dtcomplete = models.DecimalField(db_column='DTCOMPLETE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    postdate = models.DecimalField(db_column='POSTDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    date = models.DecimalField(db_column='DATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    ponumber = models.CharField(db_column='PONUMBER', unique=True, max_length=22)  # Field name made lowercase.
    template = models.CharField(db_column='TEMPLATE', max_length=6)  # Field name made lowercase.
    fobpoint = models.CharField(db_column='FOBPOINT', max_length=60)  # Field name made lowercase.
    vdcode = models.CharField(db_column='VDCODE', max_length=12)  # Field name made lowercase.
    vdexists = models.SmallIntegerField(db_column='VDEXISTS')  # Field name made lowercase.
    vdname = models.CharField(db_column='VDNAME', max_length=60)  # Field name made lowercase.
    vdaddress1 = models.CharField(db_column='VDADDRESS1', max_length=60)  # Field name made lowercase.
    vdaddress2 = models.CharField(db_column='VDADDRESS2', max_length=60)  # Field name made lowercase.
    vdaddress3 = models.CharField(db_column='VDADDRESS3', max_length=60)  # Field name made lowercase.
    vdaddress4 = models.CharField(db_column='VDADDRESS4', max_length=60)  # Field name made lowercase.
    vdcity = models.CharField(db_column='VDCITY', max_length=30)  # Field name made lowercase.
    vdstate = models.CharField(db_column='VDSTATE', max_length=30)  # Field name made lowercase.
    vdzip = models.CharField(db_column='VDZIP', max_length=20)  # Field name made lowercase.
    vdcountry = models.CharField(db_column='VDCOUNTRY', max_length=30)  # Field name made lowercase.
    vdphone = models.CharField(db_column='VDPHONE', max_length=30)  # Field name made lowercase.
    vdfax = models.CharField(db_column='VDFAX', max_length=30)  # Field name made lowercase.
    vdcontact = models.CharField(db_column='VDCONTACT', max_length=60)  # Field name made lowercase.
    termscode = models.CharField(db_column='TERMSCODE', max_length=6)  # Field name made lowercase.
    hasrqndata = models.SmallIntegerField(db_column='HASRQNDATA')  # Field name made lowercase.
    portype = models.SmallIntegerField(db_column='PORTYPE')  # Field name made lowercase.
    onhold = models.SmallIntegerField(db_column='ONHOLD')  # Field name made lowercase.
    orderedon = models.DecimalField(db_column='ORDEREDON', max_digits=9, decimal_places=0)  # Field name made lowercase.
    exparrival = models.DecimalField(db_column='EXPARRIVAL', max_digits=9, decimal_places=0)  # Field name made lowercase.
    vcoriginal = models.DecimalField(db_column='VCORIGINAL', max_digits=19, decimal_places=3)  # Field name made lowercase.
    vcavailabl = models.DecimalField(db_column='VCAVAILABL', max_digits=19, decimal_places=3)  # Field name made lowercase.
    descriptio = models.CharField(db_column='DESCRIPTIO', max_length=60)  # Field name made lowercase.
    reference = models.CharField(db_column='REFERENCE', max_length=60)  # Field name made lowercase.
    comment = models.CharField(db_column='COMMENT', max_length=250)  # Field name made lowercase.
    viacode = models.CharField(db_column='VIACODE', max_length=6)  # Field name made lowercase.
    vianame = models.CharField(db_column='VIANAME', max_length=60)  # Field name made lowercase.
    lastreceip = models.CharField(db_column='LASTRECEIP', max_length=22)  # Field name made lowercase.
    rcpdate = models.DecimalField(db_column='RCPDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    rcpcount = models.SmallIntegerField(db_column='RCPCOUNT')  # Field name made lowercase.
    currency = models.CharField(db_column='CURRENCY', max_length=3)  # Field name made lowercase.
    rate = models.DecimalField(db_column='RATE', max_digits=15, decimal_places=7)  # Field name made lowercase.
    spread = models.DecimalField(db_column='SPREAD', max_digits=15, decimal_places=7)  # Field name made lowercase.
    ratetype = models.CharField(db_column='RATETYPE', max_length=2)  # Field name made lowercase.
    ratematch = models.SmallIntegerField(db_column='RATEMATCH')  # Field name made lowercase.
    ratedate = models.DecimalField(db_column='RATEDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
    rateoper = models.SmallIntegerField(db_column='RATEOPER')  # Field name made lowercase.
    rateover = models.SmallIntegerField(db_column='RATEOVER')  # Field name made lowercase.
    scurndecml = models.SmallIntegerField(db_column='SCURNDECML')  # Field name made lowercase.
    extweight = models.DecimalField(db_column='EXTWEIGHT', max_digits=19, decimal_places=4)  # Field name made lowercase.
    extended = models.DecimalField(db_column='EXTENDED', max_digits=19, decimal_places=3)  # Field name made lowercase.
    doctotal = models.DecimalField(db_column='DOCTOTAL', max_digits=19, decimal_places=3)  # Field name made lowercase.
    extreceive = models.DecimalField(db_column='EXTRECEIVE', max_digits=19, decimal_places=3)  # Field name made lowercase.
    extcancel = models.DecimalField(db_column='EXTCANCEL', max_digits=19, decimal_places=3)  # Field name made lowercase.
    oqordered = models.DecimalField(db_column='OQORDERED', max_digits=19, decimal_places=4)  # Field name made lowercase.
    taxgroup = models.CharField(db_column='TAXGROUP', max_length=12)  # Field name made lowercase.
    taxauth1 = models.CharField(db_column='TAXAUTH1', max_length=12)  # Field name made lowercase.
    taxauth2 = models.CharField(db_column='TAXAUTH2', max_length=12)  # Field name made lowercase.
    taxauth3 = models.CharField(db_column='TAXAUTH3', max_length=12)  # Field name made lowercase.
    taxauth4 = models.CharField(db_column='TAXAUTH4', max_length=12)  # Field name made lowercase.
    taxauth5 = models.CharField(db_column='TAXAUTH5', max_length=12)  # Field name made lowercase.
    taxclass1 = models.SmallIntegerField(db_column='TAXCLASS1')  # Field name made lowercase.
    taxclass2 = models.SmallIntegerField(db_column='TAXCLASS2')  # Field name made lowercase.
    taxclass3 = models.SmallIntegerField(db_column='TAXCLASS3')  # Field name made lowercase.
    taxclass4 = models.SmallIntegerField(db_column='TAXCLASS4')  # Field name made lowercase.
    taxclass5 = models.SmallIntegerField(db_column='TAXCLASS5')  # Field name made lowercase.
    taxbase1 = models.DecimalField(db_column='TAXBASE1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxbase2 = models.DecimalField(db_column='TAXBASE2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxbase3 = models.DecimalField(db_column='TAXBASE3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxbase4 = models.DecimalField(db_column='TAXBASE4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxbase5 = models.DecimalField(db_column='TAXBASE5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txinclude1 = models.DecimalField(db_column='TXINCLUDE1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txinclude2 = models.DecimalField(db_column='TXINCLUDE2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txinclude3 = models.DecimalField(db_column='TXINCLUDE3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txinclude4 = models.DecimalField(db_column='TXINCLUDE4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txinclude5 = models.DecimalField(db_column='TXINCLUDE5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexclude1 = models.DecimalField(db_column='TXEXCLUDE1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexclude2 = models.DecimalField(db_column='TXEXCLUDE2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexclude3 = models.DecimalField(db_column='TXEXCLUDE3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexclude4 = models.DecimalField(db_column='TXEXCLUDE4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexclude5 = models.DecimalField(db_column='TXEXCLUDE5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxamount1 = models.DecimalField(db_column='TAXAMOUNT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxamount2 = models.DecimalField(db_column='TAXAMOUNT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxamount3 = models.DecimalField(db_column='TAXAMOUNT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxamount4 = models.DecimalField(db_column='TAXAMOUNT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxamount5 = models.DecimalField(db_column='TAXAMOUNT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecvamt1 = models.DecimalField(db_column='TXRECVAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecvamt2 = models.DecimalField(db_column='TXRECVAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecvamt3 = models.DecimalField(db_column='TXRECVAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecvamt4 = models.DecimalField(db_column='TXRECVAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecvamt5 = models.DecimalField(db_column='TXRECVAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexpsamt1 = models.DecimalField(db_column='TXEXPSAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexpsamt2 = models.DecimalField(db_column='TXEXPSAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexpsamt3 = models.DecimalField(db_column='TXEXPSAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexpsamt4 = models.DecimalField(db_column='TXEXPSAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexpsamt5 = models.DecimalField(db_column='TXEXPSAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txalloamt1 = models.DecimalField(db_column='TXALLOAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txalloamt2 = models.DecimalField(db_column='TXALLOAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txalloamt3 = models.DecimalField(db_column='TXALLOAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txalloamt4 = models.DecimalField(db_column='TXALLOAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txalloamt5 = models.DecimalField(db_column='TXALLOAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txbaseallo = models.DecimalField(db_column='TXBASEALLO', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txincluded = models.DecimalField(db_column='TXINCLUDED', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexcluded = models.DecimalField(db_column='TXEXCLUDED', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taxamount = models.DecimalField(db_column='TAXAMOUNT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txrecvamt = models.DecimalField(db_column='TXRECVAMT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txexpsamt = models.DecimalField(db_column='TXEXPSAMT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    txalloamt = models.DecimalField(db_column='TXALLOAMT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    docsource = models.SmallIntegerField(db_column='DOCSOURCE')  # Field name made lowercase.
    vdemail = models.CharField(db_column='VDEMAIL', max_length=50)  # Field name made lowercase.
    vdphonec = models.CharField(db_column='VDPHONEC', max_length=30)  # Field name made lowercase.
    vdfaxc = models.CharField(db_column='VDFAXC', max_length=30)  # Field name made lowercase.
    vdemailc = models.CharField(db_column='VDEMAILC', max_length=50)  # Field name made lowercase.
    discpct = models.DecimalField(db_column='DISCPCT', max_digits=9, decimal_places=5)  # Field name made lowercase.
    discount = models.DecimalField(db_column='DISCOUNT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    values = models.IntegerField(db_column='VALUES')  # Field name made lowercase.
    rqnnumber = models.CharField(db_column='RQNNUMBER', max_length=22)  # Field name made lowercase.
    rqnhseq = models.DecimalField(db_column='RQNHSEQ', max_digits=19, decimal_places=0)  # Field name made lowercase.
    scamount = models.DecimalField(db_column='SCAMOUNT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    fcamount = models.DecimalField(db_column='FCAMOUNT', max_digits=19, decimal_places=3)  # Field name made lowercase.
    joblines = models.IntegerField(db_column='JOBLINES')  # Field name made lowercase.
    trcurrency = models.CharField(db_column='TRCURRENCY', max_length=3)  # Field name made lowercase.
    raterc = models.DecimalField(db_column='RATERC', max_digits=15, decimal_places=7)  # Field name made lowercase.
    spreadrc = models.DecimalField(db_column='SPREADRC', max_digits=15, decimal_places=7)  # Field name made lowercase.
    ratetyperc = models.CharField(db_column='RATETYPERC', max_length=2)  # Field name made lowercase.
    ratemtchrc = models.SmallIntegerField(db_column='RATEMTCHRC')  # Field name made lowercase.
    ratedaterc = models.DecimalField(db_column='RATEDATERC', max_digits=9, decimal_places=0)  # Field name made lowercase.
    rateoperrc = models.SmallIntegerField(db_column='RATEOPERRC')  # Field name made lowercase.
    ratercover = models.SmallIntegerField(db_column='RATERCOVER')  # Field name made lowercase.
    rcurndecml = models.SmallIntegerField(db_column='RCURNDECML')  # Field name made lowercase.
    taramount1 = models.DecimalField(db_column='TARAMOUNT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taramount2 = models.DecimalField(db_column='TARAMOUNT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taramount3 = models.DecimalField(db_column='TARAMOUNT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taramount4 = models.DecimalField(db_column='TARAMOUNT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    taramount5 = models.DecimalField(db_column='TARAMOUNT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trinclude1 = models.DecimalField(db_column='TRINCLUDE1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trinclude2 = models.DecimalField(db_column='TRINCLUDE2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trinclude3 = models.DecimalField(db_column='TRINCLUDE3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trinclude4 = models.DecimalField(db_column='TRINCLUDE4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trinclude5 = models.DecimalField(db_column='TRINCLUDE5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trexclude1 = models.DecimalField(db_column='TREXCLUDE1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trexclude2 = models.DecimalField(db_column='TREXCLUDE2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trexclude3 = models.DecimalField(db_column='TREXCLUDE3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trexclude4 = models.DecimalField(db_column='TREXCLUDE4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trexclude5 = models.DecimalField(db_column='TREXCLUDE5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trrecvamt1 = models.DecimalField(db_column='TRRECVAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trrecvamt2 = models.DecimalField(db_column='TRRECVAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trrecvamt3 = models.DecimalField(db_column='TRRECVAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trrecvamt4 = models.DecimalField(db_column='TRRECVAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trrecvamt5 = models.DecimalField(db_column='TRRECVAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trexpsamt1 = models.DecimalField(db_column='TREXPSAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trexpsamt2 = models.DecimalField(db_column='TREXPSAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trexpsamt3 = models.DecimalField(db_column='TREXPSAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trexpsamt4 = models.DecimalField(db_column='TREXPSAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    trexpsamt5 = models.DecimalField(db_column='TREXPSAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tralloamt1 = models.DecimalField(db_column='TRALLOAMT1', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tralloamt2 = models.DecimalField(db_column='TRALLOAMT2', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tralloamt3 = models.DecimalField(db_column='TRALLOAMT3', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tralloamt4 = models.DecimalField(db_column='TRALLOAMT4', max_digits=19, decimal_places=3)  # Field name made lowercase.
    tralloamt5 = models.DecimalField(db_column='TRALLOAMT5', max_digits=19, decimal_places=3)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'POPORH1'
        unique_together = (('vdcode', 'porhseq'), ('vdcode', 'ponumber'),)

class Glpjd(models.Model):
        postingseq = models.DecimalField(db_column='POSTINGSEQ', primary_key=True, max_digits=7,
                                         decimal_places=0)  # Field name made lowercase. The composite primary key (POSTINGSEQ, BATCHNBR, ENTRYNBR, TRANSNBR) found, that is not supported. The first column is selected.
        batchnbr = models.CharField(db_column='BATCHNBR', max_length=6)  # Field name made lowercase.
        entrynbr = models.CharField(db_column='ENTRYNBR', max_length=5)  # Field name made lowercase.
        transnbr = models.DecimalField(db_column='TRANSNBR', max_digits=7,
                                       decimal_places=0)  # Field name made lowercase.
        audtdate = models.DecimalField(db_column='AUDTDATE', max_digits=9,
                                       decimal_places=0)  # Field name made lowercase.
        audttime = models.DecimalField(db_column='AUDTTIME', max_digits=9,
                                       decimal_places=0)  # Field name made lowercase.
        audtuser = models.CharField(db_column='AUDTUSER', max_length=8)  # Field name made lowercase.
        audtorg = models.CharField(db_column='AUDTORG', max_length=6)  # Field name made lowercase.
        jrnldate = models.DecimalField(db_column='JRNLDATE', max_digits=9,
                                       decimal_places=0)  # Field name made lowercase.
        fiscalyr = models.CharField(db_column='FISCALYR', max_length=4)  # Field name made lowercase.
        fiscalperd = models.CharField(db_column='FISCALPERD', max_length=2)  # Field name made lowercase.
        srceledger = models.CharField(db_column='SRCELEDGER', max_length=2)  # Field name made lowercase.
        srcetype = models.CharField(db_column='SRCETYPE', max_length=2)  # Field name made lowercase.
        editallowd = models.SmallIntegerField(db_column='EDITALLOWD')  # Field name made lowercase.
        consolidat = models.SmallIntegerField(db_column='CONSOLIDAT')  # Field name made lowercase.
        acctid = models.CharField(db_column='ACCTID', max_length=45)  # Field name made lowercase.
        companyid = models.CharField(db_column='COMPANYID', max_length=8)  # Field name made lowercase.
        jnldtldesc = models.CharField(db_column='JNLDTLDESC', max_length=60)  # Field name made lowercase.
        jnldtlref = models.CharField(db_column='JNLDTLREF', max_length=60)  # Field name made lowercase.
        transamt = models.DecimalField(db_column='TRANSAMT', max_digits=19,
                                       decimal_places=3)  # Field name made lowercase.
        transqty = models.DecimalField(db_column='TRANSQTY', max_digits=19,
                                       decimal_places=3)  # Field name made lowercase.
        scurndec = models.CharField(db_column='SCURNDEC', max_length=1)  # Field name made lowercase.
        scurnamt = models.DecimalField(db_column='SCURNAMT', max_digits=19,
                                       decimal_places=3)  # Field name made lowercase.
        hcurncode = models.CharField(db_column='HCURNCODE', max_length=3)  # Field name made lowercase.
        ratetype = models.CharField(db_column='RATETYPE', max_length=2)  # Field name made lowercase.
        scurncode = models.CharField(db_column='SCURNCODE', max_length=3)  # Field name made lowercase.
        ratedate = models.DecimalField(db_column='RATEDATE', max_digits=9,
                                       decimal_places=0)  # Field name made lowercase.
        convrate = models.DecimalField(db_column='CONVRATE', max_digits=15,
                                       decimal_places=7)  # Field name made lowercase.
        ratespread = models.DecimalField(db_column='RATESPREAD', max_digits=15,
                                         decimal_places=7)  # Field name made lowercase.
        datemtchcd = models.CharField(db_column='DATEMTCHCD', max_length=1)  # Field name made lowercase.
        rateoper = models.CharField(db_column='RATEOPER', max_length=1)  # Field name made lowercase.
        codestatus = models.SmallIntegerField(db_column='CODESTATUS')  # Field name made lowercase.
        dateentry = models.DecimalField(db_column='DATEENTRY', max_digits=9,
                                        decimal_places=0)  # Field name made lowercase.
        rptamt = models.DecimalField(db_column='RPTAMT', max_digits=19, decimal_places=3)  # Field name made lowercase.
        values = models.IntegerField(db_column='VALUES')  # Field name made lowercase.
        origcomp = models.CharField(db_column='ORIGCOMP', max_length=6)  # Field name made lowercase.
        swreverse = models.SmallIntegerField(db_column='SWREVERSE')  # Field name made lowercase.
        descomp = models.CharField(db_column='DESCOMP', max_length=6)  # Field name made lowercase.
        route = models.SmallIntegerField(db_column='ROUTE')  # Field name made lowercase.
        docdate = models.DecimalField(db_column='DOCDATE', max_digits=9, decimal_places=0)  # Field name made lowercase.
        taxauth = models.CharField(db_column='TAXAUTH', max_length=12)  # Field name made lowercase.
        txaccttype = models.SmallIntegerField(db_column='TXACCTTYPE')  # Field name made lowercase.

        class Meta:
            managed = False
            db_table = 'GLPJD'
            unique_together = (('postingseq', 'batchnbr', 'entrynbr', 'transnbr'),)
