import json
import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session  # noqa: F401
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import ContactForm, LoginForm, OrderForm, RegisterForm, SubscribeForm
from .models import BagDetail, LaundryItem, Order, User

pickup_data: dict = {}
bag_data: dict = {}


def get_or_create_user_bag(request):
    bag_data = request.session.get('bag_data', {})
    if not bag_data:
        bag_data = {'bag_details': [], 'total_items': 0, 'total_price': 0.0}
        request.session['bag_data'] = bag_data
    return bag_data


def order_number_generator():
    # Generate a random 10-digit number
    random_number = random.randint(10**9, (10**10) - 1)
    return random_number


def index(request):
    return render(request, 'main/index.html', {
        'form': ContactForm(),
        'subscribeForm': SubscribeForm(),
    })


def clientlogin(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('main:dashboard'))
            else:
                return HttpResponse('Sorry that did not work please try again ')

        else:
            return render(request, 'main/pages-login.html', {'form': form})
        ...
    return render(request, 'main/pages-login.html', {'form': LoginForm()})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']

            try:
                user = User.objects.create_user(  # noqa: F841
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=password,
                    phone=phone_number,
                ),
            except ImportError:
                return HttpResponse('User already exists')

        else:
            return render(request, 'main/pages-register.html', {'form': form})

    return render(request, 'main/pages-register.html', {'form': RegisterForm()})


@login_required(login_url='/pages/login')
def client_dashboard(request):
    user_orders = Order.objects.filter(user=request.user)
    return render(request, 'main/client_dashboard/index.html', {'orders': user_orders})


def bag(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        bag_details = data.get('bagDetails')
        total_items = int(data.get('totalItems'))
        total_price = float(data.get('totalPrice'))
        # Store bag data in session
        request.session['bag_data'] = {
            'bag_details': bag_details,
            'total_items': total_items,
            'total_price': total_price
        }
        return JsonResponse({'message': 'success'})
    elif request.method == 'GET':
        all_items = LaundryItem.objects.all()
        categories = {}
        for item in all_items:
            category_name = item.category
            if category_name == 'Household Linen':
                category_name = 'Household'
            if category_name not in categories:
                categories[category_name] = []
            categories[category_name].append(item)
        return render(request, 'main/client_dashboard/components-tabs.html', {'categories': categories})


def new_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            pickup_date = form.cleaned_data['pickup_date']
            pickup_time = form.cleaned_data['pickup_time']
            address = form.cleaned_data['address']
            instruction = form.cleaned_data['instruction']
            priority = form.cleaned_data['priority']
            payment_method = form.cleaned_data['payment_method']
            # Retrieve bag data from session
            bag_data = request.session.get('bag_data', {})
            place_order(
                bag_data, {
                    'pickup_date': pickup_date,
                    'pickup_time': pickup_time,
                    'address': address,
                    'instruction': instruction,
                    'priority': priority,
                    'payment_method': payment_method,
                }, request.user)
            # Clear the bag data from session after placing the order
            request.session['bag_data'] = None
            return HttpResponseRedirect(reverse('main:dashboard'))
        else:
            return render(request, 'main/client_dashboard/forms-element.html', {'form': form})
    return render(request, 'main/client_dashboard/forms-elements.html', {'form': OrderForm()})


def place_order(bag_data, pickup_data, user):
    order_ID = order_number_generator()
    order = Order.objects.create(orderID=order_ID,
                                 pickup_date=pickup_data['pickup_date'],
                                 pickup_time=pickup_data['pickup_time'],
                                 user=user,
                                 priority=pickup_data['priority'],
                                 payment_method=pickup_data['payment_method'],
                                 address=pickup_data['address'],
                                 instruction=pickup_data['instruction'],
                                 total_items=int(bag_data['total_items']),
                                 total_price=float(bag_data['total_price']),
                                 order_status='Pending',
                                 payment_status='Pending')
    for detail_data in bag_data['bag_details']:
        itemID = detail_data['item_id']
        item = LaundryItem.objects.get(itemID=itemID)
        quantity = detail_data['quantity']
        price = item.unit_price * quantity
        BagDetail.objects.create(order=order, item=item, quantity=quantity, price=price)

    amount = float(bag_data['total_price'])
    message = f""" New order from {user.username} orderID: {order_ID}
    Pickup Date : {pickup_data['pickup_date']}
    Pickup Time: {pickup_data['pickup_time']}
    Priority: {pickup_data['priority']}
    Payment Method: {pickup_data['payment_method']}
    Address: {pickup_data['address']}
    Instruction: {pickup_data['instruction']}
    Total Price: ${amount}
    Payment Status: Pending
    """
    subject = f'New order from {user.username} orderID: {order_ID}'
    send_mail(
        subject,
        message,
        'r0w4nr00t@gmail.com',
        ['jordanmarumure@gmail.com', 'hitol.homes@gmail.com'],
        fail_silently=False,
    )


@login_required(login_url='/pages/login')
def handle_payment():
    ...


@login_required(login_url='/pages/login')
def profile(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'main/client_dashboard/users-profile.html', {'user': user})


def help_center(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            subject = subject + ' - ' + email + ' - ' + name
            message = form.cleaned_data['message']

            send_mail(
                subject,
                message,
                'r0w4nr00t@gmail.com',
                ['jordanmarumure@gmail.com'],
                fail_silently=False,
            )
            return render(request, 'main/client_dashboard/pages-contact.html', {'message': 'success'})

    return render(request, 'main/client_dashboard/pages-contact.html', {
        'form': ContactForm(),
    })


@login_required(login_url='/pages/login')
def billing(request):
    return render(request, 'main/client_dashboard/pages-blank.html')


@login_required(login_url='/pages/login')
def view_bag(request, orderID):
    # Retrieve the Order object based on the provided orderID
    order = get_object_or_404(Order, orderID=orderID)

    # Access the bag details associated with the order
    bag_details = order.bag_details.all()
    return render(request, 'main/client_dashboard/pages-bag.html', {'order': order, 'bag_details': bag_details})


@login_required(login_url='/pages/login')
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:clientlogin'))


def about(request):
    return HttpResponse('This is the about page')


def blog(request):
    return HttpResponse('Blog Page')


def glossary(request):
    return HttpResponse('Glossary Page')


def faq(request):
    return HttpResponse('faq page')


def terms(request):
    return HttpResponse('Terms of Use')


def privacy_policy(request):
    return HttpResponse('Privacy Policy ')
