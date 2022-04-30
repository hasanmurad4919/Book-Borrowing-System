
from django.db import models
import datetime
import time 
from django.utils import timezone

# Create your models here.
class BorrowRules(models.Model):
    bor_period = models.IntegerField("borrow period", default=30)
    day_fine = models.DecimalField(max_digits=4,decimal_places=2,default=10.0)
    quota = models.IntegerField(default=5)

    def __str__(self):
        return ("perriod:{0},fine:{1},quota:{2}".format(self.bor_period,self.day_fine,self.quota))

class Account(models.Model):
    accoount_name = models.CharField("account name",max_length=20, unique=True)
    account_pwd = models.CharField("password",max_length=20)
    register_time = models.DateField("registered time", auto_now_add=True)
    #ccl_time = models.DateField("cancel time")
    ACCOUNT_STATUS_CHOICES = [
        ('CP', 'Check Pending'),
        ('N', 'Normal'),
        ('F', 'Freeze'),
        ('CA', 'Cancel'),
    ]
    account_satus = models.CharField("account status",max_length=2,choices=ACCOUNT_STATUS_CHOICES,default='N')
    bor_rules = models.ForeignKey(BorrowRules,on_delete=models.CASCADE)
    
    def keeping_num(self):
        num = self.borrow_set.filter(bor_status='K').count()
        return num
    keeping_num.admin_order_field='keeping_number'

    def current_fine(self):
        cufine = 0
        for i in self.borrow_set.filter(bor_status='K'):
            cufine = cufine+i.total_fine()
        return cufine
    current_fine.admin_order_field='current_fine'

    def fine_filt(self):
        return self.current_fine()<=100
    fine_filt.admin_order_field = 'fine_filt'
    fine_filt.boolean = True
    fine_filt.short_description = 'Is the fine under 100?'

    def __str__(self):
        return self.accoount_name
    


class Book(models.Model):
    isbn = models.CharField(max_length=40, unique=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=40)
    publisher = models.CharField(max_length=40)

    def storage(self):
        return self.bookinstance_set.count()
    storage.admin_order_field = 'storage'

    def avail(self):
        return self.bookinstance_set.filter(loan_status='A').count()
    avail.admin_order_field = 'available_num'

    def __str__(self):
        return ("{0}:{1}".format(self.isbn,self.title))

class BookReview(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    account = models.ForeignKey(Account,related_name='reviews', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    stars = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)



import uuid

class BookInstance(models.Model):
    uid = models.UUIDField(default=uuid.uuid4)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL,null=True)
    imprint = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=20, unique=True)
    LOAN_STATUS_CHOICE = [
        ('A', 'Available'),
        ('O', 'On Loan'),
    ]
    loan_status = models.CharField(max_length=1,choices=LOAN_STATUS_CHOICE, default='A')

    def __str__(self):
        return ('{0} ({1})'.format(self.book.title, self.location))

class Borrow(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    bookins = models.ForeignKey(BookInstance, on_delete=models.CASCADE)
    bor_time = models.DateField("borrow time", auto_now_add=True)
    
    BOR_STATUS_CHOICES = [
        ('K', 'keeping'),
        ('R', 'returned'),
    ]
    bor_status = models.CharField(max_length=1,choices=BOR_STATUS_CHOICES,default='K')
    f = models.DecimalField("Final Fine",max_digits=6,decimal_places=2,default=0)
    
    def loc(self):
        location = self.bookins.location
        return ('{}'.format(location))

    def ret_date(self):
        bp = self.account.bor_rules.bor_period
        return self.bor_time + datetime.timedelta(days=bp) 
    ret_date.admin_order_field = 'return_date'

    def is_expired(self):
        if self.bor_status == 'K':
            bp = self.account.bor_rules.bor_period
            return datetime.datetime.date(timezone.now())-datetime.timedelta(days=bp)<=self.bor_time
        else:
            return datetime.datetime.date(timezone.now())>=self.bor_time

    is_expired.admin_order_field = 'is_expired'
    is_expired.boolean = True
    is_expired.short_description = 'Is book still in borrow period?'


    def total_fine(self):
        bp = self.account.bor_rules.bor_period
        fi = self.account.bor_rules.day_fine
        if self.bor_status == 'K':
            expired_day = (datetime.datetime.date(timezone.now())-datetime.timedelta(days=bp)-self.bor_time).days
            if expired_day>0: 
                total_fine = expired_day * fi
                return ('{}'.format(total_fine))
            else :
                return 0
        else:
            return 0
    total_fine.admin_order_field = 'fine'


    @property
    def loca(self):
        return self.loc()

    @property
    def return_date(self):
        return self.ret_date()

    @property
    def expire(self):
        return self.expire()
    
    @property
    def fine(self):
        return self.total_fine()

    def __str__(self):
        return ('{}'.format(self.bookins.book.title))
