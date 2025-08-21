from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Brand(models.Model):
    brandname = models.CharField(max_length=100, null=True, blank=True)
    brandlogo = models.FileField(max_length=100, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.brandname

class Product(models.Model):
    brandname = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    typename = models.CharField(max_length=100, null=True, blank=True)
    productname = models.CharField(max_length=100, null=True, blank=True)
    processor = models.CharField(max_length=100, null=True, blank=True)
    screen = models.CharField(max_length=100, null=True, blank=True)
    ram = models.CharField(max_length=100, null=True, blank=True)
    storage = models.CharField(max_length=100, null=True, blank=True)
    charges = models.CharField(max_length=100, null=True, blank=True)
    rentalprice = models.CharField(max_length=100, null=True, blank=True)
    productmodel = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    image1 = models.FileField(null=True, blank=True)
    image2 = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.typename

class About(models.Model):
   pagetitle = models.CharField(max_length=100, null=True, blank=True)
   description = models.CharField(max_length=100, null=True, blank=True)

class Contact(models.Model):
    pagetitle = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    contactno = models.CharField(max_length=100, null=True, blank=True)

class Signup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Booking(models.Model):
    user = models.ForeignKey(Signup, on_delete=models.CASCADE, null=True, blank=True)
    productname = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    bookingnumber = models.CharField(max_length=100, null=True, blank=True)
    fromdate = models.DateField(null=True, blank=True)
    todate = models.DateField(null=True, blank=True)
    typename = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(null=True, blank=True)

        # ✅ New Fields:
    payment_method = models.CharField(
        max_length=100,
        choices=[
            ('UPI', 'UPI'),
            ('Credit/Debit Card', 'Credit/Debit Card'),
            ('Wallet', 'Wallet'),
            ('GPay', 'GPay'),
            ('PhonePe', 'PhonePe'),
        ],
        null=True,
        blank=True
    )

    payment_screenshot = models.ImageField(upload_to='payment_proofs/', null=True, blank=True)

    bookingdate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    totalprice = models.CharField(max_length=100, null=True, blank=True)
    totaldays = models.CharField(max_length=100, null=True, blank=True)
    totalbooking = models.CharField(max_length=100, null=True, blank=True)
    saleamount = models.CharField(max_length=200, null=True, blank=True)
    monthyear = models.CharField(max_length=200, null=True, blank=True)
    year = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        return self.user.user.username+"  "+self.quantity

    def totalprice1(self):
        return (self.rentalprice) * int(self.quantity)


class Trackinghistory(models.Model):
    user = models.ForeignKey(Signup, on_delete=models.CASCADE, null=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
