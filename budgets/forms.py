from io import BytesIO

import pyotp
import qrcode
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.forms import ModelForm, forms, inlineformset_factory
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from budgets.models import BudgetLines, Users, BudgetComments, BudgetStatus


class BudgetEditForm(ModelForm):
    class Meta:
        model = BudgetLines
        exclude = [ 'last_updated', 'last_updated_by']


class BudgetStatusForm(ModelForm):
    class Meta:
        model = BudgetStatus
        fields = ['is_active','is_complete','comment','budget_set']

class UserCreate(ModelForm):
    class Meta:
        model = Users
        fields = ['username', 'password', 'first_name', 'last_name', 'department', 'role', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        otp_base32 = pyotp.random_base32()
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")
        otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
            name=email.lower(), issuer_name="mupumaDev"
        )
        stream = BytesIO()
        image = qrcode.make(f"{otp_auth_url}")
        image.save(stream)
        user.otp_base32 = otp_base32
        user.otp_auth_url = otp_auth_url
        user.qr_code = ContentFile(
            stream.getvalue(), name=f"qr{get_random_string(10)}.png"
        )
        user.email = email
        user.password = make_password(password)
        user.save()

        return user
