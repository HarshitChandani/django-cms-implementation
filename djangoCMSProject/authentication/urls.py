from django.urls import path

from .views import login_template, register_template, handle_login, handle_signup, handle_logout

app_name = "authentication"

urlpatterns = [
    path("", login_template, name="loginPage"),
    path("login/", handle_login, name="login"),
    path("signup/", register_template, name="signupPage"),
    path("register/", handle_signup, name="register"),
    path("logout/", handle_logout, name="logout")
]
