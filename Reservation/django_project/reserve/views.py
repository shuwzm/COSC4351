from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from .forms import ReservationForm, SearchForm
from django.contrib import messages
from .models import Reservation
from .models import HighTrafficDay
from table.models import Table
from django.contrib.auth.models import User
from django.urls import reverse
from urllib.parse import urlencode
from django.db.models import Q
from itertools import chain
from django.core.mail import send_mail
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from datetime import date, datetime, time, timedelta

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

def CheckHighTrafficDay(date):
    HTDates = HighTrafficDay.objects.all()
    for h in HTDates:
        if date == h.date:
            return True

    return False

def CheckWeekend(date):
    weekno = date.weekday()
    if weekno < 5:
        return False
    else:  # 5 Sat, 6 Sun
        return True


def search_table(request):
    if request.method == 'POST':
        form = SearchForm(request.POST, my_arg='1')
        if form.is_valid():
            #form.save()
            #username = form.cleaned_data.get('username')
            #tableList = Table.objects.all()

            #tableList = list(tableList)
            #ocuppiedSet = Reservation.objects.values_list('table_id', flat=True) 
            #ocuppiedSet = Reservation.objects.values_list('table_id', flat=True)
            #ocuppiedList = list(ocuppiedSet)
            #ocuppiedList = list(chain(tableList,reservationList))
            #tables = Table.objects.exclude(tableId__in = list(Reservation.objects.values_list('table_id', flat=True)))
            custom_number = form.cleaned_data.get('customer_number')
            date = form.cleaned_data.get('date')
            arrive = form.cleaned_data.get('arrive')
            arrive = datetime.strptime(arrive, '%H:%M:%S').time()
            duration = form.cleaned_data.get('duration')



            dt = datetime.combine(date,arrive)
            out = dt + timedelta(hours=int(duration))



            #filter the reservation in the some day
            rev = Reservation.objects.filter(come__date=dt.date())
            # come between exist reservation
            revCome = rev.filter(come__time__lte=dt.time()).filter(out__time__gte=dt.time())
            # leave between exist reservation
            revLeave = rev.filter(come__time__lte=out.time()).filter(out__time__gte=out.time())
            # stay time cover exist reservtaion
            revCover = rev.filter(come__time__gte=dt.time()).filter(out__time__lte=out.time())


            tables = Table.objects.all()
            tables = tables.exclude(pk__in = list(revCome.values_list('table_id', flat=True)))
            tables = tables.exclude(pk__in = list(revLeave.values_list('table_id', flat=True)))
            tables = tables.exclude(pk__in = list(revCover.values_list('table_id', flat=True)))

            if not tables:
                messages.success(request, f'There is no table available for the reservation time, please try other time')
            else:
                table_no_filter_customer = tables
                tables = tables.filter(capacity__gte=custom_number)
                isFound = False
                if not tables:
                    for i in table_no_filter_customer:
                        for j in table_no_filter_customer:
                            if i.id != j.id and i.capacity + j.capacity >= custom_number:
                                print(i.capacity)
                                print(j.capacity)
                                print(custom_number)
                                isFound = True
                                table1 = i
                                table2 = j
                                break
                        if isFound == True:
                            break

                    messages.success(request, f'There is no single table available for the number of customers, but you can select a combination')
                    return render(request, 'reserve/search_result.html', {'form': form, 'table1': table1, 'table2': table2})            
                else:
                    if CheckWeekend(dt.date()):
                        messages.success(request, f'You can select the tables below. \nYou will pay $1 holding fee for weekend')
                    elif CheckHighTrafficDay(dt.date()):
                        messages.success(request, f'You can select the tables below. \nYou will pay $1 holding fee for high traffic day')
                    else:
                        messages.success(request, f'You can select the tables below, without holding fee')

            return render(request, 'reserve/search_result.html', {'form': form, 'tables': tables})
  
    else:
        form = SearchForm(my_arg='0')
    return render(request, 'reserve/search.html', {'form': form})
    


class ReservationCreateView(CreateView):
    #fields = ['first_name', 'last_name', 'phone', 'date', 'arrive', 'duration']

    form_class = ReservationForm
    success_url = 'reservation_list'
    

    def form_valid(self, form):

        table2 = form.cleaned_data['table2nd_id']
        # Reserve a combination
        if table2:
            messages.success(self.request, f'Owner will comfirm your reservation.')
            mail_subject = 'Reservation Comfirmation for Owener'
            message = "There is a reservation to comfirm"
            superusers_emails = list(User.objects.filter(is_superuser=True).values_list('email', flat=True))
            
            #print(superusers_emails)

            to_email = superusers_emails
            send_mail(mail_subject, message, 'youremail', [to_email[0]])
            #return HttpResponse('Please waif for owner comfirmation')

        if self.request.user.is_anonymous:
            pass
        else:
            form.instance.user_id = self.request.user
        messages.success(self.request, f'Congrats, You have successfully reserve a Table.')
        return super().form_valid(form)

    # def form_valid(self, form):
    #     return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse('table_search')

    # #initial = {"first_name": request.}
    # def get_initial(self):
    #     return {
    #          'duration': self.request.session['duration']
    #     }

    #initial = {"first_name": request.}
    def get_initial(self):
        date = self.request.GET['date']
        arrive = self.request.GET['arrive']
    
        duration = self.request.GET['duration']
        dt = datetime.combine(datetime.strptime(date, '%Y-%m-%d').date(),datetime.strptime(arrive, '%H:%M:%S').time())
        out = dt + timedelta(hours=int(duration))
        if self.request.GET.get('table_id'):
            table_id = self.request.GET['table_id']

        if self.request.GET.get('table1_id'):
            table_id = self.request.GET['table1_id']
            table2_id = self.request.GET['table2_id']
        else:
            table2_id = None
        
        if self.request.user.is_anonymous:
            last_name = ''
            first_name = ''
            phone = ''
        else:
            last_name = self.request.user.last_name
            first_name = self.request.user.first_name
            phone = self.request.user.profile.phone

        return {
             'duration': self.request.GET['duration'],
             'date': self.request.GET['date'],
             'arrive': self.request.GET['arrive'],
             'customer_number':self.request.GET['customer_number'],
             #'table_id':self.request.GET['table_id'],
             'come':dt,
             'out':out,
             'table_id':table_id,
             'table2nd_id':table2_id,
             'last_name':last_name,
             'first_name':first_name,
             'phone':phone,
             #'is_active':is_active
        }

class TableListView(ListView):
    model = Table
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

class ReservationListView(ListView):
    model = Reservation
    template_name = 'reserve/reservation_list.html'  # <app>/<model>_<viewtype>.html

    def get_queryset(self):
        if self.request.user.is_anonymous:
            messages.warning(self.request, f'Only registered user can see the reservation history.\n If you want cancel, please all the restaurant.')
        else:
            #user = get_object_or_404(User, username=self.kwargs.get('username'))
            reservations = Reservation.objects.filter(user_id=self.request.user)
            if not reservations:
                messages.warning(self.request, f'There is no reservations for you.')
            else:
                msg = 'You have points: '+str(reservations.count())
                messages.success(self.request, msg)
            return reservations
    context_object_name = 'reservations'


class ReservationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reservation
    success_url = '/'

    def test_func(self):
        rev = self.get_object()
        if self.request.user == rev.user_id:
            return True
        return False
    
class ReservationDetailView(DetailView):
    model = Reservation