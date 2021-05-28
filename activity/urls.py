from django.urls import path
from activity.views import *


urlpatterns = [
    path('', index, name='home'),
    path('syncs/', syncs, name='syncs'),
    path('<int:article_id>/', one_article, name='articles'),
    path('parameters/', parameters, name='parameters'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('entering-device-data/', entering_device_data_view, name='entering-device-data'),
    path('logout/', user_logout, name='logout'),
    path('analysis/', analysis, name='analysis')
]
