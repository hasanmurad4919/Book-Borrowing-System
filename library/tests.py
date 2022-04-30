from django.test import TestCase

from .models import Account,Book,BorrowRules,Borrow,BookInstance,BookReview



class TestBorrowRules(TestCase):
   
    def testfields(self):
        b=BorrowRules()
        b.bor_period=30
        b.day_fine=10
        b.quota=5
        b.save()
        r=BorrowRules.objects.get(pk=1)
        self.assertEqual(r,b)


class TestBook(TestCase):
    def testbook(self):
        book=Book()
        book.isbn="4687687468"
        book.title="Satkahon"
        book.author="Somoresh Majumdar" 
        book.publisher="Janani"
        book.save()
        c=Book.objects.get(pk=1)
        self.assertEqual(c,book) 



      
class TestAccount(TestCase):
    def testkeeping_num(self):
        n=Account()
        n.accoount_name="bob@gmail.com"
        n.account_pwd="abcd4789"
        n.register_time="24-04-2021"
        n.account_satus='N'

        b=BorrowRules()
        b.bor_period=3
        b.day_fine=1
        b.quota=5
        b.save()
        n.bor_rules=b
        n.save()
        u=Account.objects.get(pk=1)
        self.assertEqual(u,n)

class TestReview(TestCase):

    def testf(self):
        r=BookReview()

        r.content="this book is good"
        r.stars=5
        r.date_added='24-02-2019'


        book=Book()
        book.isbn="4687687468"
        book.title="Satkahon"
        book.author="Somoresh Majumdar" 
        book.publisher="Janani"
        book.save()
        r.book=book

        n=Account()
        n.accoount_name="bob@gmail.com"
        n.account_pwd="abcd4789"
        n.register_time="24-04-2021"
        n.account_satus='N'
        b=BorrowRules()
        b.bor_period=3
        b.day_fine=1
        b.quota=5
        b.save()
        n.bor_rules=b
        n.save()
        r.account=n

        r.save()
        
        a=BookReview.objects.get(pk=1)
        self.assertEqual(a,r)

class TestBookInstances(TestCase):

    def testf(self):
        bi=BookInstance()
        bi.uid='bf47b4eb-f5e2-42ed-8631-bb5d3b96fb78'
        bi.imprint='copy1'
        bi.location='E.3.67.1'
        bi.loan_status='O'

        book=Book()
        book.isbn="4687687468"
        book.title="Satkahon"
        book.author="Somoresh Majumdar" 
        book.publisher="Janani"
        book.save()

        bi.book=book
        bi.save()

        s=BookInstance.objects.get(pk=1)
        self.assertEqual(s,bi)


class TestBRules(TestCase):
   
    def testf(self):
        b=BorrowRules()
        b.bor_period=3
        b.day_fine=1
        b.quota=5
        b.save()
        r=BorrowRules.objects.get(pk=1)
        self.assertEqual(r,b)
    

class TestBB(TestCase):
    def testbb(self):
        book=Book()
        book.isbn="46876687468"
        book.title="Ami Topu"
        book.author="Zafar Iqbal" 
        book.publisher="Anonno"
        book.save()
        c=Book.objects.get(pk=1)
        self.assertEqual(c,book) 



      
class TestAcc(TestCase):
    def testacc(self):
        n=Account()
        n.accoount_name="leo@gmail.com"
        n.account_pwd="abcd1289"
        n.register_time="24-04-2019"
        n.account_satus='N'

        b=BorrowRules()
        b.bor_period=7
        b.day_fine=5
        b.quota=10
        b.save()
        n.bor_rules=b
        n.save()
        u=Account.objects.get(pk=1)
        self.assertEqual(u,n)


class TestRvw(TestCase):

    def testrvw(self):
        r=BookReview()

        r.content="superb book"
        r.stars=5
        r.date_added='11-02-2019'


        book=Book()
        book.isbn="46876687468"
        book.title="Ami Topu"
        book.author="Zafar Iqbal" 
        book.publisher="Anonno"
        book.save()
        r.book=book

        n=Account()
        n.accoount_name="leo@gmail.com"
        n.account_pwd="abcd1289"
        n.register_time="24-04-2019"
        n.account_satus='N'
        b=BorrowRules()
        b.bor_period=3
        b.day_fine=1
        b.quota=5
        b.save()
        n.bor_rules=b
        n.save()
        r.account=n

        r.save()
        
        a=BookReview.objects.get(pk=1)
        self.assertEqual(a,r)

class TestBookIntns(TestCase):

    def testf(self):
        bi=BookInstance()
        bi.uid='c7853ec1-2ea3-4359-b02d-b54e8f1bcee2'
        bi.imprint='copy1'
        bi.location='E.4.67.1'
        bi.loan_status='O'

        book=Book()
        book.isbn="46876687468"
        book.title="Ami Topu"
        book.author="Zafar Iqbal" 
        book.publisher="Anonno"
        book.save()

        bi.book=book
        bi.save()

        s=BookInstance.objects.get(pk=1)
        self.assertEqual(s,bi)