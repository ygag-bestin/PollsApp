from django.contrib.auth import get_user_model, logout
from django.contrib.auth import views as auth_views
from django.views import generic
from django.views.generic import CreateView
from django import forms
from .forms import SignUpForm, LoginForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

User = get_user_model()


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    success_url = reverse_lazy('index')
    template_name = 'accounts/login.html'


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('polls:index'))


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'accounts/signup.html', {'form': form})

    def send_UserVerfication_email(self, request, user, form): #rename send user verifcatiobn email
        current_site = get_current_site(request)
        mail_subject = 'Activate your poll account.'
        message = render_to_string('accounts/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('Please confirm your email address to '
                            'complete the registration')

    def post(self, request):
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                return self.send_UserVerfication_email(request, user, form)
        else:
            form = SignUpForm()
        return render(request, 'accounts/signup.html', {'form': form})


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user,
                                                                     token):
            user.is_active = True
            user.save()
            # login(request, user)
            messages.success(
                request,
                "Email verification was successful"
            )
            return redirect('users:login')

        else:

            messages.warning(
                request,
                "Activation link is invalid!"
            )
            return redirect('users:signup')


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/change-password.html'

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been changed.')
        return super().form_valid(form)


