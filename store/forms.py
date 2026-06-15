from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .patterns import PaymentStrategyFactory, ShippingStrategyFactory


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label='Nome', max_length=40, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']


class CheckoutForm(forms.Form):
    full_name = forms.CharField(label='Nome completo', max_length=120)
    address = forms.CharField(label='Endereço de entrega', max_length=220)
    payment_method = forms.ChoiceField(label='Pagamento', choices=PaymentStrategyFactory.choices())
    shipping_method = forms.ChoiceField(label='Entrega', choices=ShippingStrategyFactory.choices())
    reward_code = forms.CharField(label='Cupom GlowClub', max_length=30, required=False)
