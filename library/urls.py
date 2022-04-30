
from django.urls import path

from . import views

app_name='library'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signup/results/', views.signres, name='signupresult'),
    path('home/', views.signin, name='home'),
    path('home/<slug:acc_name>/', views.pcenter, name='pcenter'),
    path('home/<slug:acc_name>/searchResult/', views.searchresults, name='searchresults'),
   path('home/<slug:acc_name>/bookreview/', views.bookreview, name='bookreview'),
    path('home/<slug:acc_name>/searchResult/book_id=<int:book_id>/', views.bookdetail, name='bookdetails'),
    path('home/<slug:acc_name>/searchResult/book_id=<int:book_id>/bookins_id=<int:bis_id>/', views.borrowoperate, name='borrow')
]
