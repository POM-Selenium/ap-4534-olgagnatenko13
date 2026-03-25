from django import forms
from django.utils import timezone
from datetime import timedelta
from book.models import Book


class OrderForm(forms.Form):
    book_id = forms.ModelChoiceField(
        queryset=Book.objects.filter(count__gt=0),
        label='Book',
        empty_label='Select a book',
    )
    plated_end_at = forms.DateTimeField( 
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Planned return date',
    )

    def clean_plated_end_at(self):
        date = self.cleaned_data['plated_end_at']
        max_date = timezone.now() + timedelta(weeks=2)
        if date > max_date:
            raise forms.ValidationError('Return date cannot be more than 2 weeks from today.')
        if date < timezone.now():
            raise forms.ValidationError('Return date cannot be in the past.')
        return date


class OrderFilterForm(forms.Form):
    user_email = forms.CharField(required=False, label='User email')
    date_from = forms.DateField(
        required=False,
        label='From date',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    date_to = forms.DateField(
        required=False,
        label='To date',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )