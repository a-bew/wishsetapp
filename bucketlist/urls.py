from django.conf.urls import url
from django.views.generic import TemplateView, ListView
from bucketlist.views import ShowAddedeWish
from . import views

app_name = 'Bucketlist' 
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^bucketlist/showSignUp/$', views.showSignUp, name='showSignUp'),
    url(r'^bucketlist/Signin/$', views.Signin, name='Signin'),
    url(r'^bucketlist/restricted/$', views.restricted, name='restricted'),
    url(r'^bucketlist/logout/$', views.user_logout, name='logout'),
    url(r'^bucketlist/addWish/$', views.showAddWish, name='showAddWish'),
    url(r'^bucketlist/castwish/$', views.castWishform, name='castWish'),
    url(r'^bucketlist/saved/$', views.addWish, name='saved'),
    url(r'^bucketlist/sess/$', views.sesslogin, name = 'sesslogin'),
    url(r'^bucketlist/ajax/getwish/$', views.getWish, name = 'getWish'),
    url(r'^bucketlist/ajax/getwishbyid/$', views.getWishById, name='getWishById'),
    url(r'^bucketlist/ajax/updatewish/$', views.updateWish, name='updateWish'),
    url(r'^bucketlist/ajax/deletewish/$', views.deleteWish, name='deleteWish'),
    url(r'^bucketlist/ajax/getallwish/$', views.getAllWish, name='getAllWish'),
    url(r'^myprofile/$', TemplateView.as_view(template_name='myprofile.html')),
    url(r'^angular1/$', TemplateView.as_view(template_name='angularone.html')),
#    url(r'^myprofile/$', ShowAddedeWish.as_view()),

]