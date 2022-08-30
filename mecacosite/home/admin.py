from pyexpat import model
from django.contrib import admin

from . models import *

#baraie inke dar admin panel dastresi  jadval manand dashte bashin be size va color ke yek tabolarinline mizanim:

class ProductVariantInline(admin.TabularInline): #StackedInline be sorat khati neshan midahad
    #hala modeli ke gharar ast be Product ezafe beshavad ra moshakhas mikonim
    model = Variaants
    #dar admin panel 2 radif baraie por kardan bezarim. mishavad adad ra avaz kard . defult 3tast
    extra = 2



#alan dar panel admin tarikh ijad va update ra neshan nemidahad. ba kod zir neshan midahad
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'create', 'update', 'sub_category')#namaayesh field ha dar panel admin
    list_filter = ('create',)#filter kardan nataiej va neshandadn da admin panel: masalan yek mah akhir ya emroz va..(create)
    #vaghti dar tople meghdar midahim baiad yek , begzarim

    # ma 'sub_category' ra az model Categori ezafe mikonim be in ghesmat ta moshakhas beshavad har daste bandi to darto marbot 
    # be kodam category ast

    #baraie ijad slug automatic az prepopulated_field estefade mikonim ke yek dictionary ast ke key an slug ast chon migoeim
    # bar asas field name ijad kon ke meghdarash tople ast(). va vaghti dar tople yek meghdar darim , gharar midahim
    # ta eshtebahi string nakhanad django :
    prepopulated_fields = {
        'slug':('name',)
    }




# baraie product

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'create', 'update','amount','available', 'unit_price', 'discount', 'total_price',]
    list_filter = ('available',) # bar asas mojod bodan filter kon

    #agar bekhahim yek fild baraie viraiesh sari dar page dashte bashim az vizhegi list_editable estefase mikonim. masalan tedad
    list_editable = ('amount',)

    #baraie inke category mahsolat ra be shekl zarebin neshan dahad ta beytar entekhab konim.(albate baiad dar categori 
    # taghir ijad konim)
    raw_id_fields =  ('category',)   
    #baraie inke model Variant ra dar Product neshan dahad.(mitavanim chandin model ra vared Product konim)
    inlines = [ProductVariantInline]

#برای مشاهده نام و ایدی در قسمت سایز و رنگ در پنل ادمین
class VariantAdmin(admin.ModelAdmin):
    list_display = ['name','id']
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name','id']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variaants, VariantAdmin) 
admin.site.register(Size, SizeAdmin)
admin.site.register(Color)