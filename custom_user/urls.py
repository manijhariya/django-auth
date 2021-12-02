from django.urls import path, re_path
from custom_user import views

app_name="custom_user"

urlpatterns = [
	path('login', views.log_in, name="login"),
	path('login/verify', views.verify_login, name="login-verify"),
	path('logout', views.log_out, name="logout"),
	path('delete', views.delete, name="delete"),
	path('signup', views.signup, name="signup"),
	path('signup/verify', views.verify_signup, name="signup-verify"),
	path('home', views.home, name="home"),
]
