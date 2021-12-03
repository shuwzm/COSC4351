from django.urls import path
from . import views as reserve_views

urlpatterns = [
    path('', reserve_views.search_table, name='table-search'),
    path('new', reserve_views.ReservationCreateView.as_view(template_name='reserve/reservation.html'), name='reservation-create'),
    path('reservation_list', reserve_views.ReservationListView.as_view(), name='reservation-list'),
    path('reservation/<int:pk>/cancel/', reserve_views.ReservationDeleteView.as_view(), name='reservation-cancel'),
    path('reservation/<int:pk>/', reserve_views.ReservationDetailView.as_view(), name='reservation-detail'),
    
]
