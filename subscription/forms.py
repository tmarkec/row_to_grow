from django import forms
from .models import Subscription


class SubscribeForm(forms.ModelForm):
    """
    Form for subscribing to a newsletter.
    """

    class Meta:
        model = Subscription
        fields = [
            "email",
        ]