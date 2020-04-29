from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
               'id': 'message-text',
                'required': True,
                'placeholder': 'Say something...'
            }),
        }

