from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from accounts.forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, SocialForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from accounts.models import Social
from courses.models import Courses, Comments
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.contrib.auth.views import LogoutView, LoginView

User = get_user_model()


def users_signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('accounts/activate_email_account.html', {
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
            return render(request, 'accounts/email_sent.html')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def email_activate_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for confirming your email, you can now access your account.')

        return render(request, 'accounts/activation_success.html')
    else:
        messages.error(request, 'Activation error, Invalid link.')
        return render(request, 'accounts/activation_error.html')


class UsersLoginView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('account')


class UsersLogoutView(LogoutView):
    template_name = 'accounts/logout.html'


class Dashboard(ListView):
    template_name = 'accounts/dashboard.html'

    def get_queryset(self):
        self.username = get_object_or_404(User, username=self.kwargs['username'])
        return Courses.objects.filter(author=self.username)

    def get_context_data(self, *args, **kwargs):
        context = super(Dashboard, self).get_context_data(*args, **kwargs)
        context['author_list'] = self.request.user


@login_required()
def dashboard(request):
    courses = request.user.courses_set.all().order_by('-published')
    context = {
        'courses': courses,
    }
    return render(request, 'accounts/dashboard.html', context)


class UsersProfileView(LoginRequiredMixin, ListView):
    template_name = 'base-user-profile.html'

    context_object_name = 'courses'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(username=self.kwargs['username'])
        return context

    def get_queryset(self):
        self.username = get_object_or_404(User, username=self.kwargs['username'])
        return Courses.objects.filter(author=self.username)


def user_account_update_form(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated')
            return redirect('accounts:dashboard')
            # return redirect('accounts:user_profile')
    else:
        form = UserUpdateForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/update/edit_account_info.html', context)


def user_profile_update_form(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('accounts:dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'form': form
    }
    return render(request, 'accounts/update/edit_profile_info.html', context)


def user_social_form(request):
    if request.method == 'POST':
        form = SocialForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your social profile has been updated')
            return redirect('accounts:dashboard')
    else:
        form = SocialForm(instance=request.user.profile)
    context = {
        'social': form
    }
    return render(request, 'accounts/social_form.html', context)


class ProfileBaseTemplateView(ListView):
    model = Social
    template_name = 'base-user-profile.html'


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password/change_password.html'
    success_url = reverse_lazy('accounts:password_change_done')


class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'accounts/password/change_password_done.html'


class PasswordReset(PasswordResetView):
    template_name = 'accounts/password/reset_password.html'
    success_url = reverse_lazy('accounts:reset_done')
    email_template_name = 'accounts/password/password_reset_email.html'


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'accounts/password/reset_password_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'accounts/password/reset_password_confirm.html'
    success_url = reverse_lazy('accounts:reset_complete')


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'accounts/password/reset_password_complete.html'
