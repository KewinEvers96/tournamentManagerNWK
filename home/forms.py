from django import forms
from django.core.validators import MinLengthValidator

class RegistrationForm(forms.Form):
    # Competitors data
    name = forms.CharField(max_length= 128)
    lastname = forms.CharField(max_length= 128)
    # user data
    username = forms.CharField(label= 'Username',max_length= 128)
    email = forms.CharField(label= 'Email', max_length= 128, widget= forms.EmailInput())
    emailConfirmation = forms.CharField(label= 'Email Confirmation', max_length=128, widget= forms.EmailInput())
    password = forms.CharField(label= 'Password', min_length= 8, widget= forms.PasswordInput())
    passwordConfirmation = forms.CharField(label= 'Password Confirmation', min_length= 8, widget= forms.PasswordInput())
    
    
    def clean(self):
        super().clean()
        email = self.cleaned_data.get("email")
        emailConf = self.cleaned_data.get("emailConfirmation")
        
        password = self.cleaned_data.get('password')
        passwordConf = self.cleaned_data.get('passwordConfirmation')
        
        if email and emailConf and email != emailConf:
            self._errors['emailConfirmation'] = self.error_class(['Emails do not match.'])
            del self.cleaned_data['emailConfirmation']
        
        if password and passwordConf and password != passwordConf:
            self._errors['passwordConfirmation'] = self.error_class(['Passwords did not match'])
            del self.cleaned_data['passwordConfirmation']

        return self.cleaned_data
