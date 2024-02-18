from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddEventForm
from .models import Rec

def home(request):
    events = Rec.objects.all()
    sort_order = request.GET.get('sort', 'asc')

    if sort_order == 'asc':
        events = Rec.objects.all().order_by('time')
    elif sort_order == 'desc':
        events = Rec.objects.all().order_by('-time')
    else:
        events = Rec.objects.all()
        
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            messages.success(request, ' u have logged in')
            return redirect('home')
        else:
            messages.success(request, 'there was an error')
            return redirect('home')
    else:
        return render (request, 'home.html', {'events':events})
    
def logout_user(request):
    logout(request)
    messages.success(request, 'u have been logged out')
    return redirect('home')

def reg_user(request):
    if request.method == 'POST':
        form =SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username= username, password= password)
            login(request, user)
            return redirect('home')
        else:
            return render (request, 'register.html', {'form':form})
    else:
        form = SignUpForm()
        return render (request, 'register.html', {'form':form})

def events(request, pk):
    if request.user.is_authenticated:
        events = Rec.objects.get(id=pk)
        return render(request, 'events.html', {'events': events})
    else:
        messages.success(request, 'you need to login first')
        return redirect('home')
    

def delete_events(request, pk):
    if request.user.is_authenticated:
        try:
            deletee = Rec.objects.get(id=pk)
            if request.user == deletee.user or request.user.is_staff:
                deletee.delete()
                messages.success(request, 'Deleted Successfully')
                return redirect('home')
            else:
                raise Http404("You do not have permission to delete this event.")
        except Rec.DoesNotExist:
            messages.error(request, 'Event does not exist')
            return redirect('home')
    else:
        messages.error(request, 'You need to login to delete events')
        return redirect('home')
    
def update_event(request, pk):
    if request.user.is_authenticated:
        current_event = Rec.objects.get(id=pk)
        if request.user == current_event.user or request.user.is_staff:
            form = AddEventForm(request.POST or None, instance=current_event)

            if request.method == 'POST':
                if form.is_valid():
                    form.save()
                    messages.success(request, "Event updated")
                    return redirect('home')

            return render(request, 'update_event.html', {'form': form, 'event': current_event})
        else:
            raise Http404("You do not have permission to update this event.")
    else:
        messages.success(request, "Must be logged in")
        return redirect('home')
    
def add_event(request):
    form = AddEventForm(request.POST or None, request=request)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_event = form.save(commit=False)
                add_event.user = request.user
                add_event.save()
                messages.success(request, "Event Added")
                return redirect('home')
        return render(request, 'add_event.html',{'form':form})
    else:
        messages.success(request, " Must be logged in")
        return redirect('home')
    
    
def RSVP(request, pk):
    if request.user.is_authenticated:
        event = Rec.objects.get(id=pk)
        if request.user in event.rsvp_users.all():
            messages.warning(request, "You have already RSVP'd to this event.")
        else:
            event.rsvp_users.add(request.user)
            messages.success(request, "RSVP successful.")

        return redirect('home')
    else:
        messages.success(request, "You must be logged in to RSVP.")
        return redirect('home')


def search_events(request):
    query = request.GET.get('q', '')
    if query:
        events = Rec.objects.filter(title__icontains=query) | Rec.objects.filter(address__icontains=query)
    else:
        events = Rec.objects.all()  # Retrieve all events if no query is provided

    return render(request, 'search_results.html', {'events': events, 'query': query})