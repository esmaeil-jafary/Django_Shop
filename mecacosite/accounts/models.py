from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
# baraie ijad safhe karbari profile
# yani har karbar ke login kard safhe marbot be an ra neshan bedeh ke baiad az model User django komak begirim

#baraie format fhone
from phone_field import PhoneField

# baraie fhon az integerfield estefadeh kardim vali 0 ra neshan nemidahad va baiad 
# yek package be nam django-phone-field ke braie neshandadn 0 va save shodan dakhel DB ra darad
#va ba dastor pip install django-phone-field nasb mikonim. va bade miravim setting va install_app va ezafe mikonim
class Profile(models.Model):
    # har karbar ke login kard safhe marbot be an ra neshan bedeh
    user = models.OneToOneField(User, on_delete=models.CASCADE) #har karbar yek safhe darad pas yek be yek ast. 
    #migoeim ba class user rabete darad
    # phone = PhoneField(null=True, blank=True)#null va blank yani afar karbar meghdari vared bakard khata

    #phone ra fstring ham mitavanim moshkelash ra hal konim va nitavanim az phone field estefade nakonim
    phone = models.IntegerField(null=True, blank=True)
    #nadeh va profile an ra besaz
    address = models.CharField(max_length=200 , null=True, blank= True)

# baraie namayesh nam karbar dar fild haie safhe profile
    def __str__(self):
        return self.user.username # az object user ba klid yek be yek be class User dastresi darim

#--------------------------------------------------------------------------------------------------------------

# az signal zamani estefade mokonim ke agar etefaghi dar models ma oftad az an bakhabar beshavim va yek signal befrastad
# 7 ta signal darim
# 5taie aval(injalase kar badarim):


# from django.db.models.signals import post_save, pre_save, pre_delete, post_delete, m2m_changed

#post_save migoiad hargah dron DB chizi save shod etela bedeh
# pre_save migoiad ghabl az save shodan . yani karbar darkhast sabtnam mifrestad bakhabar kon
# pre_delete : ghabl az delete shodan khabar bede
# post delete migoiad bad az delete shodan bakhabar kon
# m2m baraie reletionship ast va taghir dar anha anjam shod khbar bedeh 

# 2taie badi
#request_finished yani agar dakhasti tamam shod khabar bedeh
#request_started ""     ""     ""    shoro shod khabar bedeh
# from django.core.signals import request_finished, request_started

#injalase ba post save kar darim. va migoeim ta karbar sabnam kard profile ra ham ijad kon:

from django.db.models.signals import post_save
# method connect bein frestande signal va girande signal ertebat barghrar mikonad. connect 2 ta meghdar migirad :
# 1- ye method ijad mikonim va girande ma mishavad method va bevasile an page profile khod ra ijad mikonim
# 2- sender ke ferastande ast ke dar inja models user ast . yani vaghti taghiri roie anjam shod signal befrestad 

def save_profile_user(sender, **kwargs): # tabe ma 2ta meghdar migirad: sender ke User mast va **kwargs ke etelaati ast ke az 
# taraf signal frestade mishe daron signal gharar migirad(mesle vaghti ke user jadid sakhte mishavad ke 2 ta meghdar migirad:1-
# created ke bolian ast va ya karbar sabtnam mikonad ya ba khata movajeeh mishavad manand email tekrari va ..  .2- instance: 
# etelaati ke karbar wared mikonad va ma migirim va yek user jadid ijad mikonim baraie hamin dar view dar function 
# user_register ma User.object.usre ra barabar yek meghdar ghara midahim masalan user)
    if kwargs['created']: # agar sabtnam karbar anjam shod
        profile_user = Profile(user=kwargs['instance']) # model Profile ra seda mizanim. moshkel ma user bod ke ba table
# User ertebat yek beyek dasht: va instance yani etelaati ke az objects user baraie ma gerefte bade sabtnam karbar ra migirim(
# user ke dar views ijad kardim) va barabar ba uek motaghair gharr midahim ke dar inja profile_user ast
        profile_user.save()# va dar akhar save mikonim
post_save.connect(save_profile_user, sender= User)


