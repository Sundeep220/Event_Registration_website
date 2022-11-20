from django.shortcuts import render,redirect
from .models import *
from .forms import SubmissionForm,CustomUserCreateForm,UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
    limit = request.GET.get('limit')
    if limit == None:
        limit = 20
    limit = int(limit)

    users = User.objects.filter(hackathon_participant=True)
    count = users.count()

    paginator = Paginator(users, 10)
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        users = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        users = paginator.page(page)

    pages = list(range(1, (paginator.num_pages + 1)))

    
    events = Event.objects.all()
    context = {'users': users,'events':events,'count': count,'paginator':paginator, 'pages':pages}
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
def edit_account(request,pk):
    user = User.objects.get(id=pk)
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request,'Account updated successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request,'user_form.html',context)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            hashed_password = make_password(password1)
            request.user.password = hashed_password
            request.user.save()
            messages.success(request, 'Password was changed!')
            return redirect('account')
    context = {}
    return render(request, 'change_password.html', context)

@login_required(login_url='login')
def project_submission(request, pk):
    event = Event.objects.get(id=pk)
    registered = request.user.events.filter(id=event.id).exists()
    form = SubmissionForm()
    if registered == True :
        if request.method == 'POST':
            form = SubmissionForm(request.POST)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.participant = request.user
                submission.event = event
                submission.save()
                return redirect('account')
    else:
        messages.error(request, 'Please first register for this event.')
        return redirect('event', pk=event.id)
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