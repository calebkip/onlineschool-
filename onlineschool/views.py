from ast import IsNot
from email import message
from pydoc_data.topics import topics
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
from django.http import HttpResponse
from .models import Room,Topic,Message
from django.db.models import Q
from .forms import RoomForm




def loginPage(request):
    page='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method =='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'user does not exist')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username does not exist')

    context={'page':page}
    return render (request,'onlineschool/login_register.html',context)
def logoutUser(request):
    logout(request)
    return  redirect ('home')
def registerPage(request):
    form=UserCreationForm(request.POST)
    if form.is_valid():
        user=form.save(commit=False)
        user.username=user.username.lower()
        user.save()
        login(request,user)
        return redirect('home')
    else:
        messages.error(request,'wrong credentials')
    return render(request,'onlineschool/login_register.html',{'form':form})

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q) 
    )
    topics=Topic.objects.all()
    roomCount=rooms.count()
    room_messages=Message.objects.all().filter(Q(room__topic__name__icontains=q))
    context ={'rooms':rooms,'topics':topics,'roomCount':roomCount,'room_messages':room_messages}
    return render (request,'onlineschool/home.html',context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    # topics=Topic.objects.all()
    roomMessages=room.message_set.all()
    participants=room.participants.all()
    if request.method =='POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')

        )
        room.participants.add(request.user)
    # return redirect('room',pk=room.id)
    context={'room':room,'topics':topics,'roomMessages':roomMessages,'participants':participants}
    return render (request ,'onlineschool/room.html',context)   

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms= user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={ 'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render (request,'onlineschool/profile.html',context)    
@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    if request.method =='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
           room=form.save(commit=False)
           room.host=request.user 
           room.save()
           return redirect('home')
    context={'form':form}
    return render(request,'onlineschool/roomform.html',context)    
@login_required(login_url='login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form =RoomForm(instance=room)
    if request.user  != room.host: 
        return HttpResponse('you are an intruder here') 
    if request.method =='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'onlineschool/roomform.html',context)
@login_required(login_url='login')
def deleteRoom(request,pk):
    if request.user  != room.host: 
        return HttpResponse('you are an intruder here') 
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'onlineschool/delete.html',{'obj':room})
# @login_required(login_url='login')
# def update_message(request,pk):
#     message=Message.objects.get(id=pk)
#     form =RoomForm(instance=room)
#     if request.user  != room.host: 
#         return HttpResponse('you are an intruder here') 
#     if request.method =='POST':
#         form=RoomForm(request.POST,instance=room)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     context={'form':form}
#     return render(request,'onlineschool/roomform.html',context)   

@login_required(login_url='login')
def delete_message(request,pk):
    message=Message.objects.get(id=pk)
    if request.user  != message.user: 
        return HttpResponse('you are an intruder here') 
    
    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request,'onlineschool/delete.html',{'obj':message})