from django import forms
from finance.models import *

class TransactionForm(forms.ModelForm):
    
    class Meta:
        model = Transaction
        fields = '__all__'

    