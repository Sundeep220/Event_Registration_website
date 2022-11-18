from django.shortcuts import render,redirect
from .models import *
from .forms import SubmissionForm,CustomUserCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.

def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist!')
            
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have succesfully logged in.')
            return redirect('home')
        else:
             messages.error(request, 'Username or password doesnot exist')
    context = {'page': page}
    return render(request, 'login_register.html',context)


def register_page(request):
    page = 'register'
    form = CustomUserCreateForm()

    if request.method == 'POST':
        form = CustomUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            user.save()
            login(request, user)
            messages.success(request, 'User account was created!')
            return redirect('home')
        else: 
             messages.error(request, 'An error occurred during registration')

    context = {'form': form, 'page': page}
    return render(request, 'login_register.html', context)


def logout_request(request): 
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')


def home_page(request):
    users = User.objects.filter(hackathon_participant=True)
    events = Event.objects.all()
    context = {'users': users,'events':events}
    return render(request, 'home.html',context)


def event_page(request, pk):
    event = Event.objects.get(id=pk)
    # if user is not logged in
    registered = False
    submitted = False
    if request.user.is_authenticated:

        registered = request.user.events.filter(id=event.id).exists()
        submitted = Submission.objects.filter(participant=request.user, event=event).exists()
    context = {'event': event, 'registered':registered, 'submitted':submitted}
    return render(request, 'event.html',context)

@login_required(login_url='login')
def registration_confirmation(request,pk):
    event = Event.objects.get(id=pk)
    if request.method == 'POST':
        event.participants.add(request.user)
        return redirect('event', pk = event.id)


    context = {'event': event}
    return render(request, 'event_confirmation.html',context)

@login_required(login_url='login')
def user_page(request ,pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def account_page(request):
    user = request.user
    context = {'user': user}
    return render(request, 'account.html', context)

@login_required(login_url='login')
def project_submission(request, pk):
    event = Event.objects.get(id=pk)
    form = SubmissionForm()
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.participant = request.user
            submission.event = event
            submission.save()
            return redirect('account')
    context = {'event': event, 'form': form}
    return render(request, 'submit_form.html', context)

@login_required(login_url='login')
def update_submission(request, pk):
    submission = Submission.objects.get(id=pk)
    event = submission.event

    if request.user != submission.participant:
        return HttpResponse('You cant be here!!!!')

        
    form = SubmissionForm(instance=submission)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form, 'event': event}
    return render(request, 'submit_form.html',context)