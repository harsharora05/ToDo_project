from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from base.models import list
from django.shortcuts import get_object_or_404
# Create your views here.


def home(request):

    if request.user.is_authenticated:
        currentUser = request.user
        notes = list.objects.filter(user=currentUser).all     
    else:
        notes = None

    context={'notes':notes}
        
    return render(request,'base_app/home.html',context)





def add_note(request):

    if request.method == 'POST':
        currentUser = request.user
        title = request.POST['title']
        note = request.POST['note']

        userNote=list(user=currentUser,title=title,textarea=note)
        userNote.save()
        return HttpResponseRedirect(reverse('home'))
    
    else:
        return HttpResponse('error-404')
    


@login_required
def detailView(request,id):

    data= get_object_or_404(list,pk=id)
    context = {'data':data}
    return render(request,'base_app/detailView.html',context)



def update_note(request,id):
    
    note = get_object_or_404(list,pk=id)

    if request.method == 'POST':
        title = request.POST['title']
        text = request.POST['note']

        note.title = title
        note.textarea = text
        note.user = request.user
        note.save()

        return HttpResponseRedirect(reverse('home'))



def delete_note(request,id):
    
    data = get_object_or_404(list,pk =id)
    if request.method =='POST':
        data.delete()
    return HttpResponseRedirect(reverse('home'))
    




def registration(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2 :
            print("password incorrect")

        elif User.objects.filter(username = username).first():
            print("use different username")

        else:
            user = User.objects.create_user(username,email,password1)
            user.first_name=fname
            user.last_name=lname
            user.save()

        return HttpResponseRedirect(reverse('home'))
        
    else:
        return HttpResponse("error-404")
    



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username ,password = password)

        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('User not found! please register')
    
    else:
        return HttpResponse('error-404')
    

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))





    
        

