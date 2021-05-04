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

    def clean_room_no(self):
        flag = 0
        try:
            obj = Room.objects.get(room_no = self.cleaned_data['room_no'])
            if obj.empty == True:
                flag = 1
                raise forms.ValidationError("This Room is Empty!")
            return obj.room_no
        except Exception:
            if flag == 0:
                raise forms.ValidationError("Invalid Room!")
            else:
                raise forms.ValidationError("This Room is Empty!")

    def clean_phone(self):
        try:
            obj = Costumer.objects.filter(phone = self.cleaned_data['phone'], active = True)[0]
        except Exception:
            raise forms.ValidationError("No Customer with this phone number!")
        return self.cleaned_data['phone']

    def clean(self):
        try:
            obj = Costumer.objects.filter(room_no = self.cleaned_data['room_no'], phone = self.cleaned_data['phone'], active = True)[0]
        except Exception:
            raise forms.ValidationError("No Customer with this phone number is in this Room!")
        return self.cleaned_data

class BookingForm(forms.ModelForm):
    expected_checkout_time = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Costumer
        fields = fields = ['name', 'phone', 'room_no', 'advance', 'expected_checkout_time', 'package']

    def clean_room_no(self):
        flag = 0
        try:
            obj = Room.objects.get(room_no = self.cleaned_data['room_no'])
            if obj.empty == False:
                flag = 1
                raise forms.ValidationError("This Room is already booked!")
            return obj.room_no
        except Exception:
            if flag == 0:
                raise forms.ValidationError("Invalid Room!")
            else:
                raise forms.ValidationError("This Room is already booked!")