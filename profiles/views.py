from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from .forms import UserProfileForm


def profile(request):
    """ Display the user's profile information """
    profile = get_object_or_404(UserProfile, user=request.user)

    form = UserProfileForm(instance=profile)

    template = 'profiles/profile.html'
    context = {
        'form': form
    }

    return render(request, template, context)


def info(request):
    """ Display the user account options """
    
    template = 'profiles/personal_info.html'
    context = {
    }

    return render(request, template, context)


def history(request):
    """ Display the user account options """
    
    profile = get_object_or_404(UserProfile, user=request.user)
    orders = profile.orders.all()
    template = 'profiles/history.html'
    context = {
        'orders': orders
    }

    return render(request, template, context)