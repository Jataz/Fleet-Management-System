from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import include, path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include('vehicles.urls')),
    path('',include('vehicles.urls')),
    path('', RedirectView.as_view(url='/login/')),

]
