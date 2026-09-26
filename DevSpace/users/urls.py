from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [path('login/', views.UserLogin.as_view(), name='login'),
               path ('logout/', views.LogoutView.as_view(), name='logout'),
               path('register/', views.UserRegisterView.as_view(), name='register'),
               path('profile/', views.UerProfileView.as_view(), name='profile'),
               path('profile/change_password/', views.UserPasswordChange.as_view(), name='change_password'),
               path('profile/change_password_done/', views.UserPasswordChangeDone.as_view(), name='password_change_done'),
               path('password_reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
               path('password_reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
               path('reset/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
               path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
               path('oauth2/remove', views.remove_oauth2_view, name='remove_oauth2_request'),
               path('oauth2/remove/<provider>/confirm/', views.DisconnectOauth2View.as_view(), name='disconnect_oauth2_confirm'),]