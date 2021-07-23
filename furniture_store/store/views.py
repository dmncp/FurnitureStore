from django.urls import reverse_lazy
from django.views import generic
from .forms import UserCreationForm, ContactForm, UserChangeForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('contact')
    return render(request, "contact.html", {'form': form})


def settings_view(request):
    if not request.user.is_authenticated:
        return redirect('home')
    return render(request, 'settings.html')


class EditProfileView(LoginRequiredMixin, generic.UpdateView):
    form_class = UserChangeForm
    model = User
    success_url = reverse_lazy('settings')
    template_name = 'profile_edit.html'

    def get_object(self, queryset=None):
        return self.request.user


class AddressEditView(LoginRequiredMixin, generic.ListView):
    model = UserAddress

    def get_queryset(self):
        addresses = super().get_queryset()
        addresses = addresses.filter(user=self.request.user)

        return addresses


class AddressEditFormView(LoginRequiredMixin, generic.ListView):
    model = Address

    def get_queryset(self):
        address_queryset = super().get_queryset()
        street = self.request.GET.get('street', None)
        house_nr = self.request.GET.get('house_nr', None)
        block_nr = self.request.GET.get('block_nr', None)
        zip_code = self.request.GET.get('zip_code', None)
        city = self.request.GET.get('city', None)

        if street and house_nr and zip_code and city:
            if self.kwargs['pk'] == 0:
                address = Address(city=city, street=street, house_nr=house_nr, building_nr=block_nr, zip_code=zip_code)
                address.save()

                user_address = UserAddress(user=self.request.user, address=address)
                user_address.save()

            else:
                address = Address.objects.get(id=self.kwargs['pk'])
                address.street = street
                address.city = city
                address.house_nr = house_nr
                address.building_nr = block_nr
                address.zip_code = zip_code

                address.save()

        return address_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['address'] = Address.objects.filter(id=context['pk'])[0] if context['pk'] != 0 else None

        return context


@login_required
def delete_address(request, pk):
    address = Address.objects.get(id=pk)
    user_address = UserAddress.objects.get(address=address, user=request.user)

    user_address.delete()
    address.delete()

    return redirect('address')


class CustomerOrdersView(LoginRequiredMixin, generic.ListView):
    model = Order

    def get_queryset(self):
        orders = super().get_queryset()
        orders = orders.filter(user=self.request.user)

        return orders


def get_price(user, pk):
    order = Order.objects.get(user=user, order_nr=pk)
    products = order.products.all()
    price_all = 0

    for product in products:
        price_all += product.product.price * product.amount

    return price_all


class OrderDetailsView(LoginRequiredMixin, generic.ListView):
    model = Order

    def get_queryset(self):
        orders = super().get_queryset()
        order = orders.get(order_nr=self.kwargs['pk'])

        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['price_all'] = get_price(self.request.user, self.kwargs['pk'])

        return context


class OpinionsView(LoginRequiredMixin, generic.ListView):
    model = Opinion

    def get_queryset(self):
        opinions = super().get_queryset()
        opinions = opinions.filter(user=self.request.user)

        return opinions


@login_required
def delete_opinion(request, pk):
    opinion = Opinion.objects.get(id=pk)

    opinion.delete()

    return redirect('opinions')


class OpinionEditFormView(LoginRequiredMixin, generic.ListView):
    model = Opinion

    def get_queryset(self):
        opinions = super().get_queryset()
        opinion = opinions.get(id=self.kwargs['pk'])
        rating = self.request.GET.get('rating', None)
        opinion_desc = self.request.GET.get('opinion', None)

        if rating and opinion_desc:
            opinion.rating = rating
            opinion.opinion = opinion_desc
            opinion.save()

        return opinion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rating'] = self.get_queryset().rating
        context['opinion'] = self.get_queryset().opinion

        return context


@login_required
def delete_account(request):
    if not request.user.is_staff:
        # delete addresses
        addresses = UserAddress.objects.filter(user=request.user)
        for address in addresses:
            address.delete()

        # delete shopping carts
        shopping_cart = ShoppingCart.objects.filter(user=request.user)
        for cart in shopping_cart:
            cart.delete()

        # delete orders
        orders = Order.objects.filter(user=request.user)
        for order in orders:
            order.delete()

        # delete opinions
        opinions = Opinion.objects.filter(user=request.user)
        for opinion in opinions:
            opinion.delete()

        # logout user
        user_id = request.user.id
        logout(request)

        # delete account
        user = User.objects.get(id=user_id)
        user.delete()

    return redirect('home')


class UnavailableProductsView(LoginRequiredMixin, generic.ListView):
    model = Furniture

    def get_queryset(self):
        furniture = super().get_queryset()
        furniture = furniture.filter(amount=0)
        prod_id = self.request.GET.get('product_id', None)
        name = self.request.GET.get('name', None)

        if prod_id:
            furniture = furniture.filter(id=prod_id)
        if name:
            furniture = furniture.filter(name=name)

        return furniture


class AllOrdersView(LoginRequiredMixin, generic.ListView):
    model = Order

    def get_queryset(self):
        order = super().get_queryset()
        order_nr = self.request.GET.get('order_nr', None)
        client_id = self.request.GET.get('client_id', None)

        if order_nr:
            order = order.filter(order_nr=order_nr)
        if client_id:
            order = order.filter(user__id=client_id)

        return order


@login_required
def cancel_order(request, pk):
    order = Order.objects.get(order_nr=pk)
    if order.status == 'unsent':
        order.delete()
    return redirect('order_archive')


class EditOrderView(LoginRequiredMixin, generic.ListView):
    model = Order

    def get_queryset(self):
        order = super().get_queryset()
        order = order.get(order_nr=self.kwargs['pk'])
        products = order.products.all()

        for prod in products:
            amount = self.request.GET.get('a' + str(prod.id), None)
            if amount:
                prod.amount = amount
                prod.save()

        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['price_all'] = get_price(self.request.user, self.kwargs['pk'])
        context['order_id'] = self.kwargs['pk']

        return context


@login_required
def delete_product_from_order(request, order_nr, prod_nr):
    order = Order.objects.get(order_nr=order_nr)
    product = order.products.all().get(id=prod_nr)
    product.delete()

    return redirect('order_edit', order_nr)


class AddProductToOrder(LoginRequiredMixin, generic.ListView):
    model = Furniture

    def get_queryset(self):
        furniture = super().get_queryset()
        order = Order.objects.get(order_nr=self.kwargs['pk'])
        id_list = []
        for p in order.products.all():
            id_list.append(p.product.id)

        furniture = furniture.exclude(id__in=id_list)

        return furniture

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_id'] = self.kwargs['pk']

        return context


@login_required
def add_product(request, order_nr, prod_nr):
    prod_in_list = False
    order = Order.objects.get(order_nr=order_nr)

    for prod in order.products.all():
        if prod.product.id == prod_nr:
            prod_in_list = True

    if not prod_in_list:
        prod = Furniture.objects.get(id=prod_nr)
        order_product = OrderProduct(product=prod, amount=1)
        order_product.save()
        order.products.add(order_product)

    return redirect('order_edit_add', order_nr)
