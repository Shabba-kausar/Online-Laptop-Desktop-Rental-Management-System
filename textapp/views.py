from random import randint

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from datetime import date
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Min, Sum, Avg

# Create your views here.
def home(request):
    product = Product.objects.all()
    return render(request, "homeuser.html", locals())

def user_signup(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        lname = request.POST['secondname']
        email = request.POST['email']
        pwd = request.POST['password']
        mobile = request.POST['mobile']

        user = User.objects.create_user(first_name=fname, last_name=lname, email=email, password=pwd, username=email)
        Signup.objects.create(user=user, mobile=mobile)
        messages.success(request, "Register Successful")
        return redirect('user_login')
    return render(request, "user_signup.html")


@login_required(login_url='/user_login/')
def user_profile(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        lname = request.POST['secondname']
        email = request.POST['email']
        mobile = request.POST['mobile']

        user = User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname, email=email)
        Signup.objects.filter(user=request.user).update(mobile=mobile)
        messages.success(request, "Updation Successful")
        return redirect('user_profile')
    data = Signup.objects.get(user=request.user)
    return render(request, "user_profile.html", locals())


def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        pwd = request.POST['password']
        user = authenticate(username=email, password=pwd)
        if user:
            if user.is_staff:
                messages.success(request, "Invalid User")
                return redirect('user_login')
            else:
                login(request, user)
                messages.success(request, "User Login Successful")
                return redirect('home')
        else:
            messages.success(request, "Invalid User")
            return redirect('user_login')
    return render(request, "user_login.html")

@login_required(login_url='/user_login/')
def user_logout(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('user_login')

def product_detail(request, pid):
    product = Product.objects.get(id=pid)
    return render(request, "product_detail.html", locals())

def view_booking(request, pid):
    booking = Booking.objects.get(id=pid)
    return render(request, "view_booking.html", locals())

def invoice(request, pid):
    booking = Booking.objects.get(id=pid)
    return render(request, "invoice.html", locals())

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def numOfDays(date1, date2):
    return (date2 - date1).days

@login_required(login_url='/user_login/')
def book_laptop(request, pid):
    if request.method == "POST":
        productobj = Product.objects.get(id=pid)
        userobj = Signup.objects.get(user=request.user)
        fromdate = request.POST['fromdate']
        payment_method = request.POST.get("payment_method")
        payment_screenshot = request.FILES.get("payment_screenshot")
        todate = request.POST['todate']
        print(fromdate, todate)
        typename = request.POST['typename']
        quantity = request.POST['quantity']
        address = request.POST['address']
        a = fromdate.split('-')
        c = todate.split('-')
        date1 = date(int(a[0]), int(a[1]), int(a[2]))
        date2 = date(int(c[0]), int(c[1]), int(c[2]))
        totaldays= numOfDays(date1, date2)
        totalprice=int(quantity)*int(productobj.rentalprice)*totaldays
        bookingnumber = random_with_N_digits(8)
        Booking.objects.create(productname=productobj, user=userobj, bookingnumber=bookingnumber, status="pending", fromdate=fromdate, todate=todate, typename=typename, quantity=quantity, address=address, totalprice=totalprice, totaldays=totaldays)
        messages.success(request, "Booking Generated and Booking Number is " + str(bookingnumber))
        return redirect('my_booking')
    return render(request, "book_laptop.html")

def shop_page(request):
    product = Product.objects.all()
    return render(request, "shop_page.html", locals())

def laptop(request):
    product = Product.objects.filter(typename='Laptop')
    return render(request, "laptop.html", locals())

def desktop(request):
    product = Product.objects.filter(typename='Desktop')
    return render(request, "desktop.html", locals())

@login_required(login_url='/login_admin/')
def edit_about(request):
    if request.method == "POST":
        pagetitle = request.POST['pagetitle']
        description = request.POST['description']
        About.objects.filter(id=1).update(pagetitle=pagetitle, description=description)
    data = About.objects.get(id=1)
    return render(request, "edit_about.html", locals())

def about(request):
    data = About.objects.all()
    d = {'data': data}
    return render(request, "about.html", locals())

@login_required(login_url='/login_admin/')
def edit_contact(request):
    if request.method == "POST":
        pagetitle = request.POST['pagetitle']
        description = request.POST['description']
        email = request.POST['email']
        contactno = request.POST['contactno']
        Contact.objects.filter(id=1).update(pagetitle=pagetitle, description=description, email=email, contactno=contactno)
    data = Contact.objects.get(id=1)
    return render(request, "edit_contact.html", locals())

def contact(request):
    data = Contact.objects.all()
    d = {'data': data}
    return render(request, "contact.html", locals())

@login_required(login_url='/login_admin/')
def dashboard(request):
    product = Product.objects.filter()
    brand = Brand.objects.filter()
    new = Booking.objects.filter(status="pending")
    Approved = Booking.objects.filter(status="Approved")
    Unapproved = Booking.objects.filter(status="Unapproved")
    Total = Booking.objects.filter()
    return render(request, "home.html", locals())


def login_admin(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=uname, password=pwd)
        if user:
            if user.is_staff:
                login(request, user)
                messages.success(request, "Admin Login Successful")
                return redirect('dashboard')
            else:
                messages.success(request, "Invalid Admin")
                return redirect('login_admin')
    return render(request, "admin_login.html")

@login_required(login_url='/login_admin/')
def logout_admin(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('login_admin')

@login_required(login_url='/login_admin/')
def add_brand(request):
    if request.method == "POST":
        brandname = request.POST['brandname']
        brandlogo = request.FILES.get('brandlogo')

        Brand.objects.create(brandname=brandname, brandlogo=brandlogo)
    return render(request, "add_brand.html", locals())

@login_required(login_url='/login_admin/')
def brand(request):
    data = Brand.objects.filter()
    mytype = request.GET.get('brandname')
    if mytype:
        data = data.filter(brandname=mytype)
    d = {'data': data}
    return render(request, "view_brand.html", d)

@login_required(login_url='/login_admin/')
def edit_brand(request, pid):
    if request.method == "POST":
        brandname = request.POST['brandname']

        try:
            brandlogo = request.FILES['brandlogo']
            br = Brand.objects.get(id=pid)
            br.brandlogo = brandlogo
            br.save()
        except:
            pass
        Brand.objects.filter(id=pid).update(brandname=brandname)
        messages.success(request, "Updated Successful")
        return redirect('view_brand')
    data = Brand.objects.get(id=pid)
    return render(request, "edit_brand.html", locals())

@login_required(login_url='/login_admin/')
def delete_brand(request, pid):
    data = Brand.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('view_brand')


@login_required(login_url='/login_admin/')
def add_product(request):
    brandid = request.GET.get('brandname', None)
    mybrand = None
    if brandid:
        mybrand = Brand.objects.filter(brandname=brandid)
    if request.method == "POST":
        typename = request.POST['typename']
        brandname = request.POST['brandname']
        productname = request.POST['productname']
        processor = request.POST['processor']
        screen = request.POST['screen']
        ram = request.POST['ram']
        storage = request.POST['storage']
        charges = request.POST['charges']
        rentalprice = request.POST['rentalprice']
        productmodel = request.POST['productmodel']
        description = request.POST['description']
        brandobj = Brand.objects.get(id=brandname)

        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')

        Product.objects.create(typename=typename, brandname=brandobj, productname=productname, processor=processor,
                               screen=screen, ram=ram, storage=storage, charges=charges, rentalprice=rentalprice,
                               productmodel=productmodel, description=description, image1=image1, image2=image2)
        return redirect('view_product')
    mybrand = Brand.objects.all()
    return render(request, "add_product.html", locals())

@login_required(login_url='/login_admin/')
def product(request):
    data = Product.objects.filter()
    mytype = request.GET.get('productname')
    if mytype:
        data = data.filter(productname=mytype)
    d = {'data': data}
    return render(request, "manage_product.html", d)

@login_required(login_url='/login_admin/')
def edit_product(request, pid):
    if request.method == "POST":
        typename = request.POST['typename']
        brandname = request.POST['brandname']
        productname = request.POST['productname']
        processor = request.POST['processor']
        screen = request.POST['screen']
        ram = request.POST['ram']
        storage = request.POST['storage']
        charges = request.POST['charges']
        rentalprice = request.POST['rentalprice']
        productmodel = request.POST['productmodel']
        description = request.POST['description']
        brandobj = Brand.objects.get(id=brandname)
        try:
            image1 = request.FILES['image1']
            c = Product.objects.get(id=pid)
            c.image1 = image1
            c.save()
        except:
            pass
        try:
            image2 = request.FILES['image2']
            c = Product.objects.get(id=pid)
            c.image2 = image2
            c.save()
        except:
            pass

        Product.objects.filter(id=pid).update(typename=typename, brandname=brandobj, productname=productname, processor=processor,
                               screen=screen, ram=ram, storage=storage, charges=charges, rentalprice=rentalprice,
                               productmodel=productmodel, description=description)
        messages.success(request, "Updated Successful")
        return redirect('view_product')
    data = Product.objects.get(id=pid)
    mybrand = Brand.objects.all()
    return render(request, "edit_product.html", locals())

@login_required(login_url='/login_admin/')
def delete_product(request, pid):
    data = Product.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('view_product')

@login_required(login_url='/user_login/')
def my_booking(request):
    userobj = Signup.objects.get(user=request.user)
    myproduct = Booking.objects.filter(user=userobj)
    return render(request, "my_booking.html", locals())

@login_required(login_url='/admin_login/')
def new_booking(request):
    user = request.GET.get('user')
    action = request.GET.get('action')
    if request.user.is_staff:
        myproduct = Booking.objects.filter()
    else:
        booking = Booking.objects.filter(user__user=request.user)
        data = Booking.objects.filter(typename=booking)
    if action == "New":
        data = myproduct.filter(status="pending")
    elif action == "Approved":
        data = myproduct.filter(status="Approved")
    elif action == "Unapproved":
        data = myproduct.filter(status="Unapproved")
    elif action == "Total":
        data = myproduct.filter()
    # if user:
    #     data = myproduct.filter(user__user__id=user)
    # d = {'data': myproduct}
    return render(request, "new_booking.html",locals())

@login_required(login_url='/user_login/')
def delete_booking(request, pid):
    data = Booking.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('my_booking')

@login_required(login_url='/user_login/')
def booking(request):
    data = Product.objects.all()
    data = Product.objects.filter()
    mytype = request.GET.get('productname')
    if mytype:
        data = data.filter(productname=mytype)
    d = {'data': data}
    return render(request, "my_booking.html", locals())

@login_required(login_url='/login_admin/')
def change_password(request):
    # user = User.objects.get(username=request.user.username)
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('/')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('change_password')

    return render(request,'change_password.html')

@login_required(login_url='/user_login/')
def user_change_password(request):
    # user = User.objects.get(username=request.user.username)
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('/')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('user_change_password')
    return render(request,'user_change_password.html')

def booking_detail(request, pid):
    data = Booking.objects.get(id=pid)
    booking = Booking.objects.get(id=pid)
    if request.method == "POST":
        remark = request.POST['remark']
        status = request.POST['status']
        data.status = status
        booking.status = status
        booking.save()
        data.save()
        Trackinghistory.objects.create(booking=data, remark=remark, status=status)
        messages.success(request, "Action Updated")
        return redirect('booking_detail', pid)
    traking = Trackinghistory.objects.filter(booking=data)
    if request.user.is_staff:
        return render(request, "booking_detail_admin.html", locals())
    else:
        return render(request, "mybooking_detail.html", locals())

def change_status(request, bid):
    book = Booking.objects.get(id=bid)
    if request.method == "POST":
        re = request.POST
        Booking.objects.filter(id=bid).update(status=re['status'])
        Trackinghistory.objects.create(booking=book, status=re['status'], remark=re['comment'])
        messages.success(request, "Status Updated")
    return redirect('booking_detail',bid)

@login_required(login_url='/admin_login/')
def admin_report(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']

        data = Booking.objects.filter(bookingdate__gte=fromdate, bookingdate__lte=todate)
        data2 = True

    return render(request, "admin_report.html", locals())

@login_required(login_url='/admin_login/')
def count_report(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']

        data = Booking.objects.filter(bookingdate__gte=fromdate, bookingdate__lte=todate)
        Total = Booking.objects.filter()
        data2 = True
    return render(request, "count_report.html",locals())

@login_required(login_url='/login_admin/')
def reg_user(request):
    data = Signup.objects.all()
    d = {'data': data}
    return render(request, "reg_user.html", d)

@login_required(login_url='/login_admin/')
def delete_user(request, pid):
    data = User.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('reg_user')

@login_required(login_url='/admin_login/')
def search_booking(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        data2 = True
        data = Booking.objects.filter(bookingnumber__icontains=fromdate)
    return render(request, "search_booking.html", locals())

from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Count, Sum
def report(request):
    data = None
    fromdate = None
    todate = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        req = request.POST.get('reqtype')
        print(fromdate)
        mont1 = int(fromdate.split('-')[1])
        mont2 = int(todate.split('-')[1])
        yer1 = int(fromdate.split('-')[0])
        yer2 = int(todate.split('-')[0])
        monthli = [i for i in range(mont1, mont2+1)]
        yearli = [i for i in range(yer1, yer2+1)]

    return render(request, "sales_report.html",locals())




