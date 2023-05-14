from django.shortcuts import render


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def about(request):
    """ A view to return the about us page """
    return render(request, 'home/about_us.html')


def shipping(request):
    """ A view to display the shipping page """
    return render(request, 'home/shipping_return.html')


def privacy(request):
    """ A view to display the shipping page """
    return render(request, 'home/privacy.html')



