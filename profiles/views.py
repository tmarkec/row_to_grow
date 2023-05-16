from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from .models import UserProfile, Wishlist
from .forms import UserProfileForm
from django.contrib import messages
from checkout.models import Order
from products.models import Product
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


@login_required
def profile(request):
    """
    Display the user's profile information
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.info(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed.' +
                                    'Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'on_profile_page': True
    }

    return render(request, template, context)


@login_required
def info(request):
    """ Display the user account options """

    template = 'profiles/personal_info.html'
    context = {
    }

    return render(request, template, context)


@login_required
def history(request):
    """Display the user's previous orders"""

    profile = get_object_or_404(UserProfile, user=request.user)
    orders = Order.objects.filter(user_profile=profile).order_by('-date')
    template = 'profiles/history.html'
    context = {'orders': orders}
    return render(request, template, context)


def order_history(request, order_number):
    """
    view to display order history
    """
    order = get_object_or_404(Order, order_number=order_number)
    context = {
        'order': order,
        'from_profile': True,
    }
    if request.GET.get('download_pdf'):
        response = download_order_pdf(request, order_number)
        return response

    return render(request, 'profiles/order_history.html', context)


def generate_pdf(order):

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont('Helvetica-Bold', 24)
    p.drawCentredString(300, 790, "Row to grow PDF receipt")
    p.setFont('Helvetica', 16)
    p.drawCentredString(300, 760, "Order History")
    p.drawString(50, 720, f"Order Number: {order.order_number}")
    p.drawString(
        50, 690, f"Order Date: {order.date.strftime('%Y-%m-%d %H:%M:%S')}")
    p.drawString(50, 660, f"Full name: {order.full_name}")
    p.drawString(50, 630, f"Email: {order.email}")
    p.drawString(50, 600, f"Address: {order.street_address1},")
    p.drawString(120, 570, f"{order.county},")
    p.drawString(120, 540, f"{order.country}")
    p.setFont('Helvetica-Bold', 16)
    p.drawString(50, 500, f"Total: €{order.grand_total}")
    p.setFont('Helvetica', 16)
    p.drawString(50, 450, "Order Items:")
    y = 430
    for item in order.lineitems.all():
        p.setFont('Helvetica', 12)
        p.drawString(
            50, y, f'{item.product.name} x {item.quantity} @' +
                   '{item.product.price}')
        y -= 15

    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


def download_order_pdf(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    pdf = generate_pdf(order)
    response = HttpResponse(pdf, content_type='application/pdf')
    response[
        'Content-Disposition'
        ] = f'attachment; filename=order_{order.order_number}.pdf'
    return response


@login_required
def wishlist(request):
    """
    view to display wishlist for logged in user
    """
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all()
    context = {
        'wishlist': wishlist,
        'products': products,
    }
    template = 'profiles/wishlist.html'
    return render(request, template, context)


@login_required
def add_to_wishlist(request, product_id):
    """
    view to add product to wishlist
    """
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    messages.info(request, f'Added: {product.name} to the wishlist!')
    return redirect('wishlist')


@login_required
def delete_from_wishlist(request, product_id):
    """
    view to delete product to wishlist
    """
    product = get_object_or_404(Product, id=product_id)
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.products.remove(product)
    messages.info(request, f'You removed {product.name} from the wishlist!')
    return redirect('wishlist')


@login_required
def password_change(request):
    """
    view to change user password
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.info(
                request, 'Your password was successfully updated!')
            return redirect('info')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profiles/password_change.html', {'form': form})
