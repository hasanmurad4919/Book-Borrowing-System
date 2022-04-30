
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# Create your views here.
from .models import Account,Book,BorrowRules,Borrow,BookInstance,BookReview

def index(request):

    return render(request, 'library/index.html')


def signup(request):
    return render(request, 'library/signup.html')

def signres(request):
    acc_name = request.POST['new_name']
    pwd = request.POST['new_pwd']
    if (len(acc_name) == 0 or len(pwd) == 0):
        infos = 'The account name and password should not be null'
        return render(request,'library/successcreate.html',{'infos':infos,})
    else: 
        try:
            acc = Account.objects.get(accoount_name=acc_name)
        except Account.DoesNotExist:  
            new_account = Account.objects.create(accoount_name=acc_name, account_pwd=pwd, bor_rules_id=1)
            new_account.save()
            return render(request, 'library/successcreate.html')
        else:
            infos = 'The account has been register'
            return render(request,'library/successcreate.html',{'infos':infos,})
                


from django.contrib import messages

def signin(request):
    acc_name = request.POST['acc_name']
    pwd = request.POST['acc_pwd']
    try: 
        acc = Account.objects.get(accoount_name = acc_name)
    except Account.DoesNotExist:
        messages.error(request, 'The ACCOUNT IS INCORRECT OR DOES NOT EXIST, PLEASE TRY AGAIN!')
        return render(request, 'library/index.html')
    else:
        if pwd == acc.account_pwd:
            context = {'account': acc,}
            return render(request, 'library/home.html', context)
        else:
            messages.error(request, 'PASSWORD IS WRONG, PLEASE TRY AGAIN!')
            return render(request, 'library/index.html')


def pcenter(request, acc_name):

    acc = Account.objects.get(accoount_name = acc_name)
    keeping_list = acc.borrow_set.filter(bor_status='K')
    returned_list = acc.borrow_set.filter(bor_status='R')

    context = {'acc':acc,'keeping_list':keeping_list,  'returned_list':returned_list}
    return render(request, 'library/pcenter.html', context)

def searchresults(request, acc_name):
    acc = Account.objects.get(accoount_name = acc_name)
    s = request.POST['s']
    choice = request.POST.get('choice')
    if choice == 'i':
        book_list = Book.objects.filter(isbn__icontains=s)
    elif choice == 'a':
        book_list = Book.objects.filter(author__icontains=s)
    else:
        book_list = Book.objects.filter(title__icontains=s)

    context = {'book_list':book_list, 'acc':acc, 'choice':choice, 's':s, }
    return render(request, 'library/searchResults.html', context)

def bookdetail(request, acc_name, book_id):
    book = Book.objects.get(id=book_id)
    book_ins = book.bookinstance_set.all()
    acc = Account.objects.get(accoount_name = acc_name)
    context={'book':book, 'book_ins':book_ins, 'acc':acc,}
    return render(request, 'library/bookdetails.html',context)

def bookreview(request, acc_name):
    acc = Account.objects.get(accoount_name = acc_name)
    bookreview=BookReview.objects.all()
    context = {'acc':acc,"bookreview":bookreview}
    return render(request, 'library/bookreview.html', context)


def borrowoperate(request, acc_name, book_id, bis_id):
    acc = Account.objects.get(accoount_name = acc_name)
    book_ins = BookInstance.objects.get(id = bis_id)
    book = Book.objects.get(id = book_id)
    quota = acc.bor_rules.quota
    
    if acc.account_satus in ['CP','F','CA']:
        infos = 'Your Account Status isn\'t Normal.Please contact the staff.'
        context={'book':book, 'book_ins':book_ins,'acc':acc,'infos':infos,}
        return render(request, 'library/test.html', context)
    else:         
        if (acc.keeping_num()<quota):
            borr_record = acc.borrow_set.create(bookins_id=bis_id)
            book_ins.loan_status='O'
            borr_record.save()
            book_ins.save()
            context={'book':book, 'book_ins':book_ins,'acc':acc,}
            return render(request, 'library/test.html',context)
        else:
            #messages.error(request, 'Borrowing has reached the limit')
            infos = 'Borrowing has reached the limit'
            context={'book':book, 'book_ins':book_ins,'acc':acc,'infos':infos,}
            return render(request, 'library/test.html', context)


