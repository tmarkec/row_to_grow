from django.shortcuts import render, get_object_or_404, redirect
from .forms import SubscribeForm
from .models import Subscription
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.


def subscribe(request):
    """
    Function that handles subscription for the newsletter
    """
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You subscribed to our newsletter!")
            email = request.POST.get("email")
            subject = "Row to grow subscription"
            message = (
                "Thank you for subscribing to our newsletter,"
                + " you will get latest updates on our new products and deals!"
                + "Go back to ...."
            )
            from_email = "tmarkec@gmail.com"
            recipient_list = [email]
            send_mail(subject,
                      message, from_email, recipient_list, fail_silently=False)
            return redirect("/")
    else:
        form = SubcribeForm()

    context = {"form": form}
    return render(request, "index.html", context)