from django.contrib import admin
from django.urls import path, include

from apps.health.views import healthcheck
import apps.vending.views as vending_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("healthcheck/", healthcheck),
    path("slots/", include([
        path("", vending_views.VendingMachineSlotView.as_view()),
    ])),
    path("clients/", include([
        path("", vending_views.ClientView.as_view()),
    ])),
]
