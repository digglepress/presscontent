from django.urls import path

from accounts.views import (UsersLoginView, UsersLogoutView,
                            email_activate_view, users_signup_view, dashboard,
                            user_account_update_form, user_profile_update_form, user_social_form, PasswordChange,
                            PasswordChangeDone, PasswordReset, PasswordResetDone, PasswordResetConfirm,
                            PasswordResetComplete, UsersProfileView)
app_name = 'accounts'
urlpatterns = [
    path('accounts/signup/', users_signup_view, name="register"),
    path('accounts/activate/<slug:uidb64>/<slug:token>/', email_activate_view, name='activate'),
    path('accounts/login/', UsersLoginView.as_view(), name='login'),
    path('accounts/logout/', UsersLogoutView.as_view(), name='logout'),
    path('accounts/account/update/', user_account_update_form, name='user_account_update_form'),
    path('accounts/profile/update/', user_profile_update_form, name='user_profile_update_form'),
    path('accounts/social/update/', user_social_form, name='user_social_form'),
    path('accounts/password/change/', PasswordChange.as_view(), name='password_change'),
    path('accounts/password/change/done/', PasswordChangeDone.as_view(), name='password_change_done'),
    path('accounts/password/reset/', PasswordReset.as_view(), name='password_reset'),
    path('accounts/password/reset/done/', PasswordResetDone.as_view(), name='reset_done'),
    path('accounts/password/reset/complete/', PasswordResetComplete.as_view(), name='reset_complete'),
    path('accounts/password/reset/confirm/<uidb64>/<token>', PasswordResetConfirm.as_view(), name='reset_confirm'),
    path('author/<str:username>/', UsersProfileView.as_view(), name='profile'),
    path('dashboard/', dashboard, name='dashboard'),
]
