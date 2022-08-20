from email import message
import profile
from django.shortcuts import render,redirect

# from mecacosite import accounts
# from .forms import UserRegisterForm    dar in ravash tak tak form ha ra baiad seda bezanim vali agar * bezarim
# digar niazi nist tak tak seda konim
from .forms import *
from .models import *
from django.contrib.auth.models import User
#baraie baresi mojjod bodan user pass dar DB
from django.contrib.auth import authenticate, login, logout

#baraie estefade az messages va namayesh paiam ha
from django.contrib import messages

#baraie change password
from django.contrib.auth.forms import PasswordChangeForm
# baraie session ha ast va vaghti ke password ra avaz mikonim sessions haie ghabli ra bebandad


#baraie inke karbar vaghti login nakarde natavanad profile khod ra bebinad va hamchenin update va change profile ra az 
# decorators estefade mikonim ke raftar tabe ra avaz mikonad
# va az method login_required estefade mikonim. alan dar update va profile estefade mikonim
from django.contrib.auth.decorators import login_required

from random import randint

"""
@agar user az tarigh method get vared shod form ra neshan bede
 
"""
def user_register(request):
    if request.method == 'POST':
        # vaghti karbar aztarigh method post vard beshavad be form elam mikonim.
        form = UserRegisterForm(request.POST)
        # hala shart mizarim ke agar etelaat karbar tamiz bod sabt nam ra anjam bedeh(kod mokhareb ya email sahih , adad ,...)
        if form.is_valid():
            # is valid 3 method digar ra farakhani mikonad ke outomatic etebar sanji mikonad va etelaat ra dakhel dictionary
            #mirizad va etelat ra ma az anja mikhanad
            data = form.cleaned_data
            #hala user ra ijad mikonim . va objects baraie ertebat ba models ma mibashad.
            # alan 5 ta meghdar migirim. migoeim username ra az meghdar haie clean begir
            # User.objects.create_user(username=data['user_name'], email=data['email'], first_name=data['first_name'],
            #                          last_name=data['last_name'], password=data['password_2'])
            #allan bade etmam sabt nam karbar ra mifrestim page home chon felan safhe login nadarim

            #signal:
            #baraie estefade az signal kol tabe zir ra barabar user(name ekhtiari ast) gharar midahim
            user = User.objects.create_user(username=data['user_name'], email=data['email'], first_name=data['first_name'],
                                     last_name=data['last_name'], password=data['password_2'])

            # baraie estefade az signal save user bala ra besorat zir:
            user.save()
            return redirect('home:home')#aval esme app va bad safhe ke mikhahim beravim va name url an


    # dar else migoeim agar get bod form ra neshan bede
    else:
        form = UserRegisterForm()
    context = {'form':form}
    return render(request, 'accounts/register.html', context)

#-------------------------------------------------------------------------------------------------------------
# # for login form ba base username
# #moshakhas mikonim agar method post bod yek kar va get bod yekar digar
# def user_login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#         # hala baraie validation
#         if form.is_valid(): # data ha ra mirizad dakhel dictionary cleanData
#             data = form.cleaned_data
#             # hala check konim username va pass dar DB vojod dard ya na
#             user = authenticate(request,username=data['user'], password=data['password'])
#             #agar user va pass sahih bashad authenticate meghdar clean shode ra mirizad dar user va agar eshtebah bashad
#             #null barmigardanad
#             if user is not None:  # agar meghdar khali nabod
#                 login(request,user) # ba method login karbar ra login mikonim
#                 #bad az login befrest be home page
#                 return redirect('home:home')
#
#
#     # agar GET bod ya user pass eshtebah bod
#     else:
#         form = UserLoginForm()
#     return render(request,'accounts/login.html',{'form':form})

#-------------------------------------------------------------------------------------------------------
# for login form ba base username va email
#moshakhas mikonim agar method post bod yek kar va get bod yekar digar
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        # hala baraie validation
        if form.is_valid(): # data ha ra mirizad dakhel dictionary cleanData
            data = form.cleaned_data
            try: # baraie login ba username va ba email. try aval saei mikonad ba email va agar username ra ham vared
                #kard baz login kon
                # hala check konim username va pass dar DB vojod dard ya na
                user = authenticate(request,username=User.objects.get(email=data['user']), password=data['password'])
            except:
                user = authenticate(request, username=data['user'], password=data['password'])
            #agar user va pass sahih bashad authenticate meghdar clean shode ra mirizad dar user va agar eshtebah bashad
            #null barmigardanad
            if user is not None:  # agar meghdar khali nabod
                login(request,user) # ba method login karbar ra login mikonim
                #bad az login befrest be home page

                # baraie namayesh message ha. va 'primary' ha rang ra moshakhas mikonad. hala mira vim be file message
                # va shart migozarim ke agar dar message meghdar sevom yani extra tag vojod dasht
                #bar asas hamon rang neshan bedeh
                messages.success(request,'خوش امدید وارد شدید', 'primary')
                return redirect('home:home')
                #agar user pass eshtebah bod message dahad va 'danger' baraie rang an
            else:
                messages.error(request, 'پسورد اشتباه است', 'danger')


    # agar GET bod ya user pass eshtebah bod
    else:
        form = UserLoginForm()
    return render(request,'accounts/login.html',{'form':form})

#*************************************************************************************************

#for logout
def user_logout(request):
    logout(request)
    #vaghti logout kard paiam neshan bedeh. (seccess va error farghi nadaran ba ham). baiad brim dar template root file
    #message.html ijad konim
    messages.success(request, 'با موفقیت خارج شدید', 'warning')
    return redirect('home:home')

#**************************************************************************************************

#4 baraie ijad safhe karbari profile. ke baiad model besazim

# decorators estefade mikonim ke ta karbar login nakarde ejaze nadahad vared safhe shavad. ke az @ estefade mikonim va
# yek login_url= migirad ke moshakhas mikonim karbar agar khast beravad be profile aval befrest be login

@login_required(login_url='accounts:login')
def user_profile(request):
    #neshan dadan fildha be karbaran ba estefade az id
    #id karbari ke darkhast dade ra begir
    profile = Profile.objects.get(user_id=request.user.id)
    # baraie namaiesh mohtava ha anha ra dar dictionary gharar midahim
    return render(request, 'accounts/profile.html',{'profile':profile})

#***********************************************************************************************
#warning : felan khata darad va do form user va profile ra baaham neshan nemidahad

#5 baraie inke karbar profile khodesh ro update kone

# def user_update(request):
#     #namayesh dota form update User,Profile
#     #aval moshakhas konim agar az GET omade form ro neshan bedim
#     if request.method == 'POST':
#         user_form = UserUpdateForm(request.POST, instance=request.User)
#         profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

#     #alan chon 2ta form darim baiad chek konim ke form(dakhast karbar) drost ast ya na
#         if user_form and profile_form.is_valid():
#             # etelaat ra daron DB save mikonim
#             user_form.save()
#             profile_form.save()
#         # vaghti hame chiz drost bod ye message neshan midahim.    success style rang message ast
#             messages.success(request, 'update successfully', 'success')
#             return redirect('accounts:profile')
#     else:
#         #da ghei insorat agar method GET bod 2 ta form mara namayesh bede
#         user_form = UserUpdateForm()
#         profile_form = ProfileUpdateForm()
#     # baraie namayesh etelaat be karbar baiad dron yek dictionary daron tabe render berizim ta da file html dashte bashimash
#     context = {'user_form':user_form, 'profile_form':profile_form}
#     # context ra dar render gharar midahim
#     return render(request, 'accounts/update.html', context)

                #.........................
                
# decorators estefade mikonim ke ta karbar login nakarde ejaze nadahad vared safhe shavad. ke az @ estefade mikonim va
# yek login_url= migirad ke moshakhas mikonim karbar agar khast beravad be profile aval befrest be login

@login_required(login_url='accounts:login')
def user_update(request):
    #namayesh dota form update User,Profile
    #aval moshakhas konim agar az GET omade form ro neshan bedim
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        #instance baraie inke meghdar haie mojod ra be karbar neshan dahim ta karbar bebinad va agar khast taghir dahad
        #va baiad aval maghadir ra az database begirim. baraie method GET ke dar else goftim ham instance ra ghara midahim

        # profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

    #alan chon 2ta form darim baiad chek konim ke form(dakhast karbar) drost ast ya na
        if user_form.is_valid():
            # etelaat ra daron DB save mikonim
            user_form.save()
            profile_form.save()
        # vaghti hame chiz drost bod ye message neshan midahim.    success style rang message ast
            messages.success(request, 'update successfully', 'success')
            return redirect('accounts:profile')
    else:
        #da ghei insorat agar method GET bod 2 ta form mara namayesh bede
        user_form = UserUpdateForm(instance=request.user)
        # profile_form = ProfileUpdateForm(instance=request.user.profile)
    # baraie namayesh etelaat be karbar baiad dron yek dictionary daron tabe render berizim ta da file html dashte bashimash
    # context = {'user_form':user_form, 'profile_form':profile_form}
    context = {'user_form':user_form}
    # context ra dar render gharar midahim
    return render(request, 'accounts/update.html', context)

#************************************************************************************
# baraie taghir password
#baraie in ghesmat az sessions estefadeh mikonim . ke aval baiad import konim
from django.contrib.auth import update_session_auth_hash

# ma form nemisazim va az form pish sakhteh django estefade mikonim baaraie taghir password va register
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            #baraie session 2ta meghdar migirad: request va yek user(chon az inja be user dasresi nadarim vali chon ba form bala be
            # object user dastresi darim form.user ra midahim)
            update_session_auth_hash(request, form.user)
            messages.success(request, 'پسورد با موفقیت تغییر کرد', 'success')
            return redirect('accounts:profile')

        #agar baraie taghir password: pass avalie ra eshtebah zad ya faramosh  karde bod
        else:
            messages.error(request, 'پسورد اشتباه است', 'danger')    
            return redirect('accounts:change')

    else:
        #agar ba method post amade bod form ra neshan bedeh
        # va ba request.user  moshakhas mikonim darkhast az tarigh kodam user ast
        form = PasswordChangeForm(request.user)
        #baraie inke in form PasswordChangeForm ra dar file change.html dashte bashim , motaghair form khod ra ba {'form':form}
        #ke dictionary ast mifrestim
    return render(request, 'accounts/change.html',{'form':form} )
# alan baraie ma neshan midahad form taghir passwoer ra vali neveshte ha englesh hastand va baiad beravim be -->
# setting va ghesmat AUTH-PASSWORD va az anja 4 shart pass ra farsi mikonim


#*********************************************************************************************

#baraie login kardan ba mobile

def phone(request):
    if request.method == 'POST':
        #aval form phon ra migirim va migim request az tarigh POST mikhad biad barat
        form=PhoneForm(request.POST)
        #va hala user shomare hamrahesho vared kard check mikonim ke shomare sahih  ast ya na
        if form.is_valid():
            
            #baraie inke kharej az in tabe be randit ke neveshtim dastresi dashte bashim da kol in page az global estefade mikonim
            global random_cod, phone

            data= form.cleaned_data
            # hal agar mobile sahih bod an ra migirim va 
            # hamchenin chon az intigerfield estefade kaardim 0 ra neshan nemidahad. banabar in az fstring(f"{}") estefade mikonim:
            # phone = data['phone']
            phone = f"0{data['phone']}"#moshkel 0 hal shod

            #hala yek kod(adad tasadofi) baiad ersal konim be karbar va migoeim dar form badi vared kon
            # baraie adad tasadofi az random estefade mi konim : from random import randint
            random_cod = randint(10000,20000 )
            #hala mikhahim be mobile mored nazar in code ra sms konim.
            # ke baiad azal ketabkhane marbot sherkat erae service ra nasb konim(masalan pip install ghasedak va pip install requests)
            #  va import ghasedak 
            # va kod haie marbot be on ra dar in ghesmat migzarim
            # sms = ghasedak.Ghasedak("merchend kod")
            # sms.send{{'message': random_cod, 'receptor': phone}}
            # alan karbar bauad befrestim safhe jadid pas url an ra misazim
        return redirect('accounts:verify')  
    else:
        form = PhoneForm()
    return render(request, 'accounts/phone.html', {'form':form})

    #hala view verify ra minevisim
def verify(request):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            # data=form.cleaned_data
        #cod ke karbar ferestade ba kod ma check mikonim yeki bod login anjam shavad:
            if random_cod ==form.cleaned_data['code']:
                #dar inja chon be user mostaghim dastresi nadarim vali chon be shomare tamas dastresi darim mitavanim be model
                #profile khodemon dastresi dashte bashim. va chon yek rabete yek be yek ba user dasht mitavanim dastresi peida konim
                # va az get estefade mikonim chon faghat yek meghdar ra  mikhahim biron bekeshim
                profile = Profile.objects.get(phone=phone) # har profile id uniqe darad
                # phone=phone yani hamin shomare tamasi ke karbar ijad mikonad

                # alan chon az profile kilid yek be yek darim ba user :
                # va ba estefade az field lookup ke ba __ neshan midahim va  mitavanim query daghightary dashte bashim va ba 
                # estefade az id profile mitavanim moshakhas konim ke id baraie kodam user ast
                user = User.objects.get(profile__id= profile.id)
                login(request, user)
                messages.success(request, 'hi user')
                return redirect('home:home')

                #agar karbar codee ra eshtebah zad :
            else:
                messages.error(request, 'kod eshtebah')

    else:
        form = CodeForm()


    return render(request, 'accounts/code.html', {'form': form})











