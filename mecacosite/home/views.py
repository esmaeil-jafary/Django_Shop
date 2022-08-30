# from unicodedata import category
from itertools import product
from.models import *
from django.shortcuts import render, get_object_or_404
# get_object_or_404 baraie zamani ast ke vaghti safee ke karbar amdan ya sahvan id ya slug an ra eshtebah mizanad khata ha ra
#neshan nadahad ta so estefade shavad az etelaat ma va peigham page not find 404 neshan dadeh shavad
from django.http import HttpResponse
#har url ma yek function ast ke ma baraie page home va product ijad kardim. ama baraie estefade az template va
# models baiad az render estefade konim bejaie Httprespance. ke yek request migirad va yek templates name
# def home(request):
#     return HttpResponse('به وب سایت مکاکاکو سرویس خوش آمدید')
#
# def all_product(request):
#     return  HttpResponse('صفحه محصولات ')

#************************************************************************************************************

"""
    @estefade az render
    baiad template bases khod ra dar root besazim. va bad be setting miravamim va dar DIRS:
    template ra be jango moarefi konim. vaghti az BADE_DIR estefade mikonim eshare be root ma darad
    alan baraie har safhe yek fail html misazim
    mishavad 2 views ra be yek file html rabt dad
    render 3 ta meghdar migirad ke felan 2 ta estefade mikonim
"""
# def home(request):
#      return render(request, 'home.html')
#
# def all_product(request):
#     return  render(request, 'product.html')

#****************************************************************************************************************

"""
    alan ma file haie html ra az root site bardashtim va be app entegha dadim ke address an be sorat zir mishavad 
    alan file base.html ra dar template root misazim ta baghie ers bari konan azash
"""

def home(request):
    #namaiesh hame daste bandi ha az dakhel DB
    # category = Category.objects.all()

    # baraie inke vaghti daste bandi to dar to ijad mikonim image nazarim error nadagad az filter estefade mikonim

    category = Category.objects.filter(sub_cat=False)# migoeim anhaei ra biar ke daste bandi asli hastand va bolianfield anha 
    #dar filed sub_cat models Category barabar false bashad va sub category bashand

    #hala da ghaleb dictionary query bala ra migirim va namaiesh midahim
    #hala miravim be home.html va yek for mizanim baraie namaiesh
    return render(request, 'home/home.html',{'category':category})

#-------------------------------------------------------------------------------

#namayesh products ha
# def all_product(request, slug=None):#aval ba id ke az url migereftim kar mikard ama alan ba slug :
# def all_product(request, id=None): #alave bar request id ham az url miaiad. amabarabar none gharar midim yani agar karbar 
    #mostaghim roie id zad yani az url id ersal nashode va error nemidahad va miravad be safhe product

def all_product(request, slug=None, id=None):#baraie inke ham slug va ham id ra neshan dahim
    products = Product.objects.all()
    #mikhahim vaghti roie daste bandi ha click kardim mara bebarad be safhe mahsolat ama faghat mahsolat an daste bandi ke
    # entekhab kardim namayesh dade shavad
    #tamam dastebandi ha ra begir . baraie inke vaghti roie daste bandi ha click kardim
    # beravad be safhe product ama faghat mahsolat an daste bandi ra neshan bede
    
                #----------    
    # baraie inke dar safhe product fagha mahsolati ra neshan bede ke marbot be daste bandi to dar to hastand
    category = Category.objects.filter(sub_cat=False)


    # if id:#agar id vojod dasht 
    #if slug: #aval ba id neveshtim vali alan ba slug
    if slug and id:#baraie inke ham slug va ham id ra neshan dahim
        # data = Category.objects.get(id=id)#yek daste bandi ke id an barabar id ast braie ma begir
        #agar karbar click kard roie daste bandi mahsolat han daste ra neshan bede. va nabaiad hame mahsolat ra neshan bedim va
        #product bala ra overwrite mikonim: yani na hame mahsolat ra mikhahim va na yek mahsol ra . va etelat khasi mikhahim va
        # az filter estefade mikonim
        # data = Category.objects.get(slug=slug)
        #ba ravesh bala dar error momken ast hak shavim ke az ravesh paein estefade mikonim
        data = get_object_or_404(Category, slug=slug, id=id)#baraie inke ham slug va ham id ra neshan dahim
        products = products.filter(category=data)


    return  render(request, 'home/product.html', {'products': products, 'category': category})

#------------------------------------------------------------------------------

#page jozeiat mahsol(detail)
def product_detail(request,id):
    #barie safhe jozeiat etelat takmili va form haie nazarsanji va... ra neshan midim
    # va az .all() estefade nemikonim va jozeiat haman mahsol ra neshan midahim
    # pas az get estefade mikonim ke begoeim haman yek mahsol khas ra neshan bede
    # va chon id uniqe ast bar asas an anjam midahim. va migoeim bro dakel model product va oni ke id az url baraie ma 
    # amade ra begi va barabar in id ghrar bedeh
    # Product.objects.get(id=id)

    # agar be sorat bala bashad momken ast mored hak gharar begirim banabar in az :
    #get_object_or_404 estefade mikonim ke yani ya an mahsol ra migirad ya agar nabod error 404 neshan midahad 
    product = get_object_or_404(Product, id=id)
    # # شرط می ذاریم که اگر محصولات ما رنگ بندی و سایز بندی داشتند و استتوسشان برابر  نان نبود 
# ----------------------------------------------
# این قسمت برای taggit
    similar = product.tags.similar_objects()[:2] # [:2] یعنی حداکثر 2 محصول مشابه را نشان دهد

# ----------------------------------------------

    if product.status is not None:  # != 'None' بجای این می توانیم بنویسیم اگر مخالف بود با . هردو درست است
        #که با متود پست و گت شرط می ذاریم که اگر پست بود یک کار و اگر گت بود یک کار
        if request.method == 'POST':  
            variant = Variaants.objects.filter(product_variants_id=id)
            var_id = request.POST.get('select')
            variants = Variaants.objects.get(id=var_id) 
        else:
            variant = Variaants.objects.filter(product_variants_id=id)
            variants = Variaants.objects.get(id=variant[0].id)
        context = {'product':product, 'variant':variant, 'variants':variants, 'similar':similar}    
        return render(request, 'home/detail.html', context)
#             variant= Variaants.objects.filter(product_variant_id=id)# برای اینکه با انتخاب ورینت توسط کاربر قیمت جدید را هم نمایش دهد 
#             #ریکوئست وظیفه اشتراک گذاری اطلاعات در معماری ام وی سی را برعهده دارد
#             var_id = request.POST.get('select') #ما قرار است درخواست را از کاربر بگیریم که با استفاده از ریکوئست است و باید حتما نام هم بدیم بهش
#             variants = Variaants.objects.get(id=var_id)
#         else: #اگر متود گت بود آن را
#             #باید از مدل ورینت استفاده کنیم . همچنین از فیلتر استفاده می کنیم تا اطلاهات خاص را نشان دهیم نه همه اطلاعات 
#             variant=Variaants.objects.filter(product_Variant_id=id)   # چون کلید خارجی داریم نمیتوانیم بگوئیم ایدی مساوی ایدی . 
#             #            چون محصول خودش درون یک  مدل دیگر است
#             # برای اینکه پیش فرض یک گزینه ورینت را انتخاب داشته باشد تا جنگو ارور ندهد
#             variants= Variaants.objects.get(id= variant[0].id) # ]چون یدانه را می خواهیم بصورت پیش فرض بگیریم و به کاربر نشان بدهبم

# #        return render(request, 'home/detail.html', {'product':product})# الان گفتیم محصول را نشان بده باز و رنگ و سایز را هم اضافه نشان بده
#         # چون باید هم پروداکت و هم دیکشنری انتخاب ورینت توسط کاربر را نشان دهیم بالا را کامنت می کنیم و بصورت زیر می نویسیم       
#         context = {'product':product, 'variant':variant, 'variants':variants}
#         return render(request, 'home/detail.html', context)
    else:
        return render(request, 'home/detail.html', {'product':product,'similar':similar},) 
        # سایز و رنگ نبود همینو نشان بده
