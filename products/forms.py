from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """
    Form for creating comments
    """
    class Meta:
        # model = Review
        # fields = ['review_comment', 'rating']
        model = Review
        fields = ['review_comment', 'rating',]
        widgets = {
            'review_comment': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'review_comment': 'Write your review',
            'rating': 'Rating (out of 5)',
        }
        required = {
            'rating': False
        }