from .models import Review
from django import forms


class ReviewForm(forms.ModelForm):
    """
    Form for creating comments
    """
    class Meta:
        model: Review
        fields: ['review', 'rating']