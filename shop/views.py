from django.shortcuts import render, redirect, HttpResponse, Http404
from django.contrib import messages
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from shop.Paytm import Checksum
from shop.Paytm.Checksum import verify_checksum
MERCHANT_KEY = 'your merchant key here'
# Create your views here.
def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))
        allProds.append([prod, range(1, nSlides), nSlides])
    context = {'allProds': allProds}
    return render(request, 'shop/index.html', context)

def allCategory(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        allProds.append(prod)
    context = {'allProds': allProds}
    return render(request, 'shop/allcategory.html', context)

def searchmatch(query, item):
    '''return true if query matches the item  '''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchmatch(query, item)]
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    context = {'allProds': allProds}
    if len(allProds) == 0 or len(query)<3:
        context = {'msg': "Please make sure to enter relevant search query:"}
    return render(request, 'shop/search.html', context)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    messages.success(request, 'Welcome to contact')
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
        return render(request, 'shop/contactus.html', {'thank': thank})
    return render(request, 'shop/contactus.html')

def tracker(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            orderId = request.POST.get('orderId', '')
            email = request.POST.get('email', '')
            # return HttpResponse(f"{orderId} and {email}")
            try:
                order = Order.objects.filter(order_id=orderId, email=email)
                if len(order)>0:
                    update = OrderUpdate.objects.filter(order_id=orderId)
                    updates = []
                    for item in update:
                        updates.append({'text': item.update_desc, 'time': item.timestamp})
                        response = json.dumps({"status":"success", "updates": updates, "itemsJson":order[0].items_json}, default=str)
                    return HttpResponse(response)
                else:
                    return HttpResponse({"status":"no item"})
            except Exception as e:
                return HttpResponse({"status":"error"})
                
        return render(request, 'shop/tracker.html')
    else:
        return HttpResponse("Login Required")


def productView(request, id):
    # To fetch the products using the id because forget to create primary key in models so django will use the key as id
    product = Product.objects.filter(id=id)
    return render(request, 'shop/productview.html', {'product':product[0]})

def checkout(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            item_json = request.POST.get('itemJson', '')
            name = request.POST.get('name', '')
            amount = request.POST.get('amount', '')
            email = request.POST.get('email', '')
            address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
            city = request.POST.get('city', '')
            state = request.POST.get('state', '')
            zip_code = request.POST.get('zip_code', '')
            phone = request.POST.get('phone', '')
            order = Order(item_json=item_json, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone, amount=amount)
            order.save()
            update = OrderUpdate(order_id=order.order_id, update_desc="Order has been placed")
            update.save()
            thank = True
            id = order.order_id
            # return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
            # Request paythm to transfer the amount to the account
            param_dict =  {
                'MID':'your merchant id here',
                'ORDER_ID':str(order.order_id),
                'TXN_AMOUNT':str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID':'Retail',
                'WEBSITE':'WEBSTAGING',
                'CHANNEL_ID':'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',
            }
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
            return render(request, 'shop/paytm.html', {'param_dict': param_dict})
        return render(request, 'shop/checkout.html')
    else:
        return HttpResponse("Login Required")

def mycart(request):
    return render(request, 'shop/home.html')

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    # verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})
