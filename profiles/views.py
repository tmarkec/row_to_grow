from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from django.views import View
from .models import UserProfile, Wishlist
from .forms import UserProfileForm
from django.contrib import messages
from checkout.models import Order
from products.models import Product
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    """ Display the user's profile information """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'on_profile_page': True
    }

    return render(request, template, context)


@login_required
def info(request):
    """ Display the user account options """

    template = 'profiles/personal_info.html'
    context = {
    }

    return render(request, template, context)


@login_required
def history(request):
    """Display the user's previous orders"""

    profile = get_object_or_404(UserProfile, user=request.user)
    orders = Order.objects.filter(user_profile=profile).order_by('-date')
    template = 'profiles/history.html'
    context = {'orders': orders}
    return render(request, template, context)


@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    
    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'profiles/order_history.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all()
    context = {
        'wishlist': wishlist,
        'products': products,
    }
    template = 'profiles/wishlist.html'
    return render(request, template, context)


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    messages.success(request, 'You added item to wishlist!')
    return redirect('wishlist')
    # template = 'profiles/wishlist.html'
    # context = {
    # }

    # return render(request, template, context)


@login_required
def delete_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.products.remove(product)
    messages.success(request, 'You removed item from wishlist!')
    return redirect('wishlist')


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # important to update the session
            messages.success(request, 'Your password was successfully updated!')
            return redirect('info')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profiles/password_change.html', {'form': form})