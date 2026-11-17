from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Order


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)
    first_name = forms.CharField(label="Імʼя", max_length=50)

    class Meta:
        model = User
        fields = ("username", "first_name", "email")


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("full_name", "phone", "email", "delivery", "city", "address", "payment", "comment")
        widgets = {
            "delivery": forms.RadioSelect,
            "payment": forms.RadioSelect,
            "comment": forms.Textarea(attrs={"rows": 3}),
            "phone": forms.TextInput(attrs={"type": "tel", "placeholder": "+380"}),
        }

    def clean_phone(self):
        phone = "".join(c for c in self.cleaned_data["phone"] if c.isdigit() or c == "+")
        if len(phone.lstrip("+")) < 10:
            raise forms.ValidationError("Вкажіть коректний номер телефону")
        return phone

    def clean(self):
        data = super().clean()
        if data.get("delivery") != Order.Delivery.PICKUP:
            for f in ("city", "address"):
                if not data.get(f):
                    self.add_error(f, "Обовʼязково для доставки")
        return data
