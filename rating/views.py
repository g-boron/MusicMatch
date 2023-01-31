from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Song, Voter
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, SongForm
from django.contrib.auth import authenticate, login as log_auth
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib import messages

# Create your views here.
def index(request):
    popular_songs = Song.objects.filter(is_published=True).order_by('-votes')[:5]
    message = '' 

    if popular_songs.count() == 0:
        message = 'There is no songs'

    return render(request, 'rating/index.html', {'popular_songs': popular_songs, 'message': message})


@login_required
def add_song(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.is_published = False
            song.user = request.user
            song.save()
            return redirect('index')
    else:
        form = SongForm()
    
    return render(request, 'rating/add_song.html', {'form': form})


@login_required
def vote(request):
    songs = Song.objects.all()
    for song in songs:
        song.voted = Voter.objects.filter(song=song, user=request.user).exists()
    
    return render(request, 'rating/vote.html', {'songs': songs})


@login_required
def click_vote(request, pk):
    song = get_object_or_404(Song, id=pk)
    
    if Voter.objects.filter(song=song, user=request.user).exists():
        Voter.objects.filter(song=song, user=request.user).delete()
        song.votes -= 1
    else:
        Voter.objects.create(song=song, user=request.user)
        song.votes += 1
    
    song.save()

    return HttpResponseRedirect(reverse('vote'))


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                log_auth(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('index')
            else:
                messages.error(request,"Invalid username or password!")
        else:
                messages.error(request,"Invalid username or password!")
    form = AuthenticationForm()

    return render(request, 'rating/login.html', {'login_form': form})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            log_auth(request, user)
            messages.success(request, "Registration successful." )

            return redirect("index")

        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = RegisterForm()

    return render (request, 'rating/register.html', context={"register_form":form})
