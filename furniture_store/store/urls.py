from django.urls import path
from django.views.generic.base import TemplateView
from .views import *
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('contact', contactView, name='contact'),
    path('settings', settings_view, name='settings'),
    path('settings/profile', EditProfileView.as_view(), name='profile'),
    path('settings/address', AddressEditView.as_view(template_name='address_edit.html'), name='address'),
    path('settings/address/edit/<int:pk>', AddressEditFormView.as_view(template_name='address_edit_form.html'), name='address_form'),
    path('settings/address/delete/<int:pk>', delete_address, name='address_delete'),
    path('settings/customer_orders', CustomerOrdersView.as_view(template_name='customer_orders.html'), name='customer_orders'),
    path('settings/customer_orders/details/<str:pk>', OrderDetailsView.as_view(template_name='order_details.html'), name='order_details'),
    path('settings/opinions', OpinionsView.as_view(template_name='opinions.html'), name='opinions'),
    path('settings/opinions/delete/<int:pk>', delete_opinion_user, name='delete_opinion'),
    path('settings/opinions/edit/<int:pk>', OpinionEditFormView.as_view(template_name='opinions_edit.html'), name='opinion_edit'),
    path('settings/delete_account', delete_account, name='delete_user'),
    path('settings/delete_confirm', TemplateView.as_view(template_name='delete_user.html'), name='delete_user_confirmation'),
    path('settings/unavailable_products', staff_member_required(UnavailableProductsView.as_view(template_name='out_of_stock_products.html')), name='unavailable'),
    path('settings/order_archive', staff_member_required(AllOrdersView.as_view(template_name='order_archive.html')), name='order_archive'),
    path('settings/order_archive/cancel_order/<str:pk>', staff_member_required(cancel_order), name='cancel_order'),
    path('settings/order_archive/details/<str:pk>', staff_member_required(OrderDetailsView.as_view(template_name='all_details.html')), name='all_details'),
    path('settings/order_archive/edit/<str:pk>', staff_member_required(EditOrderView.as_view(template_name='order_edit.html')), name='order_edit'),
    path('settings/order_archive/edit/delete/<str:order_nr>/<int:prod_nr>', staff_member_required(delete_product_from_order), name='prod_delete'),
    path('settings/order_archive/edit/add/<str:pk>', staff_member_required(AddProductToOrder.as_view(template_name='order_edit_add.html')), name='order_edit_add'),
    path('settings/order_archive/edit/add/<str:order_nr>/<int:prod_nr>', staff_member_required(add_product), name='add_to_order'),
    path('settings/opinions_all', staff_member_required(OpinionsAdminView.as_view(template_name='opinions_edit_admin.html')), name='opinions_admin'),
    path('settings/opinions_all/edit/<str:pk>', staff_member_required(delete_opinion_description), name='opinions_admin_edit'),
    path('settings/opinions_all/delete/<str:pk>', staff_member_required(delete_opinion_admin), name='opinions_admin_delete'),
    path('settings/all_products', staff_member_required(AllProductsView.as_view(template_name='products_all.html')), name='all_products'),
    path('settings/all_products/edit/<int:pk>', staff_member_required(EditProductView.as_view(template_name='admin_product_edit.html')), name='edit_product_admin'),
    path('settings/all_products/delete_category/<int:pk>', staff_member_required(delete_category), name='delete_category'),
    path('settings/all_products/edit_category/<int:pk>', staff_member_required(EditCategoryView.as_view(template_name='category_edit.html')), name='category_edit'),
    path('settings/users', staff_member_required(UserListView.as_view(template_name='users.html')), name='users'),
    path('settings/users/delete/<int:pk>', staff_member_required(delete_account_admin), name='delete_user'),
    path('settings/users/activate/<int:pk>', staff_member_required(user_active), name='user_active'),
    path('shopping_cart', ShoppingCartView.as_view(template_name='shopping_cart.html'), name='shop_cart'),
    path('shopping_cart/delete/<int:pk>', delete_product_from_cart, name='delete_from_cart'),
    path('shopping_cart/address', DeliveryAddressView.as_view(template_name='delivery_address.html'), name='delivery_address'),
    path('shopping_cart/confirmation', ShoppingCartView.as_view(template_name='order_confirmation.html'), name='confirm'),
    path('shopping_cart/add_order', add_new_order, name='add_order_new'),
    path('shopping_cart/order_placed', TemplateView.as_view(template_name='thanks_for_order.html'), name='thanks'),
    path('categories', CategoriesView.as_view(template_name='category_choice.html'), name='category_choice'),
    path('categories/products/<int:pk>', ProductsMainView.as_view(template_name='products_main_view.html'), name='products_main'),
    path('categories/products/add_to_shopping_cart/<int:pk>', add_to_shopping_cart, name='add_to_cart'),
    path('categories/products/details/<int:pk>', ProductDetailsView.as_view(template_name='product_details.html'), name='prod_details'),
    path('statute', TemplateView.as_view(template_name='statute.html'), name='statute'),
    path('paying_info', TemplateView.as_view(template_name='paying_info.html'), name='paying_info'),
    path('installment_shopping', TemplateView.as_view(template_name='installment_shopping.html'), name='installment_shopping'),
    path('about_us', TemplateView.as_view(template_name='about_us.html'), name='about_us'),
    path('producers', TemplateView.as_view(template_name='producers.html'), name='producers'),
]
