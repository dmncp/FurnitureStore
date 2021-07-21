from django.urls import reverse_lazy
from django.views import generic
from .forms import UserCreationForm, ContactForm, UserChangeForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import UserAddress, Address


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
