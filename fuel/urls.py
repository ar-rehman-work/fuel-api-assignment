from django.urls import path
from fuel.views import RegisterView, FuelRouteOptimizerView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('optimize-route/', FuelRouteOptimizerView.as_view(), name='optimize_route'),
]
