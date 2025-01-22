from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(('User_Master.urls','user'))),
    path('guide/',include(('guide.urls','guide'))),
    path('med/',include(('med.urls','med'))),
    path('Chemist_Master/',include(('Chemist_Master.urls','chemist'))),
]
