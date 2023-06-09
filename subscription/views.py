from django.shortcuts import render, get_object_or_404, redirect
from .forms import SubscribeForm
from .models import Subscription
from django.contrib import messages
from django.core.mail import send_mail


def subscribe(request):
    """
    Function that handles subscription for the newsletter
    """
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "You subscribed to our newsletter!")
            email = request.POST.get("email")
            subject = "Row to grow subscription"
            message = (
                "Thank you for subscribing to our newsletter,"
                + " you will get latest updates on our new products and deals in upcoming email!"
                + " Now come along and join us on our journey and check our producst"
                + " https://row-to-grow.herokuapp.com/."

            )
            from_email = "rowtogrow1@gmail.com"
            recipient_list = [email]
            send_mail(subject,
                      message, from_email, recipient_list, fail_silently=False)
            return redirect("/")
    else:
        form = SubcribeForm()

    context = {"form": form}
    return render(request, "index.html", context)
