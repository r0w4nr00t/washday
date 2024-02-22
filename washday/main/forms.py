from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import Order


class LoginForm(forms.Form):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'id': 'username',
                                   'required': True
                               }))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'id': 'password',
                                   'required': True
                               }))


class RegisterForm(forms.Form):
    first_name = forms.CharField(label='Username',
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control',
                                     'id': 'username',
                                     'required': True
                                 }))

    last_name = forms.CharField(label='Username',
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'id': 'username',
                                    'required': True
                                }))

    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'id': 'username',
                                   'required': True
                               }))

    phone_number = PhoneNumberField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'phone_number',
            'required': True,
            'placeholder': '+263'
        }))

    email = forms.EmailField(label='Username',
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                                 'id': 'username',
                                 'required': True
                             }))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'id': 'password',
                                   'required': True
                               }))

    ...


class ContactForm(forms.Form):
    name = forms.CharField(label='Name',
                           widget=forms.TextInput(attrs={
                               'class': 'form-control',
                               'id': 'name',
                               'required': True,
                               'placeholder': 'Your Name'
                           }))

    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                                 'id': 'email',
                                 'required': True,
                                 'placeholder': 'Your Email'
                             }))

    subject = forms.CharField(label='Subject',
                              widget=forms.TextInput(attrs={
                                  'placeholder': 'Subject',
                                  'class': 'form-control',
                                  'id': 'subject',
                                  'required': True
                              }))

    message = forms.CharField(widget=forms.Textarea(
        attrs={
            'rows': 5,
            'placeholder': 'Message',
            'class': 'form-control',
            'id': 'message',
            'required': True
        }))


class SubscribeForm(forms.Form):
    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                                 'id': 'email',
                                 'required': True,
                                 'placeholder': 'Your Email'
                             }))
    pass


class OrderForm(forms.ModelForm):
    pickup_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    pickup_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))  # Set 'rows' attribute to control the height
    instruction = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}))  # Set 'rows' attribute to control the height

    class Meta:
        model = Order
        fields = ['pickup_date', 'pickup_time', 'priority', 'payment_method', 'address', 'instruction']
