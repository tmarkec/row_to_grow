from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Review
from .forms import ReviewForm, ProductForm
from checkout.models import OrderLineItem
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product_id=product.id, approved=True)
    context = {
        'product': product,
        'reviews': reviews,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.warning(request, 'Only admin can access it!')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request, 'Failed to add product.' +
                         'Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.warning(request, 'Only admin can access it!')
        return redirect(reverse('home'))
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product.' +
                                    'Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.warning(request, 'Only admin can access it!')
        return redirect(reverse('home'))
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))


@login_required
def add_review(request, product_id):
    """ A view to add a review"""
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            rating = form.cleaned_data['rating']
            review_comment = form.cleaned_data['review_comment']
            review = Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                review_comment=review_comment,
                )
            review.save()
            messages.success(request, 'Thank you for your review,' +
                                      'it is waiting for the approval!')
        else:
            messages.warning(request, 'You must rate and review the product!')
        return redirect('product_detail', product_id=product.id)

    context = {
        'product': product,
        'form': form,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def del_review(request, review_id):
    """ A view to delete a review """
    user = request.user
    review = get_object_or_404(Review, id=review_id, user=user)
    if review.user == request.user:
        review.delete()
        messages.success(request, "Review deleted successfully.")
    return redirect('product_detail', product_id=review.product.id)


@login_required
def update_review(request, review_id):
    """A view to update user review"""
    user = request.user
    review = get_object_or_404(Review, id=review_id, user=user)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.approved = False
            review.updated_on = timezone.now()
            review.save()
            messages.success(request, 'Your review has been updated,' +
                                      'wait for the approval.')
            return redirect('product_detail', product_id=review.product.id)
    else:
        form = ReviewForm(instance=review)
    return render(request,
                  "products/update_review.html", {"form": form})
