from django import forms
from .models import Review, Product, Category
from .widgets import CustomClearableFileInput


class ReviewForm(forms.ModelForm):
    """
    Form for creating comments
    """
    class Meta:
        model = Review
        fields = ['review_comment', 'rating', ]
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


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    image = forms.ImageField(
        label="Image", required=False, widget=CustomClearableFileInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields["category"].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "border-black rounded-0"
