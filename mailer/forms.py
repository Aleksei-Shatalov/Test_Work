from django import forms
from .models import Mailing, Subscriber

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['subject', 'body', 'subscribers', 'scheduled_time']
        widgets = {
            'subscribers': forms.CheckboxSelectMultiple(),
            'scheduled_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }
    scheduled_time = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'id': 'scheduled_time',
            'name': 'scheduled_time'
        })
    )

