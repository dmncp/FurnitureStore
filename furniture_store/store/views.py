import string
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib import messages
from .forms import UserCreationForm, ContactForm, UserChangeForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import random


class SuperUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser


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

    def post(self, *args, **kwargs):
        street = self.request.POST['street']
        house_nr = self.request.POST['house_nr']
        block_nr = self.request.POST['block_nr']
        zip_code = self.request.POST['zip_code']
        city = self.request.POST['city']

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
        return redirect('address')

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

        order_nr = self.request.GET.get('order_nr', None)
        sort_by = self.request.GET.get('sort_by', None)
        order = self.request.GET.get('order', None)

        if order_nr:
            orders = orders.filter(order_nr=order_nr)

        if sort_by and order:
            if order == 'desc':
                sort_by = '-' + sort_by
            orders = orders.order_by(sort_by)

        return orders


class OrderDetailsView(LoginRequiredMixin, generic.ListView):
    model = Order

    def get_queryset(self):
        orders = super().get_queryset()
        order = orders.get(order_nr=self.kwargs['pk'])

        return order


class OpinionsView(LoginRequiredMixin, generic.ListView):
    model = Opinion

    def get_queryset(self):
        opinions = super().get_queryset()
        opinions = opinions.filter(user=self.request.user)

        prod_name = self.request.GET.get('prod_name', None)
        sort_by = self.request.GET.get('sort_by', None)
        order = self.request.GET.get('order', None)

        if prod_name:
            opinions = opinions.filter(furniture__name=prod_name)

        if sort_by and order:
            if order == 'desc':
                sort_by = '-' + sort_by
            opinions = opinions.order_by(sort_by)

        return opinions


def get_rating(product):
    opinions = Opinion.objects.filter(furniture=product)
    rate, counter = 0, 0
    for opinion in opinions:
        rate += opinion.rating
        counter += 1

    return rate // counter if counter > 0 else 0


def delete_opinion(pk):
    opinion = Opinion.objects.get(id=pk)
    product = opinion.furniture
    opinion.delete()
    product.rating = get_rating(product)
    product.save()


@login_required
def delete_opinion_user(request, pk):
    delete_opinion(pk)
    return redirect('opinions')


class OpinionEditFormView(LoginRequiredMixin, generic.ListView):
    model = Opinion

    def post(self, *args, **kwargs):
        rating = self.request.POST['rating']
        opinion_desc = self.request.POST['opinion']
        opinion = Opinion.objects.get(id=self.kwargs['pk'])

        if rating:
            opinion.rating = rating
            opinion.opinion = opinion_desc
            opinion.save()
        product = opinion.furniture
        product.rating = get_rating(product)
        product.save()

        return redirect('opinions')

    def get_queryset(self):
        opinions = super().get_queryset()
        opinion = opinions.get(id=self.kwargs['pk'])

        return opinion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rating'] = self.get_queryset().rating
        context['opinion'] = self.get_queryset().opinion

        return context


@login_required
def delete_account(request):
    # logout user
    # logout(request)
    # delete account
    user = User.objects.get(id=request.user.id)
    user.is_active = False
    user.save()

    return redirect('home')


class UnavailableProductsView(LoginRequiredMixin, generic.ListView):
    model = Furniture

    def get_queryset(self):
        furniture = super().get_queryset()
        furniture = furniture.filter(amount=0)
        prod_id = self.request.GET.get('product_id', None)
        name = self.request.GET.get('name', None)
        category_name = self.request.GET.get('category_name', None)

        sort_by = self.request.GET.get('sort_by', None)
        order = self.request.GET.get('order', None)

        if prod_id:
            furniture = furniture.filter(id=prod_id)
        if name:
            furniture = furniture.filter(name=name)
        if category_name:
            furniture = furniture.filter(type__name=category_name)

        if sort_by and order:
            if order == 'desc':
                sort_by = '-' + sort_by
            furniture = furniture.order_by(sort_by)

        return furniture


class AllOrdersView(LoginRequiredMixin, generic.ListView):
    model = Order

    def post(self, *args, **kwargs):
        status = self.request.POST['status']
        status = status.split('+')

        if status:
            order = Order.objects.get(id=status[1])
            new_status = status[0]

            order.status = new_status
            order.save()

        return redirect('order_archive')

    def get_queryset(self):
        order = super().get_queryset()
        order_nr = self.request.GET.get('order_nr', None)
        client_id = self.request.GET.get('client_id', None)
        sort_by = self.request.GET.get('sort_by', None)
        sort_order = self.request.GET.get('order', None)

        if order_nr:
            order = order.filter(order_nr=order_nr)
        if client_id:
            order = order.filter(user__id=client_id)

        if sort_by and sort_order:
            if sort_order == 'desc':
                sort_by = '-' + sort_by
            order = order.order_by(sort_by)

        return order


def delete_order_products(order_id):
    order = Order.objects.get(id=order_id)
    for product in order.products.all():
        product.delete()


@login_required
def cancel_order(request, pk):
    order = Order.objects.get(order_nr=pk)
    if order.status == 'unsent':
        for product in order.products.all():
            furniture = product.product
            furniture.amount += product.amount
            furniture.save()
        delete_order_products(order.id)
        order.delete()
    return redirect('order_archive')


def get_price(order):
    products = order.products.all()
    price_all = 0

    for product in products:
        price_all += product.product.price_with_discount * product.amount

    return round(price_all, 2)


class EditOrderView(LoginRequiredMixin, generic.ListView):
    model = Order

    def post(self, *args, **kwargs):
        order = Order.objects.get(order_nr=self.kwargs['pk'])
        products = order.products.all()

        for prod in products:
            amount = self.request.POST['a' + str(prod.id)]
            if amount:
                furniture = prod.product
                furniture.amount -= (int(amount) - prod.amount)
                furniture.save()

                prod.amount = int(amount)
                prod.save()

                order.price = get_price(order)
                order.save()
        return redirect('order_edit', self.kwargs['pk'])

    def get_queryset(self):
        order = super().get_queryset()
        order = order.get(order_nr=self.kwargs['pk'])

        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_id'] = self.kwargs['pk']

        return context


@login_required
def delete_product_from_order(request, order_nr, prod_nr):
    order = Order.objects.get(order_nr=order_nr)
    product = order.products.all().get(id=prod_nr)

    furniture_id = product.product.id
    amount = product.amount

    furniture = Furniture.objects.get(id=furniture_id)
    furniture.amount += amount

    furniture.save()
    product.delete()

    order.price = get_price(order)
    order.save()

    if len(order.products.all()) == 0:
        order.delete()
        delete_order_products(order.id)
        return redirect('order_archive')

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
        if prod.amount > 0:
            order_product = OrderProduct(product=prod, amount=1)
            order_product.save()
            order.products.add(order_product)

            prod.amount -= 1
            prod.save()

            order.price = get_price(order)
            order.save()
        else:
            messages.warning(request, 'Ten produkt jest niedostępny')
    else:
        messages.warning(request, 'Ten produkt należy już do zamówienia')

    return redirect('order_edit_add', order_nr)


class OpinionsAdminView(SuperUserCheck, generic.ListView):
    model = Opinion

    def get_queryset(self):
        opinions = super().get_queryset()
        opinion_id = self.request.GET.get('opinion_id', None)
        client_id = self.request.GET.get('client_id', None)
        product_name = self.request.GET.get('product_name', None)

        if opinion_id:
            opinions = opinions.filter(id=opinion_id)
        if client_id:
            opinions = opinions.filter(user__id=client_id)
        if product_name:
            opinions = opinions.filter(furniture__name=product_name)

        return opinions


@login_required
def delete_opinion_admin(request, pk):
    if request.user.is_superuser:
        delete_opinion(pk)
    return redirect('opinions_admin')


@login_required
def delete_opinion_description(request, pk):
    if request.user.is_superuser:
        opinion = Opinion.objects.get(id=pk)

        opinion.opinion = ''
        opinion.save()

    return redirect('opinions_admin')


class AllProductsView(SuperUserCheck, generic.ListView):
    model = Furniture

    def get_queryset(self):
        products = super().get_queryset()
        prod_id = self.request.GET.get('prod_id', None)
        price_from = self.request.GET.get('price_from', None)
        price_to = self.request.GET.get('price_to', None)
        category = self.request.GET.get('category', None)
        prod_name = self.request.GET.get('prod_name', None)
        state = self.request.GET.get('state', None)

        if prod_id:
            products = products.filter(id=prod_id)
        if price_from:
            products = products.filter(price__gte=price_from)
        if price_to:
            products = products.filter(price__lte=price_to)
        if category:
            products = products.filter(type__name=category)
        if prod_name:
            products = products.filter(name=prod_name)
        if state:
            products = products.filter(state=state)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = FurnitureType.objects.all()

        return context


class EditProductView(SuperUserCheck, generic.ListView):
    model = Furniture

    def post(self, *args, **kwargs):
        prod_name = self.request.POST['prod_name']
        prod_type_name = self.request.POST['prod_type']
        prod_state = self.request.POST['prod_state']
        prod_price = self.request.POST['prod_price']
        prod_origin = self.request.POST['prod_origin']
        prod_material = self.request.POST['prod_material']
        prod_desc = self.request.POST['prod_desc']
        prod_amount = self.request.POST['prod_amount']
        prod_warranty = self.request.POST['prod_warranty']
        prod_discount = self.request.POST['prod_discount']
        prod_height = self.request.POST['prod_height']
        prod_width = self.request.POST['prod_width']
        prod_depth = self.request.POST['prod_depth']
        prod_type = FurnitureType.objects.get(name=prod_type_name)

        if self.kwargs['pk'] == 0:
            prod_to_edit = Furniture(name=prod_name, type=prod_type, state=prod_state, price=prod_price,
                                     origin=prod_origin, material=prod_material, description=prod_desc,
                                     amount=prod_amount, warranty_time=prod_warranty, discount=prod_discount,
                                     height=prod_height, width=prod_width, depth=prod_depth)
        else:
            prod_to_edit = Furniture.objects.get(id=self.kwargs['pk'])
            if prod_name and prod_type_name and prod_state and prod_price and prod_origin and prod_material and prod_desc \
                    and prod_amount and prod_warranty and prod_discount and prod_height and prod_depth and prod_width:
                prod_to_edit.name = prod_name
                prod_to_edit.state = prod_state
                prod_to_edit.price = prod_price
                prod_to_edit.origin = prod_origin
                prod_to_edit.material = prod_material
                prod_to_edit.description = prod_desc
                prod_to_edit.amount = prod_amount
                prod_to_edit.warranty_time = prod_warranty
                prod_to_edit.discount = prod_discount
                prod_to_edit.height = prod_height
                prod_to_edit.width = prod_width
                prod_to_edit.depth = prod_depth
                prod_to_edit.type = prod_type

        prod_to_edit.save()
        return redirect('all_products')

    def get_queryset(self):
        products = super().get_queryset()
        product = products.filter(id=self.kwargs['pk'])
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = FurnitureType.objects.all()
        context['pk'] = self.kwargs['pk']

        return context


@login_required
def delete_category(request, pk):
    if request.user.is_superuser:
        category = FurnitureType.objects.get(id=pk)
        products = Furniture.objects.filter(type=category)

        if products.exists():
            messages.warning(request, f'Kategoria {category.name} jest w użyciu. Operacja usunięcia niemożliwa.')
        else:
            category.delete()

    return redirect('all_products')


class EditCategoryView(SuperUserCheck, generic.ListView):
    model = FurnitureType

    def post(self, *args, **kwargs):
        cat_name = self.request.POST['cat_name']
        url = self.request.POST['url']
        if self.kwargs['pk'] == 0:
            category = FurnitureType(name=cat_name, url=url)
        else:
            category = FurnitureType.objects.get(id=self.kwargs['pk'])
            if cat_name:
                category.name = cat_name
                category.url = url

        category.save()
        return redirect('all_products')

    def get_queryset(self):
        categories = super().get_queryset()
        category = categories.filter(id=self.kwargs['pk'])
        return category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']

        return context


class UserListView(SuperUserCheck, generic.ListView):
    model = User

    def post(self, *args, **kwargs):
        permission = self.request.POST['permission_new']
        permission = permission.split('+')
        user = User.objects.get(id=permission[1])

        if permission[0] == 'client':
            user.is_staff = False
            user.is_superuser = False
        elif permission[0] == 'worker':
            user.is_staff = True
            user.is_superuser = False
        elif permission[0] == 'admin':
            user.is_staff = True
            user.is_superuser = True
        user.save()

        return redirect('users')

    def get_queryset(self):
        users = super().get_queryset()
        user_id = self.request.GET.get('user_id', None)
        user_name = self.request.GET.get('user_name', None)
        permission = self.request.GET.get('permission', None)

        sort_by = self.request.GET.get('sort_by', None)
        sort_order = self.request.GET.get('order', None)

        if user_id:
            users = users.filter(id=user_id)
        if user_name:
            users = users.filter(username=user_name)
        if permission:
            if permission == 'client':
                users = users.filter(is_staff=False)
            elif permission == 'worker':
                users = users.filter(is_staff=True, is_superuser=False)
            else:
                users = users.filter(is_superuser=True)

        if sort_by and sort_order:
            if sort_order == 'desc':
                sort_by = '-' + sort_by
            users = users.order_by(sort_by)

        return users


@login_required
def delete_account_admin(request, pk):
    if request.user.is_superuser:
        # delete account
        user = User.objects.get(id=pk)
        user.is_active = False
        user.save()

    return redirect('users')


def get_all_price(products):
    price = 0
    for product in products:
        price += product.furniture.price_with_discount * product.amount
    return round(price, 2)


class ShoppingCartView(LoginRequiredMixin, generic.ListView):
    model = ShoppingCart

    def post(self, *args, **kwargs):
        amount = self.request.POST['amount']
        prod_id = self.request.POST['prod_id']
        furniture = Furniture.objects.get(id=prod_id)

        if furniture.amount - int(amount) >= 0:
            cart = ShoppingCart.objects.get(user=self.request.user, furniture__id=prod_id)
            cart.amount = amount
            cart.save()
        else:
            messages.warning(self.request, f'Produkt {furniture.name} jest niedostępny w podanej ilości. '
                                           f'Aktualnie możesz zamówić maksymalnie {furniture.amount} sztuk.')

        return redirect('shop_cart')

    def get_queryset(self):
        products = super().get_queryset()
        products = products.filter(user=self.request.user)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_price'] = get_all_price(self.get_queryset())

        return context


@login_required
def delete_product_from_cart(request, pk):
    cart = ShoppingCart.objects.get(user=request.user, furniture__id=pk)
    cart.delete()
    return redirect('shop_cart')


class DeliveryAddressView(LoginRequiredMixin, generic.ListView):
    model = UserAddress

    def post(self, *args, **kwargs):
        address_id = self.request.POST['address']
        products = ShoppingCart.objects.filter(user=self.request.user)
        for product in products:
            address = UserAddress.objects.get(id=address_id)
            product.address = address
            product.save()

        return redirect('confirm')


def generate_order_nr():
    orders = Order.objects.all()
    order_numbers = []
    for order in orders:
        order_numbers.append(order.order_nr)

    random_order_nr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

    while random_order_nr in order_numbers:
        random_order_nr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

    return random_order_nr


@login_required
def add_new_order(request):
    products = ShoppingCart.objects.filter(user=request.user)
    order = Order(user=request.user, order_nr=generate_order_nr(), price=get_all_price(products),
                  address=products[0].address)
    order.save()

    for product in products:
        order_product = OrderProduct(product=product.furniture, amount=product.amount)
        order_product.save()
        order.products.add(order_product)

        product.furniture.amount -= product.amount
        product.furniture.save()
        product.delete()

    return redirect('thanks')


def categories_counter():
    id_list = []
    category_amount = {c.id: 0 for c in FurnitureType.objects.all()}

    for product in Furniture.objects.all():
        category_amount[product.type.id] += 1
        if product.type.id not in id_list:
            id_list.append(product.type.id)

    return id_list


class CategoriesView(generic.ListView):
    model = FurnitureType

    def get_queryset(self):
        categories = super().get_queryset()
        categories = categories.filter(id__in=categories_counter())

        return categories


class ProductsMainView(generic.ListView):
    model = Furniture

    def get_queryset(self):
        products = super().get_queryset()
        products = products.filter(type__id=self.kwargs['pk'], amount__gt=0)

        prod_name = self.request.GET.get('prod_name', None)
        state = self.request.GET.get('state', None)
        height_from = self.request.GET.get('height_from', None)
        height_to = self.request.GET.get('height_to', None)
        price_from = self.request.GET.get('price_from', None)
        price_to = self.request.GET.get('price_to', None)
        sort_by = self.request.GET.get('sort_by', None)
        order = self.request.GET.get('order', None)

        if prod_name:
            products = products.filter(name__icontains=prod_name)
        if state:
            products = products.filter(state=state)
        if height_from:
            products = products.filter(height__gte=height_from)
        if height_to:
            products = products.filter(height__lte=height_to)
        if price_from:
            products = products.filter(price__gte=price_from)
        if price_to:
            products = products.filter(price__lte=price_to)

        if sort_by and order:
            if order == 'desc':
                sort_by = '-' + sort_by
            products = products.order_by(sort_by)

        return products


@login_required
def add_to_shopping_cart(request, pk):
    product = Furniture.objects.get(id=pk)
    if product.amount > 0:
        cart = ShoppingCart(user=request.user, furniture=product, amount=1, address=None)
        cart.save()
    else:
        messages.warning(request, 'Ten produkt jest niedostępny')

    return redirect('products_main', product.type.id)


class ProductDetailsView(generic.ListView):
    model = Furniture

    def post(self, *args, **kwargs):
        rate = self.request.POST.get('rate', False)
        opinion_desc = self.request.POST.get('opinion_desc', False)
        rate_edit = self.request.POST.get('rate_edit', False)
        opinion_edit = self.request.POST.get('opinion_edit', False)

        if self.request.user.is_authenticated:
            if rate:
                furniture = Furniture.objects.get(id=self.kwargs['pk'])
                if not Opinion.objects.filter(user=self.request.user, furniture=furniture).exists():
                    opinion = Opinion(user=self.request.user, furniture=furniture, rating=rate, opinion=opinion_desc)
                    opinion.save()

                    furniture.rating = get_rating(furniture)
                    furniture.save()
                else:
                    messages.warning(self.request, 'Dodałeś już jedną opinię do tego produktu. Nie możesz dodać '
                                                   'kolejnej.')

            if rate_edit:
                furniture = Furniture.objects.get(id=self.kwargs['pk'])
                opinion = Opinion.objects.get(user=self.request.user, furniture=furniture)
                opinion.rating = rate_edit
                opinion.opinion = opinion_edit
                opinion.save()

                furniture.rating = get_rating(furniture)
                furniture.save()

        else:
            messages.warning(self.request, 'Musisz się zalogować żeby zostawić opinię.')

        return redirect('prod_details', self.kwargs['pk'])

    def get_queryset(self):
        products = super().get_queryset()
        products = products.get(id=self.kwargs['pk'])

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opinions'] = Opinion.objects.filter(furniture__id=self.kwargs['pk'])
        context['user_opinion'] = Opinion.objects.filter(user=self.request.user,
                                                         furniture__id=self.kwargs['pk']) if self.request.user.is_authenticated else None
        return context
