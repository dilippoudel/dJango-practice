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




    """def clean_registration_form(self):
        if self.password != self.confirm_password:
            raise ValidationError(_(f"password didn't match"))
        return self
        """



#Forms for Editing
