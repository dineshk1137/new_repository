from django import forms
from .models import Rec
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}))
    first_name  = forms.CharField(label='', max_length='50', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'first Name'}))
    last_name = forms.CharField(label='', max_length='50', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1','password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm,self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        # self.fields['username']

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''

class AddEventForm(forms.ModelForm):
    title  = forms.CharField(required=True,label='', max_length='50', widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'Event Name'}))
    # first_name  = forms.CharField(required=False,label='', max_length='50', widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'first Name'}))
    # last_name = forms.CharField(required=False,label='', max_length='50', widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    address = forms.CharField(required=True,label='', max_length='50', widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'location'}))
    time = forms.TimeField(required=True,label='', widget=forms.widgets.TimeInput(attrs={'class':'form-control','placeholder':'time(H:M)'}))
    date = forms.DateField(required=True,label='', widget=forms.widgets.DateInput(attrs={'class':'form-control','placeholder':'date of Event(YYYY:MM:DD)'}))
    description = forms.CharField(required=True, label='', max_length='255', widget=forms.widgets.Textarea(attrs={'class':'form-control','placeholder':'Event Description'}))
    
    class Meta:
        model = Rec
        exclude = ("user","rsvp_users","first_name","last_name",)

    def save(self, commit=True):
        event = super().save(commit=False)
        user = self.request.user

        if user.is_authenticated:
            event.user = user
            event.first_name = user.first_name
            event.last_name = user.last_name

        if commit:
            event.save()
        return event
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AddEventForm, self).__init__(*args, **kwargs)
