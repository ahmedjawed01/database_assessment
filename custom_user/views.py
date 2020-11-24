from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, HttpResponseRedirect
from django.urls import reverse


class CustomLoginView(LoginView):
    form_class = AuthenticationForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            db = request.path
            user = authenticate(request=request, username=username, password=password)
            login(request, user)
            if db == '/login/':
                return redirect('/admin/')
            if db == '/bb-product-login/':
                return HttpResponseRedirect(reverse('bb_product'))
            if db == '/population-login/':
                return HttpResponseRedirect(reverse('populations'))
        else:
            return self.form_invalid(form)
