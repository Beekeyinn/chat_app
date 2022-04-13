from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate


from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_('Confirm Password'),
        widget=forms.PasswordInput, validators=[validate_password, ])

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.Meta.model.objects.get(email=email).exists():
            raise ValidationError("Email already exists.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password must match")
        return password2

    def save(self, commit=True):
        user = super(User, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password2'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password',
                  'is_active', 'is_admin',)


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput,
        help_text="Password must be of at least 6 characters.")
    password2 = forms.CharField(
        label="confirm Password", widget=forms.PasswordInput,
        validators=[validate_password, ])

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.Meta.model.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 6:
            raise ValidationError(
                "Password must be of at least 6 characters.")
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 or not password2:
            raise ValidationError("Password is required.")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password must match")
        return password2


class LoginForm(forms.Form):
    email = forms.CharField(label=_("Email"), widget=forms.TextInput)
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            return email
        raise ValidationError('Email doesnot exist. please register')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        user = authenticate(
            self.request, email=email, password=password)
        if user is None:
            raise ValidationError("Invalid credentials")
        return password
