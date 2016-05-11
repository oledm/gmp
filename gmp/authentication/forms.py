from django import forms
from django.core.exceptions import ValidationError
from djng.forms.fields import FloatField
from djng.forms import NgModelFormMixin, NgForm, NgModelForm
from djng.styling.bootstrap3.forms import Bootstrap3FormMixin
from django.forms import inlineformset_factory


from .models import Employee
from gmp.departments.models import Department

class ContactForm(Bootstrap3FormMixin, NgModelFormMixin, NgModelForm):
    class Meta:
         model = Employee
         fields = '__all__'

class DepartmentForm(Bootstrap3FormMixin, NgModelFormMixin, NgModelForm):
    class Meta:
         model = Department
         fields = '__all__'

DepartmentFormSet = inlineformset_factory(Department, Employee, fields='__all__')


def validate_password(value):
    # Just for demo. Do not validate passwords like this!
    if value != 'secret':
        raise ValidationError('The password is wrong.')
#class ContactForm(NgModelFormMixin, NgForm, Bootstrap3Form):
#    #CONTINENT_CHOICES = (('am', 'America'), ('eu', 'Europe'), ('as', 'Asia'), ('af', 'Africa'),
#    #                     ('au', 'Australia'), ('oc', 'Oceania'), ('an', 'Antartica'),)
#    #TRAVELLING_BY = (('foot', 'Foot'), ('bike', 'Bike'), ('mc', 'Motorcycle'), ('car', 'Car'),
#    #                 ('public', 'Public Transportation'), ('train', 'Train'), ('air', 'Airplane'),)
#    #NOTIFY_BY = (('email', 'EMail'), ('phone', 'Phone'), ('sms', 'SMS'), ('postal', 'Postcard'),)
#
#    #first_name = forms.CharField(label='First name', min_length=3, max_length=20)
#
#    #last_name = forms.RegexField(r'^[A-Z][a-z -]?', label='Last name',
#    #    error_messages={'invalid': 'Last names shall start in upper case'})
#    #sex = forms.ChoiceField(choices=(('m', 'Male'), ('f', 'Female')),
#    #    widget=forms.RadioSelect, error_messages={'invalid_choice': 'Please select your sex'})
#    subject = forms.CharField()
