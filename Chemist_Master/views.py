from django.shortcuts import render,redirect
from django.http import request,HttpResponseRedirect,HttpResponse
from Chemist_Master.models import *
from med.models import Medicine
from med.forms import MedicineForm
from Chemist_Master.forms import ChemistRegisterform,guideForm
from guide.models import guides
from django.core.paginator import Paginator
from datetime import date
import random
#email
import smtplib, ssl,pandas 
import razorpay
from .models import SK_Bills,ChemistRegister

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

from django.http import HttpResponse
from django.views.generic import View
from plotly.offline import plot
from plotly.graph_objs import Scatter

import pdfkit

#Chemist signin page
def chemist_signin(request):
    if request.method=="POST":
        print(request.POST['cid'])
        try:
            m = ChemistRegister.objects.get(cid=request.POST['cid'])
            if m.chemistpwd == request.POST['chemistpwd']:
                request.session['user'] = m.cid
                return redirect('chemist:ch_index')
            else:
                return render(request,'error.html')
        except:
            return render(request,'error.html')
    return render(request,'chemist_signin1.html')

# Showing uploaded medicines by chemist
def Uploaded_Medi(request):
    
    if 'user' in request.session:
        med = guides.objects.all()
        paginator = Paginator(med, 1000) # Show 10 medicines per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'test.html',{'med':med,'page_obj': page_obj})
    else:
        return redirect('chemist:ch_signin')

            
  # Update medicine {done by chemist}   
def update_med(request,id):
    if 'user' in request.session:
        medi = guides.objects.get(id=id)  
        form = guideForm(request.POST or None, instance = medi)  
        if form.is_valid():  
            form.save()  
            return redirect('chemist:Uploaded_Medi')
        return render(request,'edit.html', {'medi': medi}) 
    else:
        return redirect('chemist:ch_signin')
 
# delete medicine{done by chemist}
def delete_med(request,id):
    med = guides.objects.get(id=id)
    med.delete()
    return redirect('chemist:Uploaded_Medi')
    
# Chemist module home page
def chemist_index(request):
    if 'user' in request.session:
        return render(request,'chemist_index.html')
    else:
        return redirect('chemist:ch_signin')
        
# chemist signup
def chemist_signup(request):
    obj=ChemistRegisterform(request.POST,request.FILES)
    if obj.is_valid():
        obj.save()
        return HttpResponseRedirect('/signin/')
    return render(request,'chemist_signup.html',{'obj':obj})

#chemist logout
def logout(request):
    if 'user' in request.session:
        del request.session['user']
        return redirect('chemist:ch_signin')
    else:
        return redirect('chemist:ch_signin')
#chemist forgotpassword

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
    server.login("mailtesting681@gmail.com","mailtest@123")
    server.sendmail("mailtesting681@gmail.com",email,otp)
    server.quit()
    return redirect('chemist:otpcheck')
    return render(request,'email.html')

def otpcheck(request):
    if request.session.has_key('otp'):
        otp = request.session['otp']
        try:
            otpobj = request.POST.get('otp')
            if otpobj == None:
                return render(request,'otp.html')
            if otp == request.POST.get('otp'):
                return redirect('chemist:newpassword')
            else:
                return HttpResponse("<a href = ''>Wrong OTP Entered.</a>")
        except:
            return redirect('chemist:ch_signin')
    return render(request,'otp.html')

def newpassword(request):
    new_pass = request.POST.get('password')
    if request.method == 'POST':
        obj = ChemistRegister.objects.get(cid = request.session['username'])
        obj.chemistpwd = new_pass
        obj.save()
        return redirect('chemist:ch_signin')
    return render(request,'forgotpassword.html')

def order_medicine(request):
    if request.session.has_key('user'):

        username = request.session['user']
        print(username)
        store = ChemistRegister.objects.get(cid=username)
        prods = StockDetails.objects.all()
        if request.POST:
            pro_data = request.POST['productname']
            pro_qty = request.POST['productquantity']
            prod_date = request.POST['data']


            obj = ProductDetails()
            obj.store_person = store
            pro_nm = StockDetails.objects.get(id=int(pro_data))
            p=int(pro_nm.price)
            total=p*int(pro_qty)
            request.session['total'] = total
            print("here is total",total)
            obj.productname = pro_nm.productName
            obj.productquantity = pro_qty
            obj.date = prod_date
            obj.save()
            return redirect('chemist:paymentData')
        return render(request, 'store/addproduct.html', {'username': username, 'prods': prods})
    else:
        return redirect('chemist:ch_signin')
    
def paymentData(request):
	donationAmount = request.session['total']*100
	if request.method == "POST":
		return paymentComplete(donationAmount, request)
	return render(request, 'payment.html', {"donationAmount": donationAmount})

def paymentComplete(donationAmount, request):
	# # ---------------------------------------------------------
	client = razorpay.Client(
	auth=("rzp_test_qDwTmKnksUVsaC", "QOr66ZQbsLdNZOmrV4YGX50V"))
	client.order.create({'amount': donationAmount, 'currency': 'INR',
							'payment_capture': '1'})
	# ----------------------------------------------------
	client.order.create({
	'amount': donationAmount,
	'currency': 'INR',
	'payment_capture': '1'
	})

	# ----------------------------------------------------
	return(redirect('chemist:ProductListView'))

def paymentSuccess(request):
	mainMsg = "Thank you for payment"
	return render(request, 'paymentSuccess.html',{'mainHeading':mainMsg})
    
    
def ProductListView(request):
    if request.session.has_key('user'):
        username = request.session['user']
        store = ChemistRegister.objects.get(cid=username)
        model = ProductDetails.objects.filter(store_person=store)
        return render(request, 'store/productlist.html', {'data': model, 'username': username})
    else:
        return redirect('chemist:ch_signin')


def DeleteProduct(request, id):
    if request.session.has_key('user'):
        username = request.session['user']
        obj = ProductDetails.objects.get(id=id)
        obj.delete()
        return redirect('chemist:ProductListView')
    else:
        return redirect('chemist:ch_signin')


def EditProduct(request, id):
    if request.session.has_key('user'):
        username = request.session['user']
        model = ProductDetails.objects.get(id=id)
        # form = ProductDetailsForm(request.POST, instance=model)
        if request.POST:
            model.productname=request.POST['productname']
            model.productquantity=request.POST['productquantity']
            model.save()
            return redirect('chemist:ProductListView')
        return render(request, 'store/editproduct.html', {'data': model, 'username': username})
    else:
        return redirect('chemist:ch_signin')

class ProductViewData():
    def __init__(self, name, date, status):
        self.name = name
        self.date = date
        self.status = status

def getStatusInStr(isStatus, isDeny):
    if isStatus == True:
        return "Accepted"
    else:
        if isDeny == True:
            return "Denied"
        return "Pending"

def Dashboard(request):
    if request.session.has_key('user'):
        username = request.session['user']
        store = ChemistRegister.objects.get(cid=username)

        pdBill = SK_Bills.objects.filter(store_person=store)
        Bcount = 0
        bset = set()
        for i in pdBill:
            bset.add(str(i.Bill_No))

        print(bset)
        bset = list(bset)
        # bset.sort()
        print(bset)

        model = ProductDetails.objects.filter(store_person=store).count()
        today_stock = ProductDetails.objects.filter(
            store_person=store, date=date.today())
        qty = 0
        today_date = date.today
        print(today_date)

        acceptedData = ProductDetails.objects.filter(store_person=store)
        acceptedData = map(lambda product: ProductViewData(getattr(product, 'productname'), getattr(product, 'date'), getStatusInStr(getattr(product, 'status'), getattr(product, 'isDeny'))), acceptedData)

        for i in today_stock:
            qty += i.productquantity
        return render(request, 'store/dashboard.html', {'acceptedData' : acceptedData, 'bset': bset, 'Bcount': len(bset), 'data': model, 'total': qty, 'date': today_date, 'username': username})
    else:
        return redirect('chemist:ch_signin')

def SK_View_Bills(request, ids):
    pdBill = SK_Bills.objects.filter(Bill_No=ids)
    tot = 0.0
    date = ""
    sperson = ''
    for i in pdBill:
        date = i.date_data
        sperson = i.store_person
        tot += float(i.pd_tot)
    return render(request, 'store/SK_Order_Bill.html', {'billNo': ids, 'sperson': sperson, 'ddate': date, 'tot': tot, 'BillDes': pdBill})

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



def SK_Create_Pdf(request, dt):
    if request.session.has_key('user'):
        username = request.session['user']
        store = ChemistRegister.objects.get(cid=username)
        sa=store.chemistaddress
        sc=store.chemistcontactno
        sn=store.chemistmname



        pdBill = SK_Bills.objects.filter(Bill_No=dt)
        tot = 0.0
        date = ""
        sperson = ''
        for i in pdBill:
            date = i.date_data
            sperson = i.store_person
            tot += float(i.pd_tot)
        date=date

        Order_Data = {}

        obj_data = SK_Bills.objects.filter(Bill_No=dt)

        prod_price = 0
        prod_qty = 0
        qty = 0
        new = {}
        grand_tot = 0
        for i in obj_data:
            recd_data = {}

            print("=============")
            # recd_data['prod_nm'] = data
            recd_data["prod_price"] = i.pd_tot
            grand_tot += i.pd_tot
            recd_data["prod_qty"] = i.pd_qty
            recd_data['real_price'] = i.pd_price
            new[str(i.pd_nm)] = recd_data
            print(new)

        Order_Data[store] = new
        print(Order_Data)
        print("======================")

        data = {'data': Order_Data, 'grand_tot': grand_tot,'sa':sa,'sn':sn,'sc':sc,'store':store,'date':date}

        pdf = render_to_pdf('admin/Create_Pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
    # else:
    #     return redirect('LoginView')
