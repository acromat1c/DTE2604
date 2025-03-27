from django import forms
from .models import Group

class CodeAnswerForm(forms.Form):
    answer = forms.CharField(
        label='Your Answer',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your Python code here...',
            'class': 'form-control'
        })
    )

class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['groupName', 'description', 'image', 'is_private']
        widgets = {
            'groupName': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_private': forms.CheckboxInput(),
        }

class GroupEditForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['groupName', 'description', 'image', 'is_private']
        widgets = {
            'groupName': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_private': forms.CheckboxInput(),
        }