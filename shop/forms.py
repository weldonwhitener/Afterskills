from django import forms as forms

class RegistrationForm(forms.Form):
    username = forms.CharField(label='User Name',max_length=255)
    first_name = forms.CharField(label='First Name',max_length=30)
    last_name = forms.CharField(label='Last Name',max_length=30)
    email = forms.EmailField(label='E-mail',max_length=249)
    password = forms.CharField(label='Password',widget=forms.PasswordInput())


class ContactForm(forms.Form):
    first_name = forms.CharField(label='First Name',max_length=249)
    last_name = forms.CharField(label='Last Name',max_length=249)
    email = forms.EmailField(label='E-mail',max_length=249)
    phone_number = forms.CharField(label='Phone Number',max_length=249)
    message = forms.CharField(label='Message',max_length=249,widget=forms.Textarea(attrs={'rows':4, 'cols':19}))




