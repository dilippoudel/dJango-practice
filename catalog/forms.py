from django import forms
import datetime


from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        if data < datetime.date.today():
            raise ValidationError(_('Invalid Date -renewal in past'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks ahead'))

        return data


# form practice
class NameForm(forms.Form):
    your_name = forms.CharField(label='Your Name', max_length=100)


#step 1 Registration form
class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control','style': 'max-width: 300px;'}),label="Firstname")
    last_name = forms.CharField(label="Lastname", max_length=50, widget=forms.TextInput(attrs={'class':'form-control','style': 'max-width: 300px;'}))
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'form-control','style': 'max-width: 300px;'}))
    username = forms.CharField(label="Username", min_length=6, max_length=12, widget=forms.TextInput(attrs={'class':'form-control','style': 'max-width: 300px;'}))
    password = forms.CharField(label="Password", widget=forms.TextInput(attrs={'class':'form-control','style': 'max-width: 300px;'}))
    confirm_password = forms.CharField(label="ConfirmCharField", widget=forms.TextInput(attrs={'class':'form-control','style': 'max-width: 300px;'}))






#Forms for Creating new Authors
# step 1: Define all the filed to render template
class AuthorRegistration(forms.Form):
    first_name = forms.CharField(label="First Name",max_length=50,help_text='Enter Your First Name')
    last_name = forms.CharField(label="Last Name",max_length=50, help_text='Enter Your Last Name')
    date_of_birth = forms.DateField(label="Date Of Birth",help_text='Enter the date atleast earlier 20', required=False)
    date_of_dead = forms.DateField(label="Date Of Dead",help_text='Enter the date after birth date', required=False)


    """
    2025
    date of birth 20 years old
    date of death afte > 20 years
    // publixhed date after date age
    
    """


class ContactForm(forms.Form):
    name = forms.CharField(label='Enter Your Full name', max_length=50)
    email = forms.EmailField(label='Enter Your Email Address')
    message = forms.CharField(label='Enter the message', help_text="Describe your case, No more than 500  Chars", max_length=500)
    contact = forms.CharField(label='Contact no: ', max_length=10, help_text="Enter contact Number (Only 10 digits)")
