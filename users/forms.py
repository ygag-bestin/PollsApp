from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, \
    PasswordResetForm
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import gettext as _

User = get_user_model()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False,
                                 help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False,
                                help_text='Optional')
    email = forms.CharField(max_length=254, validators=[EmailValidator])

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("please verify you Account"),
                code='inactive',
            )


class CustomEmailValidation(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError("Email is not registered!")
        elif User.objects.filter(email=email, is_active=False).exists():
            raise forms.ValidationError(
                _("Please verify you Account"),
                code='inactive',)
        return email
