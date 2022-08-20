from distutils.log import error
from django import forms
from.models import *
#baraie farsi kardan error message haie defult Django. ke aval baiad az site django bebinim field ma che vijegi hai migirad
# masalan charfield minmum va maximum lenghs va required(ejbari bodadn) migirad. va barie email ham invalid ast

error = {
    'min_length':'حداقل 5 کاراکتر باشد',
    'required':'این فیلد اجباری است',
    'invalid':'ایمیل معتبر وارد کنید',
}
#va hala baiad in error ke neveshtim ra dar field seda bezanim ta bejaie error defult namayesh dade shavad

# 5 fild pish farz form sabte nam django ast
# class UserRegisterForm(forms.Form):
#
#     user_name = forms.CharField(max_length=50)
#     email = forms.EmailField()
#     first_name = forms.CharField(max_length=50)
#     last_name = forms.CharField(max_length=50)
#     password_1 = forms.CharField(max_length=50)
#     password_2 = forms.CharField(max_length=50)
#
#     # baraie etebar sanji form ha. email va nam karbari yeksan pass confirm. baraie uarkodam jojagane ast. avali baraie
#     #user name
#     def clean_user_name(self):
#         user = self.cleaned_data['user_name']
#         #alan baiad DB ra check konim ke username tekrari nabashaad
#
#         #alan shat migozarim name
#         #agar bekhahim tamam etelaat ra bekeshim as all() va agar faghat yek etelaat bekhahim az get va etelat khas
#         # ra ba filter
#         if User.objects.filter(username=user).exists():
#             #baraie neshan dadan paiam error
#             raise forms.ValidationError('user exist')
#         return user
#
#     #baraie email
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError('ایمیل موجود است')
#         return email
#
#     #bara password_2 validation mizarim ta ba pasword_1 yeki bashad
#     #vaghti ba in ravesh password validation mikonim miravim views va password_1 ra password_2 konim
#     def clean_password_2(self):
#         password1 = self.cleaned_data['password_1']
#         password2 = self.cleaned_data['password_2']
#         if password1 != password2:
#             raise forms.ValidationError('پسوردها یکی نیست')
#         #shart mizarim password as 8 karecter kamtar nabashad
#         elif len(password2) <8:
#             raise forms.ValidationError('تعداد کارکتر ها بیشتر از 8 حرف باشد')
#         #dar passwor hatman horof bozorg estefade shode. az method i super estefade mikonim(shart nazarim migoiad hame
#         # bozorg bashad ma faghat yedone bozorg mikhahim. ke baiad halghe for bezanim) any yani hadaghal yek horof bozorg
#         elif not any(x.isupper() for x in password2):
#             raise forms.ValidationError('پسورد باید یک حروف بزرگ داشته باشد')
#
#         return password1
#
# #******************************************************************************************
# #for form login page
#
# class UserLoginForm(forms.Form):
#     user = forms.CharField()
#     password = forms.CharField()


#-----------------------------------------------------------------------------------------------------
#baraie estefadeh az widget ha baraie ezafe kardan option be forms
# farsi kardan paiam haie khataie django: besorat pish farz baraie etebar sanji ha yekseri payam error darad ke farsi mikonim:
#CharField yek minimom lenghs ham darim ke agar kamtar vared konim khata midahad ke pish parz django ast va ma in khataha ra 
# farsi miknim.  baraie har noe field django error message darad. 
#baraie farsi kardan yek dictionary drost mikonim ke dar aval page mizarimesh:
# nokte: chon baiaie login az pishfarz khod django estefade kardim error message haie farsi baiad az ravesh digar anjam shavad
class UserRegisterForm(forms.Form):

    # baraie estefade az widget kafi ast besorat zir seda bezanim. placeholder ham baraie ijad matn da fold
    #baraie farsi kardan error ha az error ke dar bala tarif kardim estefade mikonim
    user_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder':'یوزرنیم وارد کنید'}))
    email = forms.EmailField(error_messages=error,widget=forms.EmailInput(attrs={'placeholder':'ایمیل وارد کنید'}))
    first_name = forms.CharField(max_length=50,min_length=5,error_messages=error, widget=forms.TextInput(attrs={'placeholder':'نام'}))
    last_name = forms.CharField(max_length=50,min_length=5,error_messages=error, widget=forms.TextInput(attrs={'placeholder':'نام خانوادگی'}))
    password_1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder':'پسورد را وارد کنید'}))
    password_2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder':'تکرار پسورد را وارد کنید'}))

    # baraie etebar sanji form ha. email va nam karbari yeksan pass confirm. baraie uarkodam jojagane ast. avali baraie
    #user name
    def clean_user_name(self):
        user = self.cleaned_data['user_name']
        #alan baiad DB ra check konim ke username tekrari nabashaad

        #alan shat migozarim name
        #agar bekhahim tamam etelaat ra bekeshim as all() va agar faghat yek etelaat bekhahim az get va etelat khas
        # ra ba filter
        if User.objects.filter(username=user).exists():
            #baraie neshan dadan paiam error
            raise forms.ValidationError('user exist')
        return user

    #baraie email

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('ایمیل موجود است')
        return email

    #bara password_2 validation mizarim ta ba pasword_1 yeki bashad
    #vaghti ba in ravesh password validation mikonim miravim views va password_1 ra password_2 konim
    def clean_password_2(self):
        password1 = self.cleaned_data['password_1']
        password2 = self.cleaned_data['password_2']
        if password1 != password2:
            raise forms.ValidationError('پسوردها یکی نیست')
        #shart mizarim password as 8 karecter kamtar nabashad
        elif len(password2) <8:
            raise forms.ValidationError('تعداد کارکتر ها بیشتر از 8 حرف باشد')
        #dar passwor hatman horof bozorg estefade shode. az method i super estefade mikonim(shart nazarim migoiad hame
        # bozorg bashad ma faghat yedone bozorg mikhahim. ke baiad halghe for bezanim) any yani hadaghal yek horof bozorg
        elif not any(x.isupper() for x in password2):
            raise forms.ValidationError('پسورد باید یک حروف بزرگ داشته باشد')

        return password1

#******************************************************************************************
#for form login page

class UserLoginForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField()


#****************************************************************************************
# baraie update profile ebteda baiad moshakhast karbar ra az models User va models Profile neshan dahim ta karbar update konad
# 2ta forms ijad mikonim ueki baraie User va yeki baraie Profile va dar nahaiat 1 form ra be karbar neshan midahim

# baraie sakht form baraie Class User va Profile mesl bala amal ne mikonim va baiad az ModelForm estefade konim
class UserUpdateForm(forms.ModelForm):
    class Meta:     # vizhegihaie ma ra ezafe mikonad
        model = User # gharare  az kelas User form ijad konad
        fields = ['email', 'first_name', 'last_name']  # filde haei ke mikhahim ke Username ke ghabel taghir nabaiad bashad va 
        #taghir password ham ravesh joda 

"""
profile felan khata darad
"""
class ProfileUpdateForm(forms.ModelForm):
    class meta:
        model= Profile
        fields = ['phone', 'address']



#***********************************************************************************
#  برای لاگین کردن با شماره موبایل 

class PhoneForm(forms.Form):
    phone = forms.IntegerField()

# form verify ke ghrar ast karbar cod ra vared konad

class CodeForm(forms.Form):
    code = forms.IntegerField()

