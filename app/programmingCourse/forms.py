from django import forms

class CodeAnswerForm(forms.Form):
    answer = forms.CharField(
        label='Your Answer',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your Python code here...',
            'class': 'form-control'
        })
    )
