from unicodedata import name
from  django.urls import path
from .import views
app_name = 'accounts'

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('update/', views.user_update, name= 'update'), #5 baraie inke karbar profile khodesh ro update kone
    path('change/', views.change_password, name= 'change'),# baraie taghir password
    path('login_phone/', views.phone, name= 'phone'),#baraieneshan dadn form mobil
    path('verify/', views.verify, name= 'verify'),#baraie ferestadan karbar be safhe verify

]