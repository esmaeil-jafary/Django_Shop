from django.urls import path, re_path
from .import views
app_name = 'home'
urlpatterns = [
    path('',views.home, name='home'),
    path('product/', views.all_product, name = 'product'),
    path('detail/<int:id>/', views.product_detail, name='detail'), # baraie safhe joziat mahsol. va  ba <id> migoem ke hamrah in url id 
    # ham miaiad va noee id ra ham moshakhas mikonim ke integer as
    # path('category/<int:id>/', views.all_product, name='category'),# vaghti roie oic yek category click kardim marabebarad 
    # be safe mahsolat . ama faghat mahsolat an daste ra neshan dahad. va views jadid neminevisim va az views all-product estefade m

    # alan url bala ke bevasile id kar mikard ra bevasile slug migoeim kar konad.
    # path('category/<slug:slug>/', views.all_product, name='category'),
    #vaghti ma az name daste bandi haie farsi estefadeh konim be ma error midahad dar url  haie ke ba slug misazim ya id:
    # pas baiad az re_path estefade konim va baiad az re_path(rejects) estefade konim vaki ma kalak mizanim va noesh ra nemigoeim
    # ke slug ast:
    # path('category/<slug>/', views.all_product, name='category'),
    
    # alan mikhahim dar url alave bar slug id ra ham dar url neshan dahad
    path('category/<slug>/<int:id>/', views.all_product, name='category'),


]  