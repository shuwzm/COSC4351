from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from .views import (
    TableListView,
    TableDetailView,
    TableCreateView,
    TableUpdateView,
    TableDeleteView
)
from . import views

urlpatterns = [
    path('', TableListView.as_view(), name='table-home'),
    path('<int:pk>/', TableDetailView.as_view(), name='table-detail'),
    path('new/', staff_member_required(TableCreateView.as_view()), name='table-create'),
    path('<int:pk>/update/', TableUpdateView.as_view(), name='table-update'),
    path('<int:pk>/delete/', TableDeleteView.as_view(), name='table-delete'),
    path('about/', views.about, name='blog-about'),
]
