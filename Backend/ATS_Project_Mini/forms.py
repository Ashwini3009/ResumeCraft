from django import forms
from .models import UploadedFile
from .models import User


#Upload File form handeling
class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('file',)



#signup Forms Handeling
class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'contact_number', 'dob', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password do not match.")

        return cleaned_data