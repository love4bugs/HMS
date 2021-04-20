from django import forms
from .models import *
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ['name', 'phone', 'room_no']


class BookingForm(forms.ModelForm):
    expected_checkout_time = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Costumer
        fields = fields = ['name', 'phone', 'room_no', 'advance', 'expected_checkout_time', 'package']