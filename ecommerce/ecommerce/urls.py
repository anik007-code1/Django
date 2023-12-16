from django.contrib import admin
from django.urls import path, include

# All the apps should be here in url pattern

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls'))
]
