from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns=[
    path('',display,name='display'),
    path('insert/',insert,name='insert'),
    path('update/<int:id>/',update,name='update'),
    path('delete/<int:id>/',delete,name='delete')
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)