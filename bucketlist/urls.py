from django.conf.urls import url
from django.views.generic import TemplateView, ListView
from bucketlist.views import ShowAddedeWish
from . import views

app_name = 'Bucketlist' 
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^showSignUp/$', views.showSignUp, name='showSignUp'),
    url(r'^Signin/$', views.Signin, name='Signin'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^addWish/$', views.showAddWish, name='showAddWish'),
    url(r'^castwish/$', views.castWishform, name='castWish'),
    url(r'^saved/$', views.addWish, name='saved'),
    url(r'^sess/$', views.sesslogin, name = 'sesslogin'),
    url(r'^ajax/getwish/$', views.getWish, name = 'getWish'),
    url(r'^ajax/getwishbyid/$', views.getWishById, name='getWishById'),
    url(r'^ajax/updatewish/$', views.updateWish, name='updateWish'),
    url(r'^ajax/deletewish/$', views.deleteWish, name='deleteWish'),
    url(r'^ajax/getallwish/$', views.getAllWish, name='getAllWish'),
    url(r'^myprofile/$', TemplateView.as_view(template_name='myprofile.html')),
    url(r'^angular1/$', TemplateView.as_view(template_name='angularone.html')),
#    url(r'^myprofile/$', ShowAddedeWish.as_view()),

]