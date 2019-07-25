# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
import datetime
from bucketlist.models import Tbl_wish
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UserForm, Tbl_wishForm#, UserProfileForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):

    context_dict = {'message': 'If you see this, you are ready',}

    return render(request, 'bucketlist/index.html', context_dict,)


def showSignUp(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
#        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid(): #and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
 
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

#            profile = profile_form.save(commit=False)
#            profile.user = user

#            profile.save()

            registered = True
        else:
            print(user_form.errors)#, profile_form.errors
    else:
        user_form = UserForm()
        #user_profile = UserProfileForm()
    return render(request, 'bucketlist/showSignUp.html', {'user_form': user_form, 'registered':registered},)

def Signin(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your bucketlist account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'bucketlist/Signin.html', {},)

@login_required
def restricted(request):
    return render(request, 'bucketlist/restricted.html', {'context': "Since you're logged in, you can see this text!",},)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def showAddWish(request):
    return render(request, 'bucketlist/addWish.html', )

@login_required
def castWishform(request):
    saved = False    
    if request.method == 'POST':
        tbl_wishform = Tbl_wishForm(data=request.POST)
#        profile_form = UserProfileForm(data=request.POST)
        if tbl_wishform.is_valid(): #and profile_form.is_valid():
            # Save the user's form data to the database.
            tbl_wishform.save(commit=False)
            saved = True 
            #return index(request)
        else:
            print(tbl_wishform.errors)#, profile_form.errors
    else:
        tbl_wishform = Tbl_wishForm()
        #user_profile = UserProfileForm()
    return render(request, 'bucketlist/castwish.html', {'tbl_wishform': tbl_wishform, 'saved': saved},)

@login_required
def sesslogin(request):
	m = User.objects.get(username=request.user)
	if User.objects.get(password=m.password).is_valid:
#            user = User.objects.get(username=request.POST['username'])

            #introduce to STORE SESSION

	#if m.password == request.POST['password']:
		request.session['wish_user_id'] = m.id
		return request.session['member_id']

@login_required
def addWish(request):
    saved = False
    if request.session.has_key("_auth_user_id"):
        _auth_user_id = request.session["_auth_user_id"]
        user = get_object_or_404(User, pk=_auth_user_id)

        if request.method == "POST":
        #GET the posted form
            MyTbl_wishForm = Tbl_wishForm(request.POST)
    #        MyTbl_wishForm = Tbl_wishForm(request.POST.get('tbl_wish.wish_user_id', None))
    #        MyTbl_wishForm = Tbl_wishForm(request.POST.get('tbl_wish.wish_date', None))
            if MyTbl_wishForm.is_valid():   # Django validation engine, making sure that the fields are required            
                #MyTbl_wishForm = MyTbl_wishForm.save(commit=False)
                tbl_wish = Tbl_wish()
                #tbl_wish.user.id = request.session['username_id']
                tbl_wish.wish_title = MyTbl_wishForm.cleaned_data['wish_title']
                tbl_wish.wish_description = MyTbl_wishForm.cleaned_data['wish_description']
    #            tbl_wish.wish_user_id = tbl_wish.id #request.session['wish_user_id']

                tbl_wish.wish_date = datetime.datetime.now()
                tbl_wish.user_id = user.id

                tbl_wish.save()
                

                # save
#                new_wish.save(commit=True)

                saved = True
    #            user = User.objects.get(username=request.POST['username'])

    #           request.session['username'] = user.id            #introduce to STORE SESSION
    #            return index(request)
    #        else:
    #            print(form.errors)
        else:
            MyTbl_wishForm = Tbl_wishForm()
    return render(request, 'bucketlist/saved.html', {'saved': saved})
#    return render(request, 'bucketlist/addWish.html', {'form': form})

class ShowAddedeWish(ListView):
    model  = Tbl_wish
    template_name= "myprofile.html"
    context_object_name = "wishDetails"

#isIndex = lambda (dict, id): if dict["id"] == id: return dict else: return False
def isIndex(dict, id):
    if dict["id"] == id: return dict
    else: return False

@login_required
def getWishById(request):

    wish_id = None
    wish_dict = {}

    if request.session.has_key("_auth_user_id"):

        _auth_user_id = request.session["_auth_user_id"]

        user = User.objects.get(id =_auth_user_id)
        wishes = Tbl_wish.objects.filter(user_id=user.id)

 
        if request.method == 'POST':
            print("POST")
            if 'id' in request.POST:
                wish_id = request.POST['id']
                
                
                for wish in wishes:
                    print(wish.id, wish.id)
                    if int(wish.id) == int(wish_id):
                
                      #wish = filter(lambda (wishes, wish_id): isIndex(wishes, wish_id), wishes)
                      #wish = wishes.objects.get(id=wish_id)
                      
                        print(wish_id, wish)
                        wish_dict = {
                        'id': wish.id,
                        'Title': wish.wish_title,
                        'Description': wish.wish_description,
                        'Date': wish.wish_date} 
                        response = JsonResponse(wish_dict, safe=False)

                        return HttpResponse(response)

#                except:
#                    pass
    response = JsonResponse(wish_dict, safe=False)
    
    return HttpResponse(response)

@login_required
def updateWish(request):
    if request.session.has_key("_auth_user_id"):

        _auth_user_id = request.session["_auth_user_id"]
       
        user = User.objects.get(id =_auth_user_id)
        Tbl_wish.objects.filter(user_id=user.id)

        if request.method == 'POST':
            wish_id = request.POST['id']
            wishinstance = get_object_or_404(Tbl_wish, id=wish_id)
            MyTbl_wishForm = Tbl_wishForm(request.POST or None, instance=wishinstance)
            if MyTbl_wishForm.is_valid():   # Django validation engine, making sure that the fields are required            
                
                print("Wish form", "OK")
#                Tbl_wish.objects.filter(user_id=user.id)
                tbl_wish = Tbl_wish.objects.get(id=wish_id)
                #tbl_wish.user.id = request.session['username_id']
                tbl_wish.wish_title = MyTbl_wishForm.cleaned_data['wish_title']
                tbl_wish.wish_description = MyTbl_wishForm.cleaned_data['wish_description']
                tbl_wish.id = wish_id
    #            tbl_wish.wish_user_id = tbl_wish.id #request.session['wish_user_id']
                tbl_wish.wish_date = datetime.datetime.now()
                tbl_wish.user_id = user.id
                tbl_wish.save()
                return JsonResponse({'status':'200'}, safe=False)
            else:
                print("Wish form", "Error")
                return JsonResponse({'status':'ERROR'}, safe=False)

    # except Exception as e:
    #     return json.dumps({'status':'Unauthorized access'})

@login_required
def deleteWish(request):
    result = None
    if request.session.has_key("_auth_user_id"):

        _auth_user_id = request.session["_auth_user_id"]
       
        user = User.objects.get(id =_auth_user_id)
        Tbl_wish.objects.filter(user_id=user.id)
        print("deleting")
        if request.method == 'POST':
            wish_id = request.POST['id']
            tbl_wish = Tbl_wish.objects.get(id=wish_id)
            tbl_wish.delete()
            print("deleted")
            result = JsonResponse({'status':'OK'}, safe=False)
        else:
            print("Wish form", "Error")
            result = JsonResponse({'status':'ERROR'}, safe=False)

    return HttpResponse(result)


def simulate_range(total, limit, pagination_per_page):     # No more needed alternative code found
    get_range = []
    num = total
    for i in range(0, num, limit):
        get_range.append((i, i+limit))


    get_range_ = get_range[:]

    get_range = list()
 
    num2 = int(len(get_range_))
    for j in range(0, num2, pagination_per_page):
        get_range.append((1+j, j+pagination_per_page))

    return get_range


def setPagination(range_, page):
    page = int(page)
    for index, v in enumerate(range_):
        for i in v:
            if page == i:
                return v

@login_required
def getWish(request):
    if request.session.has_key("_auth_user_id"):

        _auth_user_id = request.session["_auth_user_id"]

        user = User.objects.get(id =_auth_user_id)

        wishes = Tbl_wish.objects.filter(user_id=user.id)
        #wishes = user.wishes.filter(active=True, parent__isnull=True)
        wishes_dict = []


        limit = 3
        pages_display_per_page = 2

        total = len(wishes[:])

        paginator = Paginator(wishes, limit) # Show 25 contacts per page
        
        page = request.POST.get('page', '')
        if page == '1': page = ''

        newList = []
        
        try:
            wishes = paginator.page(page)
            newList.append({
                'has_previous' : wishes.has_previous(),
                'has_next' : wishes.has_next(),
                'previous_page_number' : wishes.previous_page_number(),
                'next_page_number' : wishes.next_page_number(),
                'start_index' : wishes.start_index(),
                'end_index' : wishes.end_index()

                })

        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            wishes = paginator.page(1)
            newList.append({
                'has_previous' : wishes.has_previous(),
                'has_next' : wishes.has_next(),
                'previous_page_number' : None,
                'next_page_number' : wishes.next_page_number() or None,
                'start_index' : wishes.start_index(),
                'end_index' : wishes.end_index()

                })

        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            wishes = paginator.page(paginator.num_pages)
            newList.append({
                'has_previous' : wishes.has_previous(),
                'has_next' : wishes.has_next(),
                'previous_page_number' : wishes.previous_page_number(),
                'next_page_number' : None,
                'start_index' : wishes.start_index(),
                'end_index' : wishes.end_index()

                })


        # range_ = simulate_range(total, limit)[:]
        # current_num = wishes.number

        # num_pos = int(len(range_)/current_num)
        # print(decode(num_pos), "page number")
        try:
            range_ = simulate_range(total, limit, pages_display_per_page)

            for wish in wishes:

                wish_dict = {
                    'id': wish.id,
                    'Title': wish.wish_title,
                    'Description': wish.wish_description,
                    'Date': wish.wish_date}
                wishes_dict.append(wish_dict)
            newList[0]['num_pages']= paginator.num_pages
            newList[0]["number"] = page if page else 1

            try:
                pag = setPagination(range_, page)
                newList[0]['upper_bound']= pag[1]
                newList[0]['lower_bound']= pag[0]
                #if pagination range in page 1 has '1', 
                #reset 'has_previous' and 'has_next'

                if pag[0] == 1 and pag[0]:
                    newList[0]['has_previous'] = False
                    newList[0]['has_next'] = True

            except (ValueError, TypeError):
                newList[0]['upper_bound']= pages_display_per_page
                newList[0]['lower_bound'] = 1


              
            newList.append(wishes_dict)
            
            response = JsonResponse(newList, safe=False)

            return HttpResponse(response)
        except Exception, e:
            return HttpResponseRedirect('error.html', error = str(e))    
            #re Create your views here.


def getAllWish(request):
    wishes_dict = []
    wishes = Tbl_wish.objects.order_by('id')[:]
    
    for wish in wishes:

        wish_dict = {
            'id': wish.id,
            'Title': wish.wish_title,
            'Description': wish.wish_description,
            'Date': wish.wish_date,
            'User': wish.user.username,
            'Email': wish.user.email}
        wishes_dict.append(wish_dict)
    response = JsonResponse(wishes_dict, safe=False)

    return HttpResponse(response)
    del reponse
    pass
    # except Exception, e:
    #     return HttpResponseRedirect('error.html', error = str(e))    



# def blog(request):
#     try:
#         all_pages = Story.pub_objects.all()
#         paginator = Paginator(all_pages, 10) # Show 25 contacts per page
        
#         page = request.GET.get('page', '')
        
#         try:
#             all_pages = paginator.page(page)
#         except PageNotAnInteger:
#             # If page is not an integer, deliver first page.
#             all_pages = paginator.page(1)
#         except EmptyPage:
#             # If page is out of range (e.g. 9999), deliver last page of results.
#             all_pages = paginator.page(paginator.num_pages)

#         context_dict= {'all_pages': all_pages}

#     except Story.DoesNotExist:
#         # We get here if we didn't find the specified category.
#         # Don't do anything - the template displays the "no category" message for us.
#         pass
    
#     return render(request, 'stathandle/blog.html', context_dict)
