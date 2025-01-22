from django.shortcuts import render,redirect,get_object_or_404
from django.http import request,HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Q

from .models import UserRegister,cart,UserQuery
from .forms import UserRegisterForm,UserQueryForm
from Chemist_Master.models import StoreDetails,ProductDetails,StockDetails,SK_Bills,ChemistRegister
from med.models import Medicine

from guide.models import guides

import csv
import pandas as pd 
import numpy as np 
from sklearn.linear_model import LinearRegression


import random
#email
import smtplib, ssl


from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

from django.http import HttpResponse
from django.views.generic import View

import pdfkit
import datetime
import pytz
import time
from datetime import datetime, timezone


# from practice.decorator import status
from plotly.offline import plot
from plotly.graph_objs import Scatter

import pdfkit
def createGraph(request):
    bills = SK_Bills.objects.all()
    bills_store = list(set([b.store_person for b in bills]))
    bills_products = list(set([b.pd_nm for b in bills]))
    if request.POST:
        s=request.POST["store"]
        p=request.POST["product"]
        bills_requested = SK_Bills.objects.filter(store_person=ChemistRegister.objects.get(
            cid=s), pd_nm=p).order_by('-date_data')

        bill_store_date_reuested, bills_store_quantity_requested = [], []
        [[bill_store_date_reuested.append(b.date_data.year), bills_store_quantity_requested.append(
            b.pd_qty)] for b in bills_requested]

        s1, s2 = pd.Series(bill_store_date_reuested), pd.Series(
            bills_store_quantity_requested)
        df = pd.DataFrame({'a': s1, 'b': s2})

        df = df.groupby(df['a'])['b'].agg(['sum'])
        bill_store_date_reuested, bills_store_quantity_requested = list(
            df.index), list(df["sum"])

        if (len(bills_store_quantity_requested) == 0):
            no_date = True
        else:
            no_date = False

        plot_div, data = None, None
        if not no_date:
            data = [[bill_store_date_reuested[i], bills_store_quantity_requested[i]]
                    for i in range(len(bills_store_quantity_requested))]
            model = LinearRegression()
            model.fit(np.array(bill_store_date_reuested).reshape(
                -1, 1), np.array(bills_store_quantity_requested).reshape(-1, 1))
            year = np.array(int(request.POST["year"])).reshape(-1, 1)

            predicted = model.predict(
                np.array(year).reshape(-1, 1))
            if predicted[0][0]<0:
                predicted[0][0]=0
            data.append([year[0][0], round(int(predicted[0][0]))])

            bill_store_date_reuested.append(year[0][0])
            bills_store_quantity_requested.append(int(predicted[0][0]))

            plot_div = plot([Scatter(x=bill_store_date_reuested, y=bills_store_quantity_requested,
                                     mode='lines', name='test',
                                     opacity=0.8, marker_color='green')],
                            output_type='div')
            print(bill_store_date_reuested[1])
        return render(request, 'admin/newgraph.html', {'year':year ,'s':s,'p':p,'no_data': no_date, 'store': bills_store, 'product': bills_products, 'plot_div': plot_div, 'data': data})
    return render(request, 'admin/newgraph.html', {'store': bills_store, 'product': bills_products})


# User signin 
def signin(request):
    if request.POST:
        email = request.POST['uid']
        pass1 = request.POST['userpwd']
        try:
            valid = UserRegister.objects.get(uid=email,userpwd=pass1)
            if valid:
                request.session['user'] = email
                return redirect('user:adminDashboard')
            else:
                return render(request,'error.html')
        except:
            return render(request,'error.html')
    return render(request,'signin1.html')

#User logout
def logout(request):
    if 'user' in request.session.keys():
        del request.session['user']
        return redirect('user:index')
    return redirect('user:index')

#User index
def index(request):

    return render(request,'index.html')

#User Index{This indexpage will open after doing signin}
def index1(request):
    if 'user' in request.session:
        qur=UserQueryForm(request.POST)
        if qur.is_valid():
            qur.save()
            messages.success(request,'Message sent..')
        return render(request,'index1.html',{'qur':qur})
    else:
        return redirect('user:signin')


# User register
def signup(request):
    obj=UserRegisterForm(request.POST)
    
    if obj.is_valid():
        obj.save()
        return HttpResponseRedirect('/signin/')
    return render(request,'signup.html',{'obj':obj})
    

# User can search for medicines using this function
def search(request):
    try:
        serch = request.GET.get('query')
    except:
        serch = None
    if  serch:
        med = guides.objects.all().filter(Q(mname__icontains= serch) | Q(drug__icontains = serch) | Q(symptoms__icontains = serch) | Q(diseases__icontains = serch) )
        data = {
            'med':med
        }
    else:
        data={}
    return render(request,'search1.html',data)

# Forgot Password

def forgot_pass(request):
    email = request.POST.get('email')
    request.session['username'] = email
    if email == None:
        return render(request,'email.html')
        
    print(email)
    otp = ''
    rand = random.choice('0123456789')
    rand1 = random.choice('0123456789')
    rand2 = random.choice('0123456789')
    rand3 = random.choice('0123456789')
    otp = rand + rand1 + rand2 + rand3
    print(otp)
    request.session['otp'] = otp


    port = 465
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com",port,context=context)
    server.login("UphaRProjecT@gmail.com","uphar007")
    server.sendmail("UphaRProjecT@gmail.com",email,otp)
    server.quit()
    return redirect('user:otpcheck')
        

    return render(request,'email.html')

def otpcheck(request):
    if request.session.has_key('otp'):
        otp = request.session['otp']
        try:
            otpobj = request.POST.get('otp')
            if otpobj == None:
                return render(request,'otp.html')
            if otp == request.POST.get('otp'):
                return redirect('user:newpassword')
            else:
                return HttpResponse("<a href = ''>Wrong OTP Entered.</a>")
        except:
            return redirect('user:signin')
    return render(request,'otp.html')

def newpassword(request):
    new_pass = request.POST.get('password')
    if request.method == 'POST':
        obj = UserRegister.objects.get(uid = request.session['username'])
        obj.userpwd = new_pass
        obj.save()
        return redirect('user:signin')
    return render(request,'forgotpassword.html')
#Add to cart 



def add_to_cart(request):
    if 'user' in request.session:
        data = request.session['user']
        ur = UserRegister.objects.get(uid=data)
        context={}
        items = cart.objects.filter(user = ur)
        context['items'] = items
        context['users'] = ur

        if request.method == "POST":
            mid = request.POST["mid"]
            qty = request.POST["qty"]
            # data = request.user.id
            is_exist =  cart.objects.filter(medicine__id = mid,user = ur,status= False)
            if len(is_exist)>0:
                context['msz'] = "Alredy in your cart"
                context['cls'] = "alert alert-warning"
            else:
                medicine = get_object_or_404(guides,id=mid)
                # usr = get_object_or_404(UserRegister,id=request.user.id)
                c = cart(user=ur ,medicine = medicine, quantity=qty)
                c.save()
                context['msz'] = "Added in your cart"
                context['cls'] = "alert alert-success"
              
        return render(request,'cart.html',context)
    else:
        return redirect('logout')

def get_cart_data(request):
    if 'user' in request.session:
        data = request.session['user']
        ur = UserRegister.objects.get(uid=data)
        items =  cart.objects.filter(user=ur, status=False)
        total,quantity = 0,0
        for i in items:
            total += float(i.medicine.package_price)*i.quantity
            quantity += float(i.quantity)

        res = {
            "Total":total, 
            "quan":quantity
        }
        return JsonResponse(res)
    else:
        return redirect('logout')

def change_quan(request):
    if "quantity" in request.GET:
        cid = request.GET["cid"]
        qty = request.GET["quantity"]
        cart_obj = get_object_or_404(cart,id=cid)
        cart_obj.quantity = qty
        cart_obj.save()
        return HttpResponse(cart_obj.quantity )
    
    if "delete_cart" in request.GET:
        id =request.GET["delete_cart"]
        cart_obj = get_object_or_404(cart,id=id)
        cart_obj.delete()
        return HttpResponseRedirect('/cart/')


def AdminDashboard(request):
    if request.session.has_key('user'):
        auser = request.session['user']

        model = ChemistRegister.objects.all()
        # predict_graph()

        # print(today.month)
        data = {}
        try:
            q = request.GET.get('search')
        except:
            q = None
        if q:
            product = ChemistRegister.objects.filter(
                Q(StoreName__icontains=q) | Q(PersonName__icontains=q))
            data = {
                'data': model,
                'StoreDetails': product,
                'auser': auser
                # 'des': dealer
            }
        else:
            data = {'data': model}
        return render(request, 'admin/dashboard.html', data)
    else:
        return redirect('user:signin')
    
def editstock(request, id):
    if request.session.has_key('user'):
        email = request.session['user']
        obj1 = StockDetails.objects.get(id=id)
        # a = profileform(instance=obj)
        # obj1 = StoreDetails.objects.all()
        if request.POST:
            obj1.productName = request.POST['productName']
            obj1.quantity = request.POST['quantity']
            obj1.price = request.POST['price']
            obj1.save()
            return redirect('user:viewstock')

        return render(request, 'admin/editstock.html', {'prod': obj1})
    else:
        return redirect('user:signin')

def viewstore(request, id):

    if request.session.has_key('user'):
        model = ChemistRegister.objects.get(id=id)
        prods = ProductDetails.objects.filter(store_person=model, status=False, isDeny=False)
        return render(request, 'admin/storedetails.html', {'data': model, 'prod': prods})
    else:
        return redirect('user:signin')


def editstore(request, id):
    if request.session.has_key('user'):
        email = request.session['user']
        obj1 = ChemistRegister.objects.get(id=id)
        # a = profileform(instance=obj)
        # obj1 = StoreDetails.objects.all()
        if request.POST:
            obj1.StoreName = request.POST['StoreName']
            obj1.email = request.POST['email']
            request.session['auser'] = request.POST['email']
            obj1.PersonName = request.POST['PersonName']
            obj1.Contact = request.POST['Contact']
            obj1.add1 = request.POST['add1']
            obj1.save()
            return redirect('user:adminDashboard')

        return render(request, 'admin/editstore.html', {'shop': obj1})
    else:
        return redirect('user:signin')

def viewstock(request):
    if request.session.has_key('user'):
        model = StockDetails.objects.all()
        return render(request, 'admin/stockdetails.html', {'data': model})
    else:
        return redirect('user:signin')

def accepteddata(request, sk, id):
    print("=============================================")
    print(f"shope = {sk} -----  prod{id}")
    p_qty = 0
    p_nm = ""
    obj = ProductDetails.objects.get(id=id)
    obj.status = True
    p_nm = obj.productname
    p_qty = obj.productquantity
    obj.save()

    print(obj)
    product_obj = StockDetails.objects.get(productName=p_nm)
    print(product_obj)
    product_obj.quantity -= p_qty
    product_obj.save()
    print("=============================================")
    return redirect('user:viewstore', sk)

def billdata(request, dt):
    # print(dt)
    sp = str(dt)
    print(sp)
    SD = ChemistRegister.objects.get(cid=str(sp))
    print("======================")
    print(SD)
    Order_Data = {}

    obj_data = ProductDetails.objects.filter(status=True, store_person=SD)
    show = False
    for i in obj_data:
        if not i.Bills_id == "":
            show = True

    prod_price = 0
    prod_qty = 0
    qty = 0
    new = {}
    grand_tot = 0
    for i in obj_data:
        recd_data = {}
        print(i)
        qty += 1
        print(qty)

        prod_qty += int(i.productquantity)
        print(prod_qty)

        data = StockDetails.objects.get(productName=i.productname)
        print(data, i.productquantity)
        print(data.price)
        rec = float(data.price * i.productquantity)
        print(rec)
        prod_price += rec
        print(prod_price)

        print("=============")
        # recd_data['prod_nm'] = data
        recd_data["prod_price"] = prod_price
        grand_tot += prod_price
        recd_data["prod_qty"] = prod_qty
        recd_data['real_price'] = data.price
        new[str(data.productName)] = recd_data
        print(new)
    Order_Data[SD] = new
    print(Order_Data)
    print("======================")
    data={'data': Order_Data, 'grand_tot': grand_tot, 'show': show,'store':SD}
    # pdf = render_to_pdf('admin/billdata.html', data)
    # return HttpResponse(pdf, content_type='application/pdf')
    return render(request, 'admin/billdata.html', {'data': Order_Data, 'grand_tot': grand_tot, 'show': show})

def denieddata(request, sk, id):
    print("=============================================")
    print(f"shope = {sk} -----  prod{id}")
    p_qty = 0
    p_nm = ""
    obj = ProductDetails.objects.get(id=id)
    obj.isDeny = True
    obj.status = False
    p_nm = obj.productname
    p_qty = obj.productquantity
    obj.save()

    print(obj)
    product_obj = StockDetails.objects.get(productName=p_nm)
    print(product_obj)
    product_obj.quantity -= p_qty
    product_obj.save()
    print("=============================================")
    return redirect('user:viewstore', sk)



def Confirm_Orders(request):
    obj = ProductDetails.objects.filter(status=True)

    data_set = set()
    for i in obj:
        nm = str(i.store_person)
        print(nm)
        data_set.add(nm)
    # print(data_set)
    data_set = list(data_set)
    # print(data_set)
    data_set.sort()
    obj1 = data_set
    print(obj1)
    Order_Data = {}

    for i in obj1:
        print("=============")
        print(i)
        recd_data = {}

        data = StoreDetails.objects.get(StoreName=str(i))
        # recd_data['stnm'] = data.StoreName

        obj_data = ProductDetails.objects.filter(
            status=True, store_person=data)

        f_total = 0
        prod_price = 0
        prod_qty = 0
        qty = 0
        show = False
        for i in obj_data:
            print(i)
            qty += 1
            print(qty)

            prod_qty += int(i.productquantity)
            print(prod_qty)
            print("\n\n===================================---")
            print(i.productname)
            print("===================================---\n\n")
            data = StockDetails.objects.get(productName=str(i.productname))
            print(data, i.productquantity)
            print(data.price)
            rec = float(data.price * i.productquantity)
            print(rec)
            prod_price += rec
            f_total += prod_price
            print(prod_price)
            for i in obj_data:
                if not i.Bills_id == "":
                    show = True

        print("=============")

        recd_data["prod_price"] = f_total
        recd_data["prod_qty"] = prod_qty
        recd_data["qty"] = qty
        recd_data['show'] = show
        Order_Data[str(i.store_person)] = recd_data
        print(Order_Data)
    return render(request, 'admin/Confirm_orders.html', {'orders': Order_Data})


def deletestore(request, id):
    if request.session.has_key('user'):
        model = StoreDetails.objects.get(id=id)
        model.delete()
        return redirect('user:adminDashboard')
    else:
        return redirect('user:Adminlogin')




def Confirm_Orders(request):
    obj = ProductDetails.objects.filter(status=True)

    data_set = set()
    for i in obj:
        nm = str(i.store_person)
        print(nm)
        data_set.add(nm)
    # print(data_set)
    data_set = list(data_set)
    # print(data_set)
    data_set.sort()
    obj1 = data_set
    print(obj1)
    Order_Data = {}

    for i in obj1:
        print("=============")
        print(i)
        a=ChemistRegister.cid
        print(a)
        recd_data = {}

        data = ChemistRegister.objects.get(cid=str(i))

        obj_data = ProductDetails.objects.filter(
            status=True, store_person=data)

        f_total = 0
        prod_price = 0
        prod_qty = 0
        qty = 0
        show = False
        for i in obj_data:
            print(i)
            qty += 1
            print(qty)

            prod_qty += int(i.productquantity)
            print(prod_qty)
            print("\n\n===================================---")
            print(i.productname)
            print("===================================---\n\n")
            data = StockDetails.objects.get(productName=str(i.productname))
            print(data, i.productquantity)
            print(data.price)
            rec = float(data.price * i.productquantity)
            print(rec)
            prod_price += rec
            f_total += prod_price
            print(prod_price)
            for i in obj_data:
                if not i.Bills_id == "":
                    show = True

        print("=============")

        recd_data["prod_price"] = f_total
        recd_data["prod_qty"] = prod_qty
        recd_data["qty"] = qty
        recd_data['show'] = show
        Order_Data[str(i.store_person)] = recd_data
        print(Order_Data)
    return render(request, 'admin/Confirm_orders.html', {'orders': Order_Data})

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def Create_Pdf(request, dt):
    if request.session.has_key('user'):
        tz = pytz.timezone('Asia/Kolkata')
        # time_now = datetime.datetime.now(timezone.utc).astimezone(tz)
        # millis = int(time.mktime(time_now.timetuple()))
        # order_id = 'SKBill_Id'+str(millis)
        order_id = 'SKBill_Id'
        print(order_id)

        # request.session['Order_id'] = order_id
        print("fname:-----------",dt)
        Bill_timestamp_no = order_id
        print(Bill_timestamp_no)

        sp = str(dt)
        print(sp)
        SD = ChemistRegister.objects.get(chemistfname=str(sp))
        print("======================")
        address=SD.chemistaddress
        contact=SD.chemistcontactno
        Name=SD.chemistmname
        Order_Data = {}

        obj_data = ProductDetails.objects.filter(status=True, store_person=SD)

        prod_price = 0
        prod_qty = 0
        qty = 0
        new = {}
        grand_tot = 0
        for i in obj_data:
            recd_data = {}
            qty += 1

            prod_qty += int(i.productquantity)

            data = StockDetails.objects.get(productName=i.productname)
            print(data, i.productquantity)
            print(data.price)
            rec = float(data.price * i.productquantity)
            print(rec)
            prod_price += rec
            print(prod_price)

            print("=============")
            # recd_data['prod_nm'] = data
            recd_data["prod_price"] = prod_price
            grand_tot += prod_price
            recd_data["prod_qty"] = prod_qty
            recd_data['real_price'] = data.price
            new[str(data.productName)] = recd_data

            skObj = SK_Bills()
            skObj.store_person = SD
            skObj.Bill_No = str(Bill_timestamp_no)
            skObj.pd_nm = i.productname
            skObj.pd_price = data.price
            skObj.pd_qty = prod_qty
            skObj.pd_tot = prod_price
            skObj.date_data = i.date
            skObj.save()
            i.delete()
        Order_Data[SD] = new
        print(Order_Data)
        print("======================")
        data = {'data': Order_Data, 'grand_tot': grand_tot,'SD':SD,'ADD':address,'CON':contact,'NAME':Name,'new':new}
        pdf = render_to_pdf('admin/billdata.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
