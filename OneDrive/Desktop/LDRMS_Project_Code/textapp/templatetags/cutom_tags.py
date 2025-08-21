from django import template
from textapp.models import Booking

register = template.Library()

@register.simple_tag
def pendingbook(data, data2):
    pending = Booking.objects.filter(status='pending')
    return pending

@register.filter(name='findreportyear')
def findreportyear(year):
    data = Booking.objects.filter(bookingdate__year=year)
    total = 0
    for i in data:
        total += int(i.totalprice)
    return total

@register.filter(name='findreportmonth')
def findreportmonth(month):
    data = Booking.objects.filter(bookingdate__month=month)
    total = 0
    for i in data:
        total += int(i.totalprice)
    return total

@register.filter(name='findmonth')
def findmonth(month):
    li = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return li[month-1]