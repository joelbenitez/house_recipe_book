from datetime import datetime

from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


SITES = [
    ("BRU1", "Brussels"),
    ("FR5", "Frankfurt"),
    ("LA1", "Los Angeles"),
    ("NY1", "New York"),
    ("SY3", "Sydney"),
]


class CustomerInterconnectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

    customer_name = forms.CharField(
        label="Company name",
        max_length=100,
        help_text="Your company's name",
        widget=forms.TextInput(attrs={"placeholder": "A super cool company"}),
    )
    asn = forms.IntegerField(
        label="Autonomous System Number",
        help_text="Your ASN (an integer)",
        widget=forms.NumberInput(attrs={"placeholder": 12345, "max": 4294967296}),
    )
    contact = forms.EmailField(
        label="Contact email",
        required=False,
        help_text="Your email address",
        widget=forms.TextInput(attrs={"placeholder": "john.doe@example.com"}),
    )

    site = forms.ChoiceField(
        choices=SITES, label="Location", help_text="Where we are going to interconnect"
    )

    date_selection = forms.DateField(
        label="Date of service",
        help_text="The initial date of service",
        widget=forms.DateInput(attrs={"type": "date", "min": datetime.now().date()}),
    )

    notes = forms.CharField(
        label="Additional notes or feedback (Optional)",
        required=False,
        help_text="Any additional comments you'd like to provide",
        widget=forms.Textarea(attrs={"rows": 5}),
    )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]
