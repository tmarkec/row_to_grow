from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib import messages
from checkout.models import Order

def profile(request):
    """ Display the user's profile information """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
    form = UserProfileForm(instance=profile)

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'on_profile_page': True
    }

    return render(request, template, context)


def info(request):
    """ Display the user account options """
    
    template = 'profiles/personal_info.html'
    context = {
    }

    return render(request, template, context)


# def history(request):
#     """ Display the user previous orders """

#     orders = profile.orders.all()
#     template = 'profile/history.html'
#     context = {
#         'orders': orders,
      
#     }

#     return render(request, template, context)
def history(request):
    """Display the user's previous orders"""

    # Retrieve the current user's profile
    profile = get_object_or_404(UserProfile, user=request.user)

    # Retrieve all orders associated with the user's profile
    orders = Order.objects.filter(user_profile=profile).order_by('-date')

    # Render the template with the list of orders
    template = 'profiles/history.html'
    context = {'orders': orders}
    return render(request, template, context)