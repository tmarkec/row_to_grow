from django.shortcuts import render, redirect
from .forms import ContactForm


def contact(request):
    """
    view to display contact form
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')
    else:
        form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form})


def contact_success(request):
    """
    view to display succesfully submitting contact form
    """
    return render(request, 'contact/contact_success.html')
