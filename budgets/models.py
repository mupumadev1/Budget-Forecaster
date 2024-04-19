from datetime import datetime, timezone

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


class Department(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)


class Accounts(models.Model):
    acctid = models.CharField(db_column='ACCTID', primary_key=True, max_length=45,
                              )
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
    history = HistoricalRecords()


class Users(AbstractUser, PermissionsMixin):
    role = models.CharField(max_length=255, choices=ROLE, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    otpauth_url = models.CharField(max_length=225, blank=True, null=True)
    otp_base32 = models.CharField(max_length=255, null=True, blank=True)
    qr_code = models.ImageField(upload_to="qrcode/", blank=True, null=True)
    login_otp = models.CharField(max_length=255, null=True, blank=True)
    login_otp_used = models.BooleanField(default=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    history = HistoricalRecords()

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


class BudgetAssumptions(models.Model):
    factor = models.CharField(max_length=255, null=True)
    rate = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    history = HistoricalRecords()


class BudgetTotals(models.Model):
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default=1)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.CharField(max_length=4, default='2024')
    total = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period1 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period2 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period3 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period4 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period5 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period6 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period7 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period8 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period9 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period10 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period11 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period12 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    budget_set = models.CharField(max_length=255, choices=SET_TYPE)
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    posted = models.BooleanField(default=False)
    exchange_rate = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    history = HistoricalRecords()

    def calculate_quarter_sums(self):
        # Calculate the sum of each quarter based on the period fields
        q1 = self.period1 + self.period2 + self.period3
        q2 = self.period4 + self.period5 + self.period6
        q3 = self.period7 + self.period8 + self.period9
        q4 = self.period10 + self.period11 + self.period12

        # Update the instance with the calculated quarter sums
        self.Q1 = q1
        self.Q2 = q2
        self.Q3 = q3
        self.Q4 = q4

        # Save the instance to persist the changes
        self.save()

    def calculate_half_sums(self):
        # Calculate the sum of each quarter based on the period fields
        h1 = self.period1 + self.period2 + self.period3 + self.period4 + self.period5 + self.period6
        h2 = self.period7 + self.period8 + self.period9 + self.period10 + self.period11 + self.period12

        # Update the instance with the calculated quarter sums
        self.H1 = h1
        self.H2 = h2

        # Save the instance to persist the changes
        self.save()


class ChangeLog(models.Model):
    flag = models.BooleanField(default=False)
    department = models.CharField(max_length=255, null=True)
    budget_set = models.CharField(max_length=255, null=True)


class BudgetLinesLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    item_description = models.CharField(max_length=255, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    department = models.CharField(max_length=255, null=True)
    budget_set = models.CharField(max_length=255, null=True)


# Create your models here.
class BudgetLines(models.Model):
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    item_description = models.CharField(max_length=255, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.CharField(max_length=4, default='2024')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default=1)
    rate = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    usage = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    staff = models.IntegerField(null=True)
    factor = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period1 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period2 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period3 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period4 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period5 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period6 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period7 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period8 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period9 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period10 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period11 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    period12 = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    budget_set = models.CharField(max_length=255, choices=SET_TYPE)
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    posted = models.BooleanField(default=False)
    exchange_rate = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    history = HistoricalRecords()


class BudgetStatus(models.Model):
    budget_set = models.CharField(max_length=255, choices=SET_TYPE)
    year = models.CharField(max_length=4, default='2024')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=True)
    updated_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255, null=True, blank=True)
    history = HistoricalRecords()


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
