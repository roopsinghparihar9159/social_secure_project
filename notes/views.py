from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from notes.form import UserRegistrationForm,UserLoginForm,NoteForm
from django.contrib import messages
from notes.models import Note
from django.http import JsonResponse
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        form = NoteForm()
        notes = Note.objects.filter(user=request.user).order_by('-id')
        data={
            'form':form,
            'notes':notes
        }
        if request.method=="POST":
            title=request.POST.get('title')
            description=request.POST.get('description')
            print(title,description)
            note=Note()
            note.title=title
            note.description=description
            note.user=request.user
            note.save()
            notes = Note.objects.values().filter(user=request.user).order_by('-id')
            user_notes = list(notes)
            return JsonResponse({"status":"1","status_message":"Your note added successfully","notes":user_notes})
            
        return render(request,'notes/index.html',context=data)
    else:
        return redirect('Login')

def edit_note(request):
    edit_id = request.POST.get('edit_id')
    title = request.POST.get('title')
    description = request.POST.get('description')
    Note.objects.filter(id=edit_id).update(title=title,description=description)
    notes = Note.objects.values().filter(user=request.user).order_by('-id')
    user_notes = list(notes)
    return JsonResponse({"status":"1","status_message":"Your note updated successfully","notes":user_notes})

def delete_note(request):
    delete_id = request.GET.get('delete_id')
    Note.objects.filter(id=delete_id).first().delete()
    print(delete_id)
    notes = Note.objects.values().filter(user=request.user).order_by('-id')
    user_notes = list(notes)
    return JsonResponse({"status":"1","status_message":"Your note Deleted Successfully","notes":user_notes})

def signup(request):
    form = UserRegistrationForm()
    data = {
        'form':form,
    }
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        
        if(password != re_password):
            messages.add_message(request,messages.ERROR,'Password do not match')
        else:
            user = User.objects.create_user(username=username,password=password,email=email,first_name=name)
            if(user.is_active):
                print('Register')
                messages.add_message(request,messages.SUCCESS,'User register successfully')
                
            else:
                print('error')
    return render(request,'notes/signup.html',context=data)

def UserLogin(request):
    form = UserLoginForm()
    data={
        'form':form
    }
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(request,username=username,password=password)
        except:
            return JsonResponse({"status":"Invalid Credential"})

        if user is not None:
            login(request,user)
            print(user)
            return JsonResponse({"status":"User login Successully"})
        else:
            return JsonResponse({"status":"Invalid Credential"})
    return render(request,'notes/login.html',context=data)

def UserLogout(request):
    logout(request)
    return redirect('Login')