from django.conf import settings
from django.views.generic import RedirectView
from django.shortcuts import redirect
from django.http.response import Http404
from django.contrib.auth import views
from django.urls import reverse_lazy
from two_factor import views as tfa_views
from two_factor.utils import default_device
from apps.account import forms
from apps.account import models
from vulnman.core.views.mixins import ThemeMixin, VulnmanContextMixin
from vulnman.core.views import generics
from apps.account.token import account_activation_token


class Index(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_vendor:
                return reverse_lazy('responsible_disc:vulnerability-list')
            return reverse_lazy('projects:project-list')
        return reverse_lazy('account:login')


class Login(ThemeMixin, tfa_views.LoginView):
    template_name = "account/login.html"


class Logout(views.LogoutView):
    pass


class Profile(generics.VulnmanDetailView):
    template_name = "account/profile.html"
    context_object_name = "user"
    slug_field = "username"

    def get_queryset(self):
        return models.User.objects.filter(is_pentester=True, is_active=True)


class Setup2FAView(tfa_views.SetupView):
    # TODO: write tests
    # TODO: write if 2fa is really required in login, if 2fa enabled
    qrcode_url = "account:setup-2fa-qr"
    template_name = "account/components/profile/tfa_setup.html"
    success_url = reverse_lazy("index")

    def get_success_url(self):
        return reverse_lazy("account:user-profile", kwargs={"slug": self.request.user.username})

    def get(self, request, *args, **kwargs):
        """
        Start the setup wizard. Redirect if already enabled.
        """
        if default_device(self.request.user):
            return redirect(self.get_success_url())
        return super().get(request, *args, **kwargs)


class Disable2FAView(tfa_views.DisableView):
    pass


class QRCodeGeneratorView(tfa_views.QRGeneratorView):
    pass


class ProfileUpdate(generics.VulnmanAuthUpdateView):
    template_name = "account/edit_profile.html"
    form_class = forms.UpdatePentesterProfileForm

    def get_object(self, queryset=None):
        qs = self.get_queryset()
        try:
            obj = qs.get()
        except qs.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" % {
                "verbose_name": qs.model._meta.verbose_name})
        return obj

    def get_queryset(self):
        return models.PentesterProfile.objects.filter(user__is_pentester=True, user=self.request.user,
                                                      user__is_active=True)

    def form_valid(self, form):
        user = form.instance.user
        user.first_name = form.cleaned_data.get("first_name")
        user.last_name = form.cleaned_data.get("last_name")
        user.save()
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial["first_name"] = self.request.user.first_name
        initial["last_name"] = self.request.user.last_name
        return initial


class ChangePassword(VulnmanContextMixin, views.PasswordChangeView):
    form_class = forms.ChangePasswordForm
    template_name = "account/change_password.html"

    def get_success_url(self):
        return reverse_lazy('account:user-profile', kwargs={'slug': self.request.user.username})


class ActivateAccount(views.PasswordResetConfirmView, VulnmanContextMixin):
    # TODO: write tests
    template_name = "account/activate_account.html"
    form_class = forms.PasswordSetForm
    token_generator = account_activation_token
    success_url = reverse_lazy(settings.LOGIN_URL)
