from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.db.models import Count
def index(request):
    return render(request, 'wishapp/index.html')
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')

    user=User.objects.get(email=request.POST['email'])

    request.session['email']=request.POST['email']

    return redirect('/wishes')
def add(request):
    errors = User.objects.basic_validator(request.POST)
        # check if the errors object has anything in it

    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    
    else:
        # if the errors object is empty, that means there were no errors!
        # retrieve the user to be updated, make the changes, and save
        User.objects.Create_user(request.POST)

        request.session['email']=request.POST['email']

        messages.success(request, "User successfully added")
        # redirect to a success route
        return redirect('/wishes')
def wishes(request):
    if 'email' not in request.session:
        return redirect('/')
    context={
        'wishes':Wish.objects.all(),
        'user':User.objects.all().get(email=request.session['email'])
    }
    return render(request,'wishapp/wishes.html',context)
def new(request):
    if 'email' not in request.session:
        return redirect('/')
    user=User.objects.get(email=request.session['email'])
    context={
        'user':user
    }
    return render(request, 'wishapp/new.html',context)
def wishadd(request):
    if 'email' not in request.session:
        return redirect('/')
    errors = Wish.objects.basic_validator(request.POST)
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/wishes/new')
    else:
        user=User.objects.get(email=request.session['email'])
        Wish.objects.Create_wish(request.POST,user)
        messages.success(request, "Wish successfully added")
        return redirect('/wishes')
def grantwish(request,wishid):
    if 'email' not in request.session:
        return redirect('/')
    wish=Wish.objects.get(id=wishid)
    wish.granted=True
    wish.save()
    return redirect('/wishes')
def like(request,wishid,userid):
    if 'email' not in request.session:
        return redirect('/')
    wish=Wish.objects.get(id=wishid)
    user=User.objects.get(id=userid)
    if wish.author_id is user.id:
        return redirect('/wishes')
    try:
        Check_if_Liked = wish.likes.get(user_id=userid,post_id=wishid)
    except:
        flag=False
    if flag is False:
        wish.likes.add(user)
    return redirect('/wishes')

def editwish(request,wishid):
    if 'email' not in request.session:
        return redirect('/')
    context={
        'user':User.objects.get(email=request.session['email']),
        'wish':Wish.objects.get(id=wishid)
    }
    return render(request, 'wishapp/editwish.html',context)
def updatewish(request,wishid):
    if 'email' not in request.session:
        return redirect('/')
    errors = Wish.objects.basic_validator(request.POST)
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/wishes/edit/'+str(wishid))
    else:
        Wish.objects.Update_wish(request.POST,wishid)
        messages.success(request, "Wish successfully added")
        return redirect('/wishes')
def delete(request,wishid):
    if 'email' not in request.session:
        return redirect('/')
    Wish.objects.Delete_wish(wishid)
    return redirect('/wishes')
def stats(request):
    if 'email' not in request.session:
        return redirect('/')
    user=User.objects.get(email=request.session['email'])
    context={
        'user':user,
        'grantedwishes':Wish.objects.annotate(x=Count('granted')).filter(granted=True),
        'usergranted':Wish.objects.annotate(x=Count('granted')).filter(granted=True,author=user),
        'userpending':Wish.objects.annotate(x=Count('granted')).filter(granted=False,author=user)
    }
    return render(request, 'wishapp/stats.html', context)
def logout(request):
    del request.session['email']
    return redirect('/')