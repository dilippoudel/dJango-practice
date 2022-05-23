from django import forms
import datetime
from .models import Book, Author, BookInstance, Genre, Langauge, Contact

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


# custom validation for matching password and email check
def validate_email(value):
    if "@gmail.com" in value:
        return value
    else:
        raise ValidationError("Please submit the gmail address")
    return value

    """def is_password_match(value):
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['confirm_password']
        if password == repeat_password:
            return password, repeat_password
        else:
            raise ValidationError("Your password didn't match")
        return password, repeat_password"""


# step 1 Registration form
class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                 label="Firstname")
    last_name = forms.CharField(label="Lastname", max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control'}),
                             validators=[validate_email])
    username = forms.CharField(label="Username", min_length=6, max_length=12,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label="Confirm password",
                                       widget=forms.TextInput(attrs={'class': 'form-control'}))


# Forms for Creating new Authors
# step 1: Define all the filed to render template
class AuthorRegistration(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=50, help_text='Enter Your First Name')
    last_name = forms.CharField(label="Last Name", max_length=50, help_text='Enter Your Last Name')
    date_of_birth = forms.DateField(label="Date Of Birth", help_text='Enter the date atleast earlier 20',
                                    required=False)
    date_of_dead = forms.DateField(label="Date Of Dead", help_text='Enter the date after birth date', required=False)

    """
    2025
    date of birth 20 years old
    date of death afte > 20 years
    // publixhed date after date age
    
    """


class ContactForm(forms.Form):
    name = forms.CharField(label='Enter Your Full name', max_length=50)
    email = forms.EmailField(label='Enter Your Email Address')
    message = forms.CharField(label='Enter the message', help_text="Describe your case, No more than 500  Chars",
                              max_length=500)
    contact = forms.CharField(label='Contact no: ', max_length=10, help_text="Enter contact Number (Only 10 digits)")


class CreatingBookAndEditing(forms.Form):
    allAuthors = Author.objects.all()
    allGenres = Genre.objects.all()
    allLanguages = Langauge.objects.all()
    CHOICES_AUTHORS = ()
    CHOICES_LANGUAGES = ()
    CHOICES_GENRES = ()
    for x in range(len(allAuthors)):
        CHOICES_AUTHORS = CHOICES_AUTHORS + (
            (f'{allAuthors[x].id}', f'{allAuthors[x].first_name} {allAuthors[x].last_name}'),
        )
    for x in range(len(allGenres)):
        CHOICES_GENRES = CHOICES_GENRES + (
            (f'{allGenres[x].id}', f'{allGenres[x].name}'),
        )
    for x in range(len(allLanguages)):
        CHOICES_LANGUAGES = CHOICES_LANGUAGES + (
            (f'{allLanguages[x].id}', f'{allLanguages[x].name}'),
        )

    title = forms.CharField(label='Book Title', max_length=50)
    author = forms.ChoiceField(choices=CHOICES_AUTHORS, label='Select author')
    summary = forms.CharField(max_length=500, label='Summary', required=True,
                              widget=forms.Textarea(attrs={'name': 'body', 'rows': '10', 'cols': '30'}))
    isbn = forms.CharField(max_length=13, label='ISBN', required=True)
    genre = forms.ChoiceField(choices=CHOICES_GENRES, label='Select Genre')
    language = forms.ChoiceField(choices=CHOICES_LANGUAGES, label='Select Language')
