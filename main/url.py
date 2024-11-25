from django.urls import path

from .views import (
    AccountListCreateView, AccountDetailView,
    DestinationListCreateView, DestinationDetailView,
    AccountDestinationsView, DataHandlerView,
    home
)

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('accounts/', AccountListCreateView.as_view(), name='account-list-create'),
    path('accounts/<int:pk>/', AccountDetailView.as_view(), name='account-detail'),
    path('destinations/', DestinationListCreateView.as_view(), name='destination-list-create'),
    path('destinations/<int:pk>/', DestinationDetailView.as_view(), name='destination-detail'),
    path('accounts/<uuid:account_id>/destinations/', AccountDestinationsView.as_view(), name='account-destinations'),
    path('server/incoming_data/', DataHandlerView.as_view(), name='data-handler'),
]
