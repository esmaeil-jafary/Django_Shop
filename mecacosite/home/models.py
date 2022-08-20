from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# برای محصولات
class Category(models.Model):
    # baraie ijad category haie to dar to az relationships estefade mikonim:
    #har categori mitone chandim category todar to dashte bashe vali har to dar to motaleg be yek category ast
    #chon in field sub_category ghara ast ba modele khodash ertebat dashte bashad banabar in meghar aval self migozarim.
    #bade baiad dar tarif category moshakhas konim daste madar ast ya zir majmoe ke az bolianfield estefade mikonim.
    
    
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True, related_name='sub')#null=True, blank=True yani
    #agar dar daste band to dar to khodash madar bod va ba jaei ertebat nadasht error nadahad.
    #related_name: yani alan ma az category ba forignkey ba daste haie to dar to ertebat darim va agar bejhahim az daste haie 
    # to dar to ham ba category ertebat dashte bashim az yek vizhegi related_name= estefade mikonim
    sub_cat = models.BooleanField(default=False) #default=False yani har categori jadid ke misazim defult daste madar bashad 
    name = models.CharField(max_length=200)
    create = models.DateTimeField(auto_now_add=True)#auto_now_add yani harvagh category ijad shod django tarikh va zaman ra sabt mikonad
    update = models.DateTimeField(auto_now=True)# mesl balast faghat vaghti update konim faghat tarikh va zaman re be update midahad
    #sakhtan slug baaraie namaiesh name kala dar url. va dar admin panel az charecter haie farsi poshtibani nemishavad
    # banabar in baiad az yek vizhegi estefade konim allow_unicode va barabar ba true gharar midahim. va baiad Uniqe konim slug ra
    # ta dar category be moshkel nakhorim az unique=True estefade mikonim. har fildi ra bekhahim mitavanim uniqe konim
    # va baraie inke slug ra khode django auto ijad konad baiad beravim be page admin va :->
    slug = models.SlugField(allow_unicode=True, unique=True, null=True, blank=True)
    # image = models.ImageField(upload_to='category')#migoeim kojaa zakhire beshvad
    
    image = models.ImageField(upload_to='category', null=True, blank=True)#vaghti manytomanyfield ijad mikonim 
    #baraie image ham baian null va blanck ghrar bedim. va agar baraie image ax ngozarim eror midahad ke miravim be views va hal mikon



# برای اینکه نام دسته بندی را در صفحه ادمین نمایش دهد
    def __str__(self):
        return self.name 

# vaghti dar url az 2 meghdar (slug va id masalan) estefade mikonim az get_absolute_url estefade mikonim
    def get_absolute_url(self):
        #ma dar file haie html az tag url estefade mikardim vali dadr file haie python az url estefade mishavad va dar 
        #file haie python az revers estefade mikonim ke aval baiad impirt konim
        #reverse 2ta meghdar migirad 1 esme url  va 2 args ke yek list va moshakhas mikonim che meghdar haie ra 
        # dar url ghrar dadim ke slug va id bod.  
        #hala baiad beravim be page home va tag a khodemon ro taghir bedim
        #baraie tak meghdar ham mitavanim estefade konim az get_absolute_url
        return reverse('home:category', args=[self.slug, self.id])


#برای محصولات

class Product(models.Model):
    #in field ra baraie field status va choices minevisim
    VARIANT = (
        ('None', 'none'),# (baraie ya hichkodam ya rang ya saize) None avali chizi ast ke ma dar admin panel mibinm va entekhab 
        #mikonim va daron DB meghdar midim va none dovomi daron admin panel mibinim va meghdar dehi mishavad
        ('Size', 'size'),
        ('Color', 'color'),
        
    )

    #har product marbot be kodam category ast ke yek forignkey mizanim chon har product baraie yek category ast vali har
    #category chand mahsol darad(masalan daste bandi mardane mitavanad kafsh tisher shalvar dashte bashad)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    #vaghti daste bandi to dar to ijad mikonim baraie category baiad dar pruduct ham taghir ijad konim. yani har product motasel
#mishavad ba yek daste bandi to dar to va an to dar to khodash br daste madar motasel ast va ertebat ma mishvad chand be chand
    category = models.ManyToManyField(Category, blank=True) #dar manytomanyfield , on_delete=models.CASCADE va null nadarim 
    name = models.CharField(max_length=200)
    #tedad mahsolat: ham az integerfield ham az positiveintigerfield ke adad sahih ast. va bade  frokhtan mahsol yeki az amount kam mishavad
    amount = models.PositiveIntegerField()
    # gheimat asli
    unit_price = models.PositiveIntegerField()
    # gheimat takhfif . agar khali bashad error midahad banabar in null va blanck(masalan safhe tozihat nadarad) ra true mikonim
    discount = models.PositiveIntegerField(null=True, blank=True)
    # gheimat nahaie : gheimat - takhfif = gheimat nahaie ke be karbar neshan midahim
    total_price = models.PositiveIntegerField()
    information = models.TextField(null=True, blank=True)#etelaat mahsol
    create = models.DateTimeField(auto_now_add=True)#auto_now_add yani harvagh category ijad shod django tarikh va zaman ra sabt mikonad
    update = models.DateTimeField(auto_now=True)
    #mojod bodan ya nabodan product. va agar khostim faghat mahsolati ke mojode ra neshan bedim azsh estefade konim
    available = models.BooleanField(default=True)#harvaght mahsol jadid ijad mikonim khodash neshan dahad va agar frokhtim tikash ra 
    #bezanim ta neshan nadahad.

    #baraie inke harbar ke yek mahsol tarif mikonim , entekhab konim ke mahsol saiz bandi rang bandi darad ya hichkodam
    status = models.CharField(max_length=200, null=True, blank=True, choices=VARIANT)#choices yani ma mitavanim entekhab konim 
    #bein gozine ha va az field VARIANT entekhab mikonim. va baiad fari choice ha class benevisim
         
    image = models.ImageField(upload_to='product')# dar directory media yek poshe be nam product misazad va pic ha ra daron an mirizad
#baraie size va rang ke dar gheimat tasir darad model digari baiad anjam shavad
    
    # namayesh name field ha
    def __str__(self):
        return self.name 

    #baraie mohasebe total_price(amount - unit_price) tabe zir ra minevisim
    #vaghti yek def dron class minevisim baiad hatman ya () bezarim ya az decorator property estefade konim ta raftar def ra avaz konim
    @property     #tabe ra be atrbiut tabdil mikonad
    def total_price(self):
        #agar takhfif nadasht
        if not self.discount:
            return unit_price
        #agar takhfif dasht
        elif self.discount:
            #hala darsad ra mohasebe mikonim
            total = (self.discount * self.unit_price) / 100
            #alan gheimat asli ra menhaie total mikonim ta gheimat bade takhfif bedast biad
            # int yani hatman yek adad sahih bargardanad
            return int(self.unit_price-total)
        #total_price ra return mikonim ta meghdar dehi shavad 
        return self.total_price
    # va dar akhar python manage.py makemigrations va migrate ra mizanim


    #baraie model size va color dar VARAINT
class Size(models.Model):
    name = models.CharField(max_length=100)

class Color(models.Model):
    name = models.CharField(max_length=200)

    #alan be yek model jadid niaz darim ke agar da admin panel entekhab kardim ke size bandi darim va harkodam gheimat joda darand
    #model zir ra minevisim
class Variaants(models.Model):
    name = models.CharField(max_length=100)
    product_variants = models.ForeignKey(Product, on_delete=models.CASCADE)
    size_variants = models.ForeignKey(Size, on_delete=models.CASCADE)
    color_variants = models.ForeignKey(Color, on_delete=models.CASCADE)

        #baraie inke be har mahsol vije yek gheimat va takhfif va ... bedahin az model Product copy mikonim

    amount = models.PositiveIntegerField()
    # gheimat asli
    unit_price = models.PositiveIntegerField()
    # gheimat takhfif . agar khali bashad error midahad banabar in null va blanck(masalan safhe tozihat nadarad) ra true mikonim
    discount = models.PositiveIntegerField(null=True, blank=True)
    # gheimat nahaie : gheimat - takhfif = gheimat nahaie ke be karbar neshan midahim
    total_price = models.PositiveIntegerField()

        #va barie inke javab ra name an ra dar admin pane neshan dahad:
         # namayesh name field ha
    def __str__(self):
        return self.name 

    #baraie mohasebe total_price(amount - unit_price) tabe zir ra minevisim
    #vaghti yek def dron class minevisim baiad hatman ya () bezarim ya az decorator property estefade konim ta raftar def ra avaz konim
    @property     #tabe ra be atrbiut tabdil mikonad
    def total_price(self):
        #agar takhfif nadasht
        if not self.discount:
            return unit_price
        #agar takhfif dasht
        elif self.discount:
            #hala darsad ra mohasebe mikonim
            total = (self.discount * self.unit_price) / 100
            #alan gheimat asli ra menhaie total mikonim ta gheimat bade takhfif bedast biad
            # int yani hatman yek adad sahih bargardanad
            return int(self.unit_price-total)
        #total_price ra return mikonim ta meghdar dehi shavad 
        return self.total_price
    # va dar akhar python manage.py makemigrations va migrate ra mizanim
