from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include('vehicles.urls')),
    path('dashboard/',include('vehicles.urls')),
    path('', RedirectView.as_view(url='/dashboard/')),
]
