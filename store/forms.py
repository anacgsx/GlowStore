from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CheckoutForm(forms.Form):
    full_name = forms.CharField(label='Nome completo', max_length=120)
    address = forms.CharField(label='Endereço de entrega', max_length=220)
    payment_method = forms.ChoiceField(
        label='Pagamento',
        choices=[('pix', 'Pix - 5% off'), ('credit', 'Cartão de crédito'), ('club', 'Glow Club - 10% off')],
    )
    shipping_method = forms.ChoiceField(
        label='Entrega',
        choices=[('standard', 'Padrão'), ('express', 'Expressa')],
    )
