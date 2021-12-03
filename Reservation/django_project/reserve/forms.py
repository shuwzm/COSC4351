from django import forms
from django.contrib.auth.models import User
#from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Reservation

from datetime import date, datetime, time, timedelta
from django.core import validators
from dateutil.relativedelta import relativedelta


DURATION_CHOICES = [(1, '1 hour'), (2, '2 hour'), (3, '3 hour'), (4, '4 hour'), (5, '5 hour'), (6, '6 hour')]

BIRTH_YEAR_CHOICES = ['1980', '1981', '1982']
FAVORITE_COLORS_CHOICES = [
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
]

TIME_CHOICES = (('10:00:00', '10 AM'),
                ('11:00:00', '11 AM'),
                ('12:00:00', 'Noon'),
                ('13:00:00', '01 PM'),
                ('14:00:00', '02 PM'),
                ('15:00:00', '03 PM'),
                ('16:00:00', '04 PM'),
                ('17:00:00', '05 PM'),
                ('18:00:00', '06 PM'),
                ('19:00:00', '07 PM'),
                ('20:00:00', '08 PM'),
                ('21:00:00', '09 PM') )

def validate_date(date):
    if date < datetime.now().date():
        raise validators.ValidationError("Date cannot be in the past")

class DateInput(forms.DateInput):
    input_type = "date"
    
class TimeInput(forms.TimeInput):
    input_type = "time"



class SearchForm(forms.Form):
    
    # name = forms.CharField()
    # message = forms.CharField(widget=forms.Textarea)

    # birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    # favorite_colors = forms.MultipleChoiceField(
    #     required=False,
    #     widget=forms.Select,
    #     choices=FAVORITE_COLORS_CHOICES,
    # )
    duration = forms.ChoiceField(required=False, widget=forms.Select, choices=DURATION_CHOICES)
    date = forms.DateField(widget=DateInput(attrs={'min': datetime.today().strftime('%Y-%m-%d'), 'max': (datetime.today()+relativedelta(months=1)).strftime('%Y-%m-%d')}))
    #date = forms.DateField(widget=DateInput, validators=[validate_date])
    #date = forms.DateField(widget=forms.DateField(attrs={'min': '2020-01-01', 'max': '2021-01-01'}))
    #arrive = forms.TimeField(widget=TimeInput(attrs={'min': "10:30:00", 'max': "21:00:00"}))
    arrive = forms.ChoiceField(required=True, widget=forms.Select, choices=TIME_CHOICES)
    customer_number = forms.IntegerField()
    
    def __init__(self, *args, **kwargs):
        my_arg = kwargs.pop('my_arg')
        super().__init__(*args, **kwargs)
        #self.fields["arrive"].widget = TimeInput()
        #self.fields['date'].widget.attrs.update({'min': '2020-01-01', 'max': '2021-01-01'})
        if my_arg == '1':
            self.fields['arrive'].widget.attrs['readonly'] = True
            self.fields['duration'].widget.attrs['readonly'] = True
            self.fields['date'].widget.attrs['readonly'] = True
            self.fields['customer_number'].widget.attrs['readonly'] = True
        # self.fields["end"].widget = DateInput()
        # self.fields["opening"].widget = TimeInput()
        # self.fields["closing"].widget = TimeInput()
        # self.fields["vernissage"].widget = DateTimeInput()
        # self.fields["vernissage"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]
        # self.fields["finissage"].widget = DateTimeInput()
        # self.fields["finissage"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name', 'phone', 'date', 'arrive', 'duration', 'customer_number', 'table_id', 'table2nd_id', 'come', 'out']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["arrive"].widget = TimeInput()
        self.fields["date"].widget = DateInput()
        self.fields['table2nd_id'].required = False

        self.fields['arrive'].widget.attrs['readonly'] = True
        self.fields['duration'].widget.attrs['readonly'] = True
        self.fields['date'].widget.attrs['readonly'] = True
        self.fields['customer_number'].widget.attrs['readonly'] = True
        self.fields['table_id'].widget.attrs['readonly'] = True
        self.fields['table2nd_id'].widget.attrs['readonly'] = True
        self.fields['come'].widget.attrs['readonly'] = True
        self.fields['out'].widget.attrs['readonly'] = True
        self.fields['arrive'].widget = forms.HiddenInput()
        self.fields['duration'].widget = forms.HiddenInput()
        # self.fields["opening"].widget = TimeInput()
        # self.fields["closing"].widget = TimeInput()
        # self.fields["vernissage"].widget = DateTimeInput()
        # self.fields["vernissage"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]
        # self.fields["finissage"].widget = DateTimeInput()
        # self.fields["finissage"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]
