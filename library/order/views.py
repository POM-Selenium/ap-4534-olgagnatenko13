from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

from order.models import Order
from book.models import Book
from .forms import OrderForm, OrderFilterForm


@login_required
def orders_list(request):
    form = OrderFilterForm(request.GET)

    if request.user.role == 1:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)

    if form.is_valid():
        if form.cleaned_data.get('user_email'):
            orders = orders.filter(user__email__iexact=form.cleaned_data['user_email'])
        if form.cleaned_data.get('date_from'):
            orders = orders.filter(created_at__date__gte=form.cleaned_data['date_from'])
        if form.cleaned_data.get('date_to'):
            orders = orders.filter(created_at__date__lte=form.cleaned_data['date_to'])

    return render(request, 'orders/list.html', {'orders': orders, 'form': form})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user, end_at=None)
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def create_order(request):
    if request.user.role == 1:
        return redirect('/orders/')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            book = form.cleaned_data['book_id']
            Order.create(request.user, book, form.cleaned_data['plated_end_at'])
            book.count -= 1
            book.save()
            messages.success(request, 'Order created successfully.')
            return redirect('/orders/')
    else:
        form = OrderForm()

    return render(request, 'orders/create.html', {'form': form})


@login_required
def close_order(request, order_id):
    if request.user.role != 1:
        return redirect('/orders/')

    order = get_object_or_404(Order, pk=order_id)
    if order.end_at is None:
        order.end_at = timezone.now()
        order.save()
        book = order.book
        if book:
            book.count += 1
            book.save()
        messages.success(request, 'Order closed successfully.')
    return redirect('/orders/')