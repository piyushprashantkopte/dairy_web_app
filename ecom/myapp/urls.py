from django.urls import path
from myapp.views import *
from django.contrib.auth import views as auth_view
from .forms import LoginForm,MyPasswordResetForm,MyPasswordChangeForm,MySetPasswordForm

urlpatterns = [
    path("", home , name='home'),
    path("about/", about , name='about'),
    path("contact/", contact , name='contact'),
    path("category/<slug:val>/", CategoryView.as_view() , name='category'),
    path("category-title/<val>/", CategoryTitle.as_view() , name='category-title'),
    path("product-detail/<int:pk>/", ProductDetail.as_view() , name='product-detail'),
    path("profile/", ProfileView.as_view() , name='profile'),
    path("address/", address , name='address'),
    path("updateAddress/<int:pk>", UpdateAddress.as_view() , name='updateAddress'),
    path("add-to-cart/", add_to_cart , name='add_to_cart'),
    path("cart/", show_cart , name='showcart'),
    path("checkout/", checkout.as_view() , name='checkout'),
    path("pluscart/", plus_cart),
    path("minuscart/", plus_cart),
    path("removecart/", remove_cart),



    #login Authentication
    path("registration/", CustomerRegistrationView.as_view() , name='customerregistration'),
    path("accounts/login/", auth_view.LoginView.as_view(template_name='login.html' ,authentication_form=LoginForm ), name='login'),
    path("passwordchange/", auth_view.PasswordChangeView.as_view(template_name='changepassword.html' , form_class=MyPasswordChangeForm ,success_url='/passwordchangedone'), name='passwordchange'),
    path("passwordchangedone/", auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html' ), name='passwordchangedone'),
    path("logout/", auth_view.LogoutView.as_view(template_name='',next_page='login.html') , name='logout'),

    path("password-reset/", auth_view.PasswordResetView.as_view(template_name='password_reset.html' , form_class=MyPasswordResetForm), name='password_reset'),

    path("password-reset-done/", auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html' ), name='password_reset_done'),

    path("password-reset-confirm/<uidb64>/<token>/", auth_view.PasswordResetConfirmView.as_view(template_name='password_reset.html' , form_class=MySetPasswordForm), name='password_reset_confirm'),

    path("password-reset-complete/", auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html' ), name='password_reset_complete'),
]
