from django import forms
from app.models import *

class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = '__all__'
        exclude = ['agent','date_birth','company','created_at']

class SippingForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = '__all__'
        exclude = ['agent','date_birth','company','created_at']