from django.urls import path
from .views import (
    CoolestDistrictsView,
    TravelAdviceView,
)

urlpatterns = [
    path('coolest-district/', CoolestDistrictsView.as_view(), name='coolest-district'),
    path('trave-advice/<int:from_district>/<int:to_district>/<str:travel_date>/', TravelAdviceView.as_view(), name='travel-advice'),
]
