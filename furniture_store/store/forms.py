from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(
        label="Imię",
        required=True,
        help_text=""
    )
    last_name = forms.CharField(
        label="Nazwisko",
        required=True,
        help_text=""
    )
    password1 = forms.CharField(
        label="Hasło",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=""
    )
    password2 = forms.CharField(
        label="Powtórz hasło",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=""
    )
    username = forms.CharField(
        label="Nazwa użytkownika",
        help_text=""
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name" , "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class ContactForm(forms.Form):
    name = forms.CharField(required=True, label='Imię i nazwisko')
    from_email = forms.EmailField(required=True, label='Email')
    subject = forms.CharField(required=True, label='Temat')
    message = forms.CharField(widget=forms.Textarea, required=True, label="Treść wiadomości")
