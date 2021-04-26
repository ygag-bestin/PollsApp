from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from . import views
from .forms import CustomEmailValidation
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import reverse_lazy

app_name = 'users'

urlpatterns = [
                  path('signup/', views.SignUpView.as_view(), name='signup'),
                  path('login/', auth_views.LoginView.as_view(
                      template_name='accounts/login.html',
                      redirect_field_name='next',
                      authentication_form=LoginForm,
                      extra_context={
                          'next': 'polls:index',
                      },
                  ), name='login'),
                  path('logout/', views.LogoutView.as_view(), name='logout'),
                  path("password_reset/",
                       auth_views.PasswordResetView.as_view(
                           template_name='accounts/password/password_reset'
                                         '.html',
                           form_class=CustomEmailValidation,
                           email_template_name='accounts/password'
                                               '/password_reset_email.html',
                           success_url=reverse_lazy('users'
                                                    ':password_reset_done')),
                       name="password_reset"),
                  path('password_reset/done/',
                       auth_views.PasswordResetDoneView.as_view(
                           template_name='accounts/password'
                                         '/password_reset_done.html'),
                       name='password_reset_done'),
                  path('reset/<uidb64>/<token>/',
                       auth_views.PasswordResetConfirmView.as_view(
                           template_name="accounts/password"
                                         "/password_reset_confirm.html",
                           success_url=reverse_lazy(
                               "users:password_reset_complete")),

                       name='password_reset_confirm'),
                  path('reset/done/',
                       auth_views.PasswordResetCompleteView.as_view(
                           template_name='accounts/password'
                                         '/password_reset_complete.html'),
                       name='password_reset_complete'),
                  path(
                      'change-password/',
                      views.CustomPasswordChangeView.as_view(success_url="/"),

                      name='change_password'
                  ),
                  path('activate/<uidb64>/<token>/',
                       views.ActivateView.as_view(), name='activate'),
                  path('api/', include('users.api.urls'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
