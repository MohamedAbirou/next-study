from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RoomForm, MessageForm, UserForm, MyUserCreationForm
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import *
import time



# Create your views here.
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    

    if request.method == 'POST':
        email = request.POST['email'].lower()
        password = request.POST['password']

        try:
            user = CustomUser.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials!')

    context = {"page": page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong with registration!')


    context = {"form": form}
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)
    )

    topics = Topic.objects.all()[:5]
    my_topics = Topic.objects.all()
    total_rooms = sum([topic.room_set.count() for topic in my_topics])
    room_count = rooms.count()
    recent_activities = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by('-created')[:5]

    context = {"rooms": rooms, "topics": topics, "room_count": room_count, "recent_activities": recent_activities, "total_rooms": total_rooms}
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body'),
                timestamp=int(time.time()), # Store creating time as Unix timestamp
            )
        room.participants.add(request.user)
        return redirect('room', room.id)
    
    context = {"room": room, "room_messages": room_messages, "participants": participants}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    # Get the message
    message = get_object_or_404(Message, id=pk)

    # Check if the current user is the author of the message
    if request.user == message.user:
        # Delete the message
        message.delete()
        return redirect('room', pk=message.room.id)

    else:
        # If the user is not the author of the message, show an error page or message
        return render(request, 'error.html', {'message': 'You do not have permission to delete this message.'})

@login_required(login_url='login')
def userProfile(request, pk):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    user = CustomUser.objects.get(id=pk)
    # Filter rooms hosted by the user
    rooms_hosted = user.room_set.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q)
    )
    
    # Filter rooms in which the user participates, excluding rooms hosted by the user
    rooms_participating = Room.objects.filter(
        Q(participants=user) &
        (Q(topic__name__icontains=q) | Q(name__icontains=q))
    )
    
    activities = user.message_set.all().order_by('-created')
    topics = Topic.objects.all()
    user_rooms_per_topic = {topic.name: topic.room_set.filter(host=user).count() for topic in topics}
    total_rooms = sum(user_rooms_per_topic.values())

    context = {
        'user': user,
        'rooms_hosted': rooms_hosted,  # Rooms hosted by the user
        'rooms_participating': rooms_participating,  # Rooms in which the user participates
        'activities': activities,
        'topics': topics,
        'total_rooms': total_rooms,
        'user_rooms_per_topic': user_rooms_per_topic
    }
    
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )

        return redirect('home')

    context = {"form": form, "topics": topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()

        return redirect('home')

    context = {"form": form, "topics": topics, "room": room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {"obj": room}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def updateMessage(request, pk):
    message = get_object_or_404(Message, id=pk)
    form = MessageForm(instance=message)

    if request.user != message.user:
        return render(request, 'error.html', {'message': 'You do not have permission to edit this message.'})

    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('room', message.room.id)

    context = {"form": form}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = get_object_or_404(Message, id=pk)

    if request.user != message.user:
        return render(request, 'error.html', {'message': 'You do not have permission to delete this message.'})

    if request.method == 'POST':
        message.delete()
        return redirect('room', message.room.id)

    context = {"obj": message}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {
        "form": form
    })

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    total_rooms = sum([topic.room_set.count() for topic in topics])
    return render(request, 'base/topics.html', {"topics": topics, "total_rooms": total_rooms})

def activityPage(request):
    activities = Message.objects.all()
    return render(request, 'base/activity.html', {"activities": activities})