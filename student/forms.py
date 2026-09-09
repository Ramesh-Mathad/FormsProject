from django import forms
from .models import Student


class StudentForm(forms.Form):
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'accept': 'image/*',
                'class': 'form-control',
            }
        )
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'e.g. Ramesh Mathad',
                'class': 'form-control',
            }
        )
    )
    roll_no = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'e.g. 24',
                'class': 'form-control',
            }
        )
    )
    course = forms.ChoiceField(
        choices=Student.COURSES,
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'name@gmail.com',
                'class': 'form-control',
            }
        )
    )
    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Street, city, state, PIN code',
                'class': 'form-control',
                'rows': 3,
            }
        )
    )

    def clean_name(self):
        self.name = self.cleaned_data.get('name')
        if len(self.name) <= 3:
            raise forms.ValidationError('Name should be more than 3 chr')
        return self.name

    def clean_email(self):
        self.email = self.cleaned_data.get('email')
        if not self.email.endswith('gmail.com'):
            raise forms.ValidationError('only gmails are accepted')
        return self.email

    def clean_roll_no(self):
        self.roll_no = self.cleaned_data.get('roll_no')
        if self.roll_no < 1:
            raise forms.ValidationError("Roll no can not be zero")
        return self.roll_no
