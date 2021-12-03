from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Table

def home(request):
    context = {
        'tables':Table.objects.all()
    }
    return render(request, 'table/home.html', context)

class TableListView(ListView):
    model = Table
    template_name = 'table/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'tables'
    #ordering = ['-date_posted']

class TableDetailView(DetailView):
    model = Table


class TableCreateView(LoginRequiredMixin, CreateView):
#class TableCreateView(CreateView):
    model = Table
    fields = ['tableId', 'capacity', 'isOutdoor', 'isBooth']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TableUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Table
    fields = ['tableId', 'capacity', 'isOutdoor', 'isBooth']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     return False


class TableDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Table
    success_url = '/'

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})